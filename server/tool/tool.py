"""This module contains the logic of accessing stackoverflow,
 retrieving the adequate questions for the query in vscode, compiler error
 and then choosing the best answer for the error"""

import re
import sys
import os

import requests
import googlesearch
from html2text import html2text
import random

import sumy

import json


from .utils import ANSWERS_URL, QUESTIONS_URL, SEARCH_URL
from .utils import Question, Answer
from slugify import slugify


def google_questions(query):
    """ wrapper function for: 
    1. getting the most relevant questions of stackoverflow as results 
       obtained when when the query is searched in google
    2. getting question ids from the url obtained using regular expressions.
    3. getting the questions with those ids from stackoverflow and converting from html to text.
    """

    # getting question urls from search engine
    search_text = query + " site:stackoverflow.com"
    
    try:
        questions_urls = list(googlesearch.search(search_text))[:3]
    except:
        print("!!! can't find relate stackoverflow results in googlge !!!")

    #getting question ids from the url obtained using regular expressions.
    question_ids = get_question_ids(questions_urls)

    # getting the questions with those ids from stackoverflow and converting from html to text
    questions = []

    for qid in question_ids:
        response = requests.get(QUESTIONS_URL.replace("<id>", qid))
        items = response.json()["items"]

        if items == []:
            continue

        question_html = items[0]
        question_body = question_html["body"]
        markdown_question_body = html2text(question_body)
        questions.append(Question(id=qid, has_accepted=None, body=markdown_question_body, url=question_html["link"]))
    
    return questions

def get_question_ids(questions_urls):
    """
       taking only the question ids from the urls using regular expresssions
       parse questions id from each url path
       re.findall will return something like '/666/' so the
       [1:-1] slicing can remove these slashes
    """

    question_ids = []

    for q in questions_urls:
        if re.findall(r"/\d+/", q) != []:
            question_ids.append(re.findall(r"/\d+/", q)[0][1:-1])

    return question_ids

def ask_stackoverflow(query):
    """Ask StackOverflow (so) API for questions."""

    if query is None:
        return []

    print(query)

    response_json = requests.get(query).json()

    items = response_json["items"]

    questions = []

    for question in items:
        if question["is_answered"]:
            questions.append(Question(id=str(question["question_id"]), has_accepted="accepted_answer_id" in question, body=question["title"], url=question["link"]))

    return questions

def convert_to_searchable_query (query):
    """
    converting the raw query into api call for stackoverflow.
    """
    error_message_slug = slugify(query, separator="+")
    order = "&order=desc"
    sort = "&sort=relevance"
    intitle = f"&intitle={error_message_slug}"

    search_query = SEARCH_URL + order + sort + intitle

    return search_query


def get_answers_to_questions(questions):
    """ 
    retriving the most voted anwers and the accepted 
    answers for the question with given ids 
    """

    answers = []

    for question in questions:

        response = requests.get(ANSWERS_URL.replace("<id>", question.id))
        items = response.json()["items"]

        if items == []:
            continue
        
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
                profile_image=most_voted_answer["owner"].get(
                    "profile_image", None),
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

        # storing in database

        questions.append(
            Question(id=question_id, has_accepted=None, body=markdown_question_body))

    return questions


def print_results(questions, answers):
    """this function converts the questions and answers
    into a json file and serves it to the server and error resolver
    when they use this module.
    """

    num_of_results = len(questions)
    
    search_results = []

    for i in range(num_of_results):
    
        answer = answers[i].body

        if len(questions[i].body) > 140:
            question_title = questions[i].body[0:140] + "..."
        else:
            question_title = questions[i].body

        temp_result = {
        "index": i,
        "Title": questions[i].body,
        "TitleTrunc": question_title,
        "Answers": 1,
        "Answer": answer,
        "URL": questions[i].url,
        }

        search_results.append(temp_result)

    return search_results


def search_query(query_list, error_info):
        """This coordinate the answer aquisition process. It goes like this:
        1- Use the query to check stackexchange API for related questions
        2- If stackoverflow API search engine couldn't find questions, ask Google search engine module instead
        3- For each question, get the most voted and accepted answers
        4- Sort answers by vote count and limit them
        """

        print("1\n")
        # already constructed query which is ready for api call - const_query
        # raw_query is query in plain text
        const_query, raw_query = query_list

        if const_query == None:
            const_query = convert_to_searchable_query(raw_query)
        
        # query = "https://api.stackexchange.com/2.2/search?site=stackoverflow&order=desc&sort=relevance&tagged=python&intitle=nameerror+name+is+not+defined"

        questions = []
        
        if error_info != None:
                print(const_query)
                questions = ask_stackoverflow(const_query)
        
        
        if questions == []:
            print("entering google")
            questions = google_questions(raw_query)

        answers = get_answers_to_questions(questions)

        return print_results(questions, answers)
