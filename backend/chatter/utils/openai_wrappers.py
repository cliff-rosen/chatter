import local_secrets as secrets
from utils import logging
import openai
import json

# from openai.embeddings_utils import get_embedding as openai_get_embedding


OPENAI_API_KEY = secrets.OPENAI_API_KEY
# COMPLETION_MODEL = 'gpt-3.5-turbo'
# COMPLETION_MODEL = "gpt-4"
COMPLETION_MODEL = "gpt-4-0125-preview"
EMBEDDING_MODEL = "text-embedding-ada-002"
MAX_TOKENS = 400

logger = logging.getLogger()
logger.info("openai_wrapper loaded")

# openai.api_key = OPENAI_API_KEY
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate(messages, temperature):

    try:
        completion = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=temperature,
            stream=False,
        )
        response = completion.choices[0].message.content

    except Exception as e:
        print("query_model error: ", str(e))
        logger.warning("get_answer.query_model error:" + str(e))
        response = "We're sorry, the server was too busy to handle this response.  Please try again."

    finally:
        print("finally")

    return response


def agenerate(messages, temperature):

    try:
        completion = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=temperature,
            stream=True,
        )

        for chunk in completion:
            message = chunk.choices[0].delta.content
            if message is None:
                message = ""
            # print(message, end="", flush=True)
            yield message

    except Exception as e:
        print("query_model error: ", str(e))
        logger.warning("get_answer.query_model error:" + str(e))
        response = "We're sorry, the server was too busy to handle this response.  Please try again."

    finally:
        print("finally")


def get_embedding(text):
    res = client.embeddings.create(
        model=EMBEDDING_MODEL, input=text, encoding_format="float"
    )
    return res.data[0].embedding
