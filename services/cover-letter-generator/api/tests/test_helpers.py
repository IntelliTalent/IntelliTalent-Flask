import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from docx import Document
from api.helpers.helper import (
    get_available_titles_vectors,
    fill_template_sentence,
    fill_experience_template,
    fill_cover_letter,
    calculate_similarity,
    calculate_similarity_with_available_titles,
    get_similar_titles,
    sample_titles,
    write_to_word,
    generate_cover_letter_data,
    preprocess_user_info,
    upload_file
)


class HelpersTest(unittest.TestCase):
    def test_get_available_titles_vectors(self):
        available_title_vectors = get_available_titles_vectors()
        self.assertEqual(len(available_title_vectors), 27)

    def test_fill_template_sentence(self):
        sentence = "I worked at $worked_company as a $worked_position."
        user_info = {
            "experiences": [{"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}],
            "skills": ["Python", "Java"],
            "yearsOfExperience": 3
        }
        wanted_job_info = {"jobTitle": "Software Engineer", "companyName": "XYZ Inc"}
        result, skills_counter, global_skills_counter, experiences_counter = fill_template_sentence(
            sentence, user_info, wanted_job_info, 0, 0, 0
        )
        self.assertEqual(result, "I worked at ABC Corp as a Software Engineer.")
        self.assertEqual(skills_counter, 0)
        self.assertEqual(global_skills_counter, 0)
        self.assertEqual(experiences_counter, 1)
        
    def test_fill_template_sentence_no_dot(self):
        sentence = "I worked at $worked_company as a $worked_position"
        user_info = {
            "experiences": [{"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}],
            "skills": ["Python", "Java"],
            "yearsOfExperience": 3
        }
        wanted_job_info = {"jobTitle": "Software Engineer", "companyName": "XYZ Inc"}
        result, skills_counter, global_skills_counter, experiences_counter = fill_template_sentence(
            sentence, user_info, wanted_job_info, 0, 0, 0
        )
        self.assertEqual(result, "I worked at ABC Corp as a Software Engineer.")
        self.assertEqual(skills_counter, 0)
        self.assertEqual(global_skills_counter, 0)
        self.assertEqual(experiences_counter, 1)
    
    def test_fill_experience_template(self):
        sentence = "At $worked_company, I was a $worked_position for $company_exp_years years."
        experience = {"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}
        result = fill_experience_template(sentence, experience)
        self.assertEqual(result, "At ABC Corp, I was a Software Engineer for 2 years.")
    
    def test_fill_cover_letter(self):
        available_templates = {
            "intro": ["I am applying for the $position at $applying_company."],
            "experience": ["I have worked at $worked_company as a $worked_position."],
            "skills": ["My skills include $skill and $skill."],
            "closing": ["Thank you for considering my application."],
            "additional_skills": ["I also know $skill."],
            "additional_experiences": ["Previously, I worked at $worked_company as a $worked_position."]
        }
        user_info = {
            "fullName": "John Doe",
            "address": "123 Main St",
            "phoneNumber": "1234567890",
            "email": "john@example.com",
            "skills": ["Python", "Java"],
            "experiences": [{"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}],
            "yearsOfExperience": 3
        }
        wanted_job_info = {"jobTitle": "Software Engineer", "companyName": "XYZ Inc"}
        cover_letter = fill_cover_letter(available_templates, user_info, wanted_job_info)
        self.assertIn("I am applying for the Software Engineer at XYZ Inc.", cover_letter)
        self.assertIn("I have worked at ABC Corp as a Software Engineer.", cover_letter)
        self.assertIn("My skills include Python and Java.", cover_letter)
        self.assertIn("Thank you for considering my application.", cover_letter)
        
    def test_fill_cover_letter_no_skills(self):
        available_templates = {
            "intro": ["I am applying for the $position at $applying_company."],
            "experience": ["I have worked at $worked_company as a $worked_position."],
            "skills": ["My skills include $skill and $skill."],
            "closing": ["Thank you for considering my application."],
            "additional_skills": ["I also know $skill."],
            "additional_experiences": ["Previously, I worked at $worked_company as a $worked_position."]
        }
        user_info = {
            "fullName": "John Doe",
            "address": "123 Main St",
            "phoneNumber": "1234567890",
            "email": "john@example.com",
            "experiences": [{"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}],
            "yearsOfExperience": 3
        }
        wanted_job_info = {"jobTitle": "Software Engineer", "companyName": "XYZ Inc"}
        
        # It should raise ValueError
        with self.assertRaises(ValueError):
            fill_cover_letter(available_templates, user_info, wanted_job_info)
    
    def test_calculate_similarity(self):
        vec1 = np.array([1, 0])
        vec2 = np.array([0, 1])
        similarity = calculate_similarity(vec1, vec2)
        self.assertEqual(similarity, 0.0)
    
    def test_calculate_similarity_with_available_titles(self):
        _, arg_sorted_similarities = calculate_similarity_with_available_titles("backend engineer")
        self.assertEqual(arg_sorted_similarities[0], 1) # 1 maps to backend engineer index in AVAILABLE_JOB_TITLES in config
    
    def test_get_similar_titles(self):
        result = get_similar_titles("backend engineer")
        # make sure that first key = backend-engineer
        self.assertEqual(list(result.keys())[0], "backend-engineer")
    
    def test_sample_titles(self):
        probabilities = {"title1": 0.5, "title2": 0.3, "title3": 0.2}
        result = sample_titles(probabilities)
        self.assertEqual(sum(result.values()), 14) # note that it floors
    
    def test_write_to_word(self):
        cover_letter = (
            "John Doe\n"
            "123 Main St\n"
            "1234567890\n"
            "john@example.com\n"
            "June 13, 2024\n"
            "Dear Hiring Manager,\n"
            "I am writing to apply for the Software Engineer position at XYZ Inc.\n"
            "I have extensive experience in Python and Java.\n"
            "Thank you for considering my application.\n"
            "Sincerely,\n"
            "John Doe."
        )
        filename = "test.docx"
        write_to_word(cover_letter, filename)
        
        # just assert that it doesn't throw error
        
    def test_generate_cover_letter_data(self):
        user_info = {
            "fullName": "John Doe",
            "address": "fasf",
            "phoneNumber": "545",
            "email": "moasmfas",
            "experiences": [{"companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2}],
            "skills": ["Python", "Java"],
            "yearsOfExperience": 2
        }
        wanted_job_info = {"jobTitle": "backend engineer", "companyName": "XYZ Inc"}
        filled_cover_letter, filename = generate_cover_letter_data(user_info, wanted_job_info)
        
        self.assertIn("John Doe", filled_cover_letter)
        self.assertTrue(filename.startswith('api/generated-coverletters/John-Doe-'))
        
    def test_generate_cover_letter_data_no_templates(self):
        user_info = {
            "fullName": "John Doe",
            "address": "fasf",
            "phoneNumber": "545",
            "email": "moasmfas",
            "experiences": [
                {
                    "companyName": "ABC Corp", "jobTitle": "Software Engineer", "companyExperienceYears": 2
                },
                {
                    "companyName": "JWT", "jobTitle": "Software Engineer", "companyExperienceYears": 3
                }
            ],
            "skills": ["Python", "Java", "C++", "Javascript", "Go", "R"],
            "yearsOfExperience": 2
        }
        wanted_job_info = {"jobTitle": "43248797@$#$", "companyName": "XYZ Inc"}
        filled_cover_letter, filename = generate_cover_letter_data(user_info, wanted_job_info)
        
        self.assertIn("John Doe", filled_cover_letter)
        print("filename")
        print(filename)
        self.assertTrue(filename.startswith('api/generated-coverletters/John-Doe-'))

    def test_preprocess_user_info(self):
        user_info = {
            "experiences": [
                {"startDate": "2019-01-01", "endDate": "2019-12-30"},
                {"startDate": "2017-01-01", "endDate": "2018-12-30"},
            ]
        }
        preprocess_user_info(user_info)
        
        self.assertEqual(len(user_info["experiences"]), 2)
        
        self.assertEqual(user_info["experiences"][0]["companyExperienceYears"], 1)  # 2019-2020
        self.assertEqual(user_info["experiences"][1]["companyExperienceYears"], 2)  # 2017-2019
        
        # Check sorting by startDate descending
        self.assertEqual(user_info["experiences"][0]["startDate"], "2019-01-01")
        self.assertEqual(user_info["experiences"][1]["startDate"], "2017-01-01")

    @patch('api.helpers.helper.requests')
    def test_upload_file(self, requests_mock):
        file_path = "api/tests/test_files/test.docx"
        upload_url = "http://example.com/api/v1/uploader/upload"
        response_mock = MagicMock()
        response_mock.json.return_value = {"link": upload_url}
        requests_mock.request.return_value = response_mock

        uploaded_link = upload_file(file_path)

        requests_mock.request.assert_called_once()
        self.assertEqual(uploaded_link, upload_url)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(HelpersTest))