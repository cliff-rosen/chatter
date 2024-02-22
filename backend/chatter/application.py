import time
from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from api import login, document, domain, prompt, answer, token, conversations, hello
from api.errors import InputError
from utils.utils import decode_token
from utils import logging


MAX_TOKENS_DEFAULT = 200
TEMPERATURE_DEFAULT = 0.4

logger = logging.getLogger()

application = Flask(__name__)
CORS(application)

logger.info("Initializing application...")

parser = reqparse.RequestParser()
parser.add_argument("domain_id", type=int)


def authenticate():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
            decoded_token = decode_token(auth_token)
            # print(decoded_token)
            if "error" in decoded_token:
                return False
        except IndexError:
            return False
    else:
        return False
    return True


"""
@app.route('/hello', methods=['POST'])
def hello():
    print(request.json)
    return 'Hello!'
"""


class Token(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        print("token", username, password)
        res = token.get_token(username, password)
        if res["status"] != "SUCCESS":
            if res["status"] == "INVALID_LOGIN":
                return (res, 401)
            else:
                res["status"] = "SERVER_ERROR"
                return (res, 500)
        return res


class Login(Resource):
    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")
        res = login.login(username, password)
        if res["status"] == "ERROR":
            if res["error"] == "UNAUTHORIZED":
                return (res, 401)
            else:
                return (res, 500)
        return res


class Domain(Resource):
    def get(self, domain_id=None):
        print("domain_id", domain_id)
        if domain_id is None:
            res = domain.get_domains()
            return res
        else:
            res = domain.get_domain(domain_id)
            return res


class Prompt(Resource):
    def get(self):
        res = prompt.get_prompt()
        return res


class Answer(Resource):
    def post(self):
        # retrieve inputs
        data = request.get_json()
        # print("body", data)
        conversation_id = data["conversation_id"]
        domain_id = data["domain_id"]
        user_id = data["user_id"]
        query = data["query"]
        prompt_template = data["prompt_template"]
        temp = data["temp"]
        deep_search = data["deep_search"]
        print("domain_id", domain_id)
        print("query", query)
        print("temp", temp)

        # execute call to get_answer()
        res = answer.get_answer(
            conversation_id,
            domain_id,
            query,
            prompt_template,
            temp,
            user_id,
            deep_search,
        )
        return res


class Conversations(Resource):
    def get(self):
        # retrieve inputs
        domain_id = request.args.get("domain_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        return conversations.get_conversations_by_time(domain_id, start_date, end_date)


class Document(Resource):
    def post(self):
        print(time.ctime())
        print("document")
        print("Content Type: " + request.headers.get("Content-Type"))
        # print(request.headers)
        print(request.get_data())
        try:
            print("files:")
            # print(request.files)
            file = request.files["file"]
            filename = file.filename
            content_type = file.content_type
            file_data = file.read()
            print(filename, content_type, file_data)
            document.insert_document(1, "", filename, "", file_data)
        except Exception as e:
            print(e)

        return {"status": "ok"}


def res():
    for chunk in hello.get_hello():
        message = chunk.choices[0].delta.content
        if not message:
            message = ""
        print(message, end="", flush=True)
        # yield json.dumps(message) + "\n"
        yield message


def res1():
    for chunk in [
        'data: {"status": "ok", "content": "1"}\n\n',
        'data: {"status": "ok", "content": "2"}\n\n',
        'data: {"status": "ok", "content": "3"}\n\n',
    ]:
        # print("about to yield", chunk)
        yield chunk
        print("yielded", chunk)
    chunk = 'data: {"status": "done", "content": ""}\n\n'
    yield chunk
    print("yielded", chunk)


def res2():
    for chunk in [
        "event: data\ndata: 1\n\n",
        "event: data\ndata: 2\n\n",
        "event: data\ndata: 3\n\n",
    ]:
        yield chunk
        print("yielded", chunk)


class Hello(Resource):
    def get(self):
        return Response(res1(), mimetype="text/event-stream")
        # return hello.get_hello()
        # return Response(hello.get_hello(), mimetype="text/event-stream")
        # return Response(res1(), mimetype="text/event-stream")


api = Api(application)
api.add_resource(Token, "/auth/token")
api.add_resource(Login, "/login")
api.add_resource(Domain, "/domain", "/domain/<int:domain_id>")
api.add_resource(Prompt, "/prompt")
api.add_resource(Answer, "/answer")
api.add_resource(Conversations, "/conversations")
api.add_resource(Hello, "/hello")
api.add_resource(Document, "/document")

if __name__ == "__main__":
    application.run(debug=True)
