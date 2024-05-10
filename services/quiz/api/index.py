import random
from flask import request, jsonify, current_app as app
"""from .profile.profile_service import (
    create_profile,
    get_all_profiles
)"""
from .shared.helpers import (
    make_response_json,
)
from .logger import logger
import json
from flask import request, jsonify, current_app as app


with open("./api/context_skills_mapping.json", "r") as f:
    context_skills_mapping = json.load(f)

with open("./api/quizzes_dataset.json", "r") as f:
    quiz_dataset = json.load(f)

quiz_data_by_context = {}
for question in quiz_dataset:
    context = question["context"].lower()
    if context not in quiz_data_by_context:
        quiz_data_by_context[context] = []
    quiz_data_by_context[context].append(question)


# print the each context and the number of questions in it
# for context, questions in quiz_data_by_context.items():
#     logger.debug(f"Context: {context} - Number of questions: {len(questions)}")



def get_top_matching_contexts(skills_array, number_of_context=10):
    context_match_count = {}
    for context, matched_skills in context_skills_mapping.items():
        match_count = sum(1 for skill in skills_array if skill in matched_skills)
        context_match_count[context] = match_count
    sorted_contexts = sorted(context_match_count.items(), key=lambda x: x[1], reverse=True)
    return [context for context, _ in sorted_contexts[:number_of_context]]


def generate_random_questions(contexts, num_questions_per_context=20):
    selected_questions = []

    for current_context in contexts:
        if current_context not in quiz_data_by_context:
            continue


        context_questions = quiz_data_by_context[current_context]
        selected_questions.extend(random.sample(context_questions, min(num_questions_per_context, len(context_questions))))

    return selected_questions

def health_check():
    logger.debug("Health check")
    return "Hello World From Quiz Service!"


def get_questions_for_skills(skills, num_of_contexts=5, number_of_questions_per_context=20):
    contexts = get_top_matching_contexts(skills, num_of_contexts)
    questions = generate_random_questions(contexts, number_of_questions_per_context)
    return questions

def generateNumberOfQuizzes(skills, num_of_contexts=5, number_of_questions_per_context=20, numbher_of_quizzes=1):
    quizzes = []
    for _ in range(numbher_of_quizzes):
        quizzes.append(get_questions_for_skills(skills, num_of_contexts, number_of_questions_per_context))
        logger.debug(f"Generated quiz: the number of quizzes is {len(quizzes)}")
    return quizzes
