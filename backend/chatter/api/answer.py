from db import db
import local_secrets as secrets
from utils.utils import make_new_conversation_id, num_tokens_from_string
from utils.openai_wrappers import agenerate
import conf
import utils.kb_service as kb
from api.errors import InputError
from utils import logging
import json
import urllib.parse

"""
prompt structure

 text:
    initial instruction
    context
    history
    query

 messages:
    system: initial instruction + context
    assistant: initial message
    user/assistant: 0 or more pairs of prior turns
    user: current query

TO DO:
set COMPLETION_MODEL_TIKTOKEN for gpt-4

"""

logger = logging.getLogger()

COMPLETION_MODEL_TIKTOKEN = "text-davinci-003"
MAX_TOKEN_COUNT = 8000
MAX_RESPONSE_TOKENS = 1000


def get_answer(
    conversation_id, domain_id, query, initial_prompt, temperature, user_id, deep_search
):
    """
    Generate an answer from the LLM based on the following items:

        initial prompt: supplied as initial_prompt
        context: retrieved from kb based on supplied query
        initial assistant message: retrieved from db based on domain
        conversation history: retrieved from conversation_id
        user query: supplied as query
    """

    # temporarily force temp to 0
    temperature = 0.0

    print("get_answer -------------------------------->")
    use_context = False
    prompt_context = ""
    context_chunks = {}
    initial_message = conf.DEFAULT_INITIAL_MESSAGE
    conversation_history = []
    response_text = ""

    print("getting domain settings")
    res = db.get_domain(domain_id)
    if res["initial_conversation_message"]:
        initial_message = res["initial_conversation_message"]
    if res["use_context"]:
        use_context = True

    print("getting conversation history")
    if conversation_id != "NEW":
        conversation_history = db.get_conversation_history(conversation_id)
        print(
            "  conversation_id: ", conversation_id, "length", len(conversation_history)
        )

    print("getting context chunks")
    if use_context:
        context_chunks = kb.get_chunks_from_query(domain_id, query)

    print("creating context from chunks")
    pre_context_token_count = num_tokens(initial_prompt, initial_message, query)
    prompt_context = create_prompt_context(
        pre_context_token_count,
        conversation_history,
        context_chunks,
        MAX_RESPONSE_TOKENS,
    )

    """
    create_prompt_context
        create_conversation_history_text
        process_chunks_and_get_as_text
    """

    print("creating prompt messages")
    messages = create_prompt_messages(
        initial_prompt,
        prompt_context,
        initial_message,
        conversation_history,
        query,
    )
    logger.info("Prompt:\n" + str(query))
    if not messages:
        return {"status": "BAD_REQUEST"}

    print("querying model")
    response = query_model(messages, temperature)

    print("returning stream")
    for message in response:
        if not message:
            message = ""
        print(message, end="", flush=True)
        data = json.dumps({"status": "ok", "content": message})
        yield "data: " + data + "\n\n"
        response_text = response_text + message

    print("updating conversation tables")
    conversation_id = update_conversation_tables(
        domain_id,
        query,
        initial_prompt,
        prompt_context,
        initial_message,
        temperature,
        conversation_id,
        conversation_history,
        response_text,
        context_chunks,
        user_id,
    )

    print("get_answer completed")
    retval = {
        "status": "response",
        "conversation_id": conversation_id,
        "answer": response_text,
        "chunks": context_chunks,
        "chunks_used_count": len(list(context_chunks.keys())),
    }
    yield "data: " + json.dumps(retval) + "\n\n"
    yield "data: " + json.dumps({"status": "done", "content": ""}) + "\n\n"


def num_tokens(*args):
    token_count = 0
    text = ""
    for arg in args:
        text += arg
    token_count += num_tokens_from_string(text, COMPLETION_MODEL_TIKTOKEN)
    return int(token_count)


def create_conversation_history_text(conversation_history):
    conversation_text = ""
    user = "User"
    ai = "Assistant"
    user_key = "query_text"
    assistant_key = "response_text"

    try:
        for row in conversation_history:
            conversation_text += (
                f"{user}: {row[user_key]}\n{ai}: {row[assistant_key]}\n\n"
            )
    except Exception as e:
        raise InputError("Bad conversationHistory record:" + str(conversation_history))
    return conversation_text


def create_prompt_context(
    pre_context_token_count,
    conversation_history,
    chunks,
    max_response_tokens,
):
    context_for_prompt = ""
    if not chunks:
        return ""

    conversation_history_text = create_conversation_history_text(conversation_history)
    conv_hist_token_count = num_tokens(conversation_history_text)
    prompt_token_count = pre_context_token_count + conv_hist_token_count
    max_context_token_count = MAX_TOKEN_COUNT - prompt_token_count - max_response_tokens

    context_for_prompt = process_chunks_and_get_as_text(chunks, max_context_token_count)

    return context_for_prompt


def process_chunks_and_get_as_text(chunks, max_chunks_token_count):
    print(
        "process_chunks_and_get_as_text using max token count of",
        max_chunks_token_count,
    )
    context = ""
    chunks_token_count = 0
    chunks_used_count = 0

    for id, chunk in sorted(
        chunks.items(), key=lambda item: item[1]["score"], reverse=True
    ):
        chunk_text = ""
        url = f"{conf.KB_BASE_URL}/{urllib.parse.quote(chunk['uri'])}"
        chunk_meta_data = (
            f"chunk_id: {str(id)}\nfilename: {chunk['uri']}\nurl: {url}\n\n"
        )
        chunk_text = "<CHUNK>\n" + chunk_meta_data + chunk["text"] + "</CHUNK>"
        tokens_in_chunk = num_tokens_from_string(chunk_text, COMPLETION_MODEL_TIKTOKEN)
        if chunks_token_count + tokens_in_chunk > max_chunks_token_count:
            print(" chunk", id, "too long to fit.  moving on.")
            chunks[id]["used"] = False
            continue

        context = context + chunk_text + "\n\n"
        chunks[id]["used"] = True
        chunks_used_count += 1
        chunks_token_count += tokens_in_chunk

    print(
        "chunks provided: %s, chunks used: %s, tokens used: %s"
        % (len(chunks), chunks_used_count, int(chunks_token_count))
    )

    if context:
        return "<START OF CONTEXT>\n" + context.strip() + "\n<END OF CONTEXT>"
    else:
        return ""


def create_prompt_text(
    initial_prompt, prompt_context, initial_message, conversation_history, query
):
    user_role = "User: "
    bot_role = "Assistant: "

    conversation_history_text = ""
    prompt = ""

    system_message = initial_prompt
    if prompt_context:
        system_message = system_message + "\n\n" + prompt_context

    conversation_history_text = create_conversation_history_text(conversation_history)

    prompt = (
        system_message
        + "\n\n"
        + bot_role
        + initial_message
        + "\n\n"
        + conversation_history_text
        + user_role
        + query
        + "\n"
        + bot_role
    )

    return prompt


def create_prompt_messages(
    initial_prompt, prompt_context, initial_message, conversation_history, query
):
    messages = []

    # add system message
    system_message = initial_prompt
    if prompt_context:
        system_message = system_message + "\n\n" + prompt_context
    messages.append({"role": "system", "content": system_message})

    # add initial assistant message
    messages.append({"role": "assistant", "content": initial_message})

    # add user and assistant messages from history
    user_key = "query_text"
    assistant_key = "response_text"
    for row in conversation_history:
        messages.append({"role": "user", "content": row[user_key]})
        messages.append({"role": "assistant", "content": row[assistant_key]})

    # add new user message
    messages.append({"role": "user", "content": query})

    # logger.info(messages)
    return messages


def query_model(messages, temperature):
    return agenerate(messages, temperature)


def update_conversation_tables(
    domain_id,
    query,
    initial_prompt,
    prompt_context,
    initial_message,
    query_temp,
    conversation_id,
    conversation_history,
    response_text,
    chunks,
    user_id,
):
    prompt_text = create_prompt_text(
        initial_prompt, prompt_context, initial_message, conversation_history, query
    )

    conversation_text = prompt_text + response_text

    if conversation_id == "NEW":
        conversation_id = make_new_conversation_id()
        db.insert_conversation(conversation_id, user_id, domain_id, conversation_text)
    else:
        db.update_conversation(conversation_id, conversation_text)

    response_chunk_ids = ", ".join(list(chunks.keys()))

    db.insert_query_log(
        domain_id,
        query,
        prompt_text,
        query_temp,
        response_text,
        response_chunk_ids,
        user_id,
        conversation_id,
    )
    # logger.info('Conversation:\n' + conversation_text)

    return conversation_id
