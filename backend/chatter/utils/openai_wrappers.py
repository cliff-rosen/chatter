import local_secrets as secrets
from utils import logging
import openai
#from openai.embeddings_utils import get_embedding as openai_get_embedding


OPENAI_API_KEY = secrets.OPENAI_API_KEY
#COMPLETION_MODEL = 'gpt-3.5-turbo'
COMPLETION_MODEL = 'gpt-4'
#COMPLETION_MODEL = 'gpt-4-32k'
EMBEDDING_MODEL = "text-embedding-ada-002"
MAX_TOKENS = 400

logger = logging.getLogger()
logger.info('openai_wrapper loaded')

#openai.api_key = OPENAI_API_KEY
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate(messages, temperature):

    response =''

    try:
        completion = client.chat.completions.create(
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


def get_embedding(text):
    res = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=text,
                    encoding_format="float"
                )
    return res.data[0].embedding
    
