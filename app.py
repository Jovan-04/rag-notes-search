from flask import Flask, request
from flask_restful import Api, Resource

from search import search
from prompt import prompt

app = Flask(__name__)
api = Api(app)

@api.resource("/")
class Hello(Resource):
    def get(self):
        return "<p>hello, world!</p>"

@api.resource("/prompt")
class Prompt(Resource):
    def get(self):
        if 'q' not in request.args:
            return 400

        return prompt(request.args['q'])

@api.resource("/search")
class Search(Resource):
    def get(self):
        if 'q' not in request.args:
            return 400

        return search(request.args['q'])

if __name__ == "__main__":
    app.run(debug=True)