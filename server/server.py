"""
this module is to serve the json of questions and answers obtained by from tool.py to the side panel of vscode frontend
"""

import sys
import json
from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS, cross_origin

from tool.tool import search_query

# initialization
app = Flask(__name__)

CORS(app)

@app.route('/receiver', methods=['POST'])
@cross_origin()
def worker():
    data = request.get_json()

    print(data["search"])

    x = {
    "Questions": search_query([None, data["search"]], None),
    }

    # x = {
    #     "Questions": [
    #         {
    #             "index":0,
    #             "Title": "Question1",
    #             "TitleTrunc": "Question1_trunc",
    #             "Answer": "Answer for question 1",
    #             "Answers": 1,
    #             "URL": "www.stackoverflow.com",
    #         },
    #         {
    #             "index":1,
    #             "Title": "Question2",
    #             "TitleTrunc": "Question2_trunc",
    #             "Answer": "Answer for question 2",
    #             "Answers": 1,
    #             "URL": "www.stackoverflow.com",
    #         },
    #         {
    #             "index":2,
    #             "Title": "Question3",
    #             "TitleTrunc": "Question3_trunc",
    #             "Answer": "Answer for question 3",
    #             "Answers": 1,
    #             "URL": "www.stackoverflow.com",
    #         }
    #     ]
    # }


    # convert into JSON:
    y = json.dumps(x)
   

    return y

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True)

