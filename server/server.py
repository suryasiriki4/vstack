import sys
import json
from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS, cross_origin

from storage import QUESTIONS
import tool

# initialization
app = Flask(__name__)

CORS(app)

@app.route('/receiver', methods=['POST'])
@cross_origin()
def worker():
    data = request.get_json()

    print(data["search"])

    print("hello world")

    # x = {
    # "Questions": tool.fun(data["search"]),
    # }

    x = {
    "Questions": ["how you doing?", "how am i doint?", "how are they doing?", "do you love me?"],
    }

    # convert into JSON:
    y = json.dumps(x)
   

    return y

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True)

