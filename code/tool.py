# regular expression
# install numpy
# python3 -c "import nltk; nltk.download('punkt')"
import re
import sys
import os

from bs4 import BeautifulSoup
import requests
import googlesearch
from html2text import html2text
import random




def get_answers_to_questions(question_ids):
    """ retriving the most voted anwers and the accepted answers for the question with given ids """

    answers = []

    for question_id in question_ids:

        response = requests.get(ANSWERS_URL.replace("<id>", question_id))
        items = response.json()["items"]

        if items == []:
            continue

        most_voted_answer = items[0]

        body_of_most_voted_answer = most_voted_answer["body"]

        markdown_answer_body = html2text(body_of_most_voted_answer)

        answers.append(
            Answer(
                id=str(most_voted_answer["answer_id"]),
                accepted=most_voted_answer["is_accepted"],
                score=most_voted_answer["score"],
                body=markdown_answer_body,
                author=most_voted_answer["owner"]["display_name"],
                profile_image=most_voted_answer["owner"].get("profile_image", None),
        ))

    return answers


def store_questions(question_ids):
    questions = []

    for question_id in question_ids:

        response = requests.get(QUESTIONS_URL.replace("<id>", question_id))
        items = response.json()["items"]

        if items == []:
            continue

        question = items[0]

        question_body = question["body"]

        markdown_question_body = html2text(question_body)

        questions.append(Question(id=question_id, has_accepted=None, body=markdown_question_body))



    return questions


def main():

    query = input("please enter your query : ")

    questions_urls = get_questions_urls(query)  # getting all the urls of the questions related to the query.

    QUSTION_IDS = get_question_ids(questions_urls)  # getting question ids from the url.

    QUESTIONS = store_questions(QUSTION_IDS)  # storing questions all the top questions with ids in a list


    ANSWERS = get_answers_to_questions(QUSTION_IDS) # getting top most answers to the question with the given ids.

    

    print_results(QUSTION_IDS, QUESTIONS, ANSWERS)  # printing all the resutled questions with answers
