import unittest, json
from unittest.mock import patch
from api.index import (get_top_matching_contexts, generate_random_questions, get_questions_for_skills, generateNumberOfQuizzes)

class TestQuizService(unittest.TestCase):

    @patch('api.index.open')
    @patch('json.load')
    def test_get_top_matching_contexts(self, mock_load, mock_open):
        skills_array = ["nodejs", "javascript"]
        contexts = get_top_matching_contexts(skills_array, number_of_context=2)
        self.assertEqual(contexts.__len__(), 2)


    @patch('random.sample', return_value=[{"context": "math", "question": "What is 2+2?"}])
    def test_generate_random_questions(self, mock_random_sample):
        contexts = ['patterns in software design']
        questions = generate_random_questions(contexts, num_questions_per_context=1)
        self.assertEqual(questions, [{"context": "math", "question": "What is 2+2?"}])

    @patch('api.index.get_top_matching_contexts', return_value=["math"])
    @patch('api.index.generate_random_questions', return_value=[{"context": "math", "question": "What is 2+2?"}])
    def test_get_questions_for_skills(self, mock_generate_random_questions, mock_get_top_matching_contexts):
        skills = ["geometry"]
        result = get_questions_for_skills(skills, num_of_contexts=1, number_of_questions_per_context=1)
        self.assertEqual(result, [{"context": "math", "question": "What is 2+2?"}])

    @patch('api.index.get_questions_for_skills', return_value=[{"context": "math", "question": "What is 2+2?"}])
    def test_generate_number_of_quizzes(self, mock_get_questions):
        quizzes = generateNumberOfQuizzes(["geometry"], num_of_contexts=1, number_of_questions_per_context=1, numbher_of_quizzes=2)
        self.assertEqual(len(quizzes), 2)
        self.assertEqual(quizzes, [[{"context": "math", "question": "What is 2+2?"}], [{"context": "math", "question": "What is 2+2?"}]])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestQuizService))



