import openai
from openai.embeddings_utils import get_embedding
import logging

logger = logging.getLogger()

#COMPLETION_MODEL = 'gpt-3.5-turbo'
COMPLETION_MODEL = 'gpt-4'
#COMPLETION_MODEL = 'gpt-4-32k'
MAX_TOKENS = 400

logger.error('openai_wrapper loaded')

def generate(messages, temperature):

    response =''

    try:
        completion = openai.ChatCompletion.create(
            model=COMPLETION_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=temperature
            )
        response = completion.choices[0].message.content
    except Exception as e:
        print('query_model error: ', str(e))
        logger.warning('get_answer.query_model error:' + str(e))
        response = "We're sorry, the server was too busy to handle this response.  Please try again."

    return response

