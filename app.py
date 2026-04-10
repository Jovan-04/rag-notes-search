from flask import Flask, request, make_response, render_template
from flask_restful import Api, Resource

from search import search, build_index
from prompt import prompt

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('index.html')

@api.resource("/prompt")
class Prompt(Resource):
    def get(self):
        if 'q' not in request.args:
            return make_response("no query parameter q found :(", 400)
        
        final_answer = prompt(user_query)

        return make_response(final_answer, 200)

@api.resource("/search")
class Search(Resource):
    def get(self):
        if 'q' not in request.args:
            return make_response("no query parameter q found :(", 400)

        user_query = request.args['q']
        results = search(user_query)

        return {"query": user_query, "results": results}

if __name__ == "__main__":
    print("Initializing database...")
    build_index()
    app.run(debug=True, port=5050)