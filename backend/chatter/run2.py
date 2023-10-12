import openai
import local_secrets as secrets

print('run2')
OPENAI_API_KEY = secrets.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

