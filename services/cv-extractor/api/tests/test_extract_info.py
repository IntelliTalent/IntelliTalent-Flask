import unittest
from unittest.mock import patch
from datetime import datetime
from api.extract_info.extract_text import (
    remove_empty_lines,
    extract_text_from_pdf,
    extract_sections,
)
from api.extract_info.extract_skills import (
    extract_skills_parallel,
    extract_skills,
    extract_project_skills,
)
from api.extract_info.extract_experience import (
    parse_date,
    calculate_years_of_experience,
    extract_years_of_experience,
)
from api.extract_info.extract_main_info import (
    extract_name,
    extract_email,
    extract_education,
    extract_languages,
)
from api.extract_info.extract_info import (
    extract_info,
)

class ExtractInfoTest(unittest.TestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.cv_text = "Moaz Mohamed Hassan\nEmail Address: moaz25jan2015@gmail.com\nPhone: +201070495321, +201550865053\nAddress: Giza, Egypt.\nGitHub: GitHub, LinkedIn: LinkedIn\nEducation\nBachelor's of Computer Engineering, Faculty of Engineering, Cairo University, Giza, Egypt\n2019-2024\nAccumulative GPA: 3.5\nExperience\nAppgain.io, Cairo, Egypt\nBackend Developer (June 2023 – Till now)\n Created 2 backend applications (microservices) to communicate with other microservices in\nthe system in Agile environment.\n One of them is a public Shopify app to be installed on clients stores and integrated with\nour database and dashboard.\n Other one is a push sender to effectively send push notifications(app push and web push)\nto many users using asynchronous calls and batches to fasten the sending process to FCM\nand APN, this service enhanced sending process time to about 100000 users by more than\n90%.\n Implemented independent tasks to fix issues or add features in other microservices and\nother products as it is a product company.\n Integration with the frontend team, and creating API documentation using Postman.\n Technologies: Flask, Node.js, Express.js, Next.js, MongoDB, PM2, Docker, gitlab,\nPostman, and Jira.\nSafecotech Solutions, Cairo, Egypt\nBackend Developer (July 2022 – March 2023)\n Created 55 API endpoints in the backend applications of a website for IT ticket\nsubmission and resolution, and deployed it using Heroku, and a website for a client called\nDigitize.\n Direct client communication experience required to analyze and implement the client's\nrequirements.\n Worked in an agile environment, created API documentation, and collaborated with the\nfrontend team.\n Technologies: Node.js, Express.js, MongoDB, Postman, and Heroku.\nMostaqel Freelancing Website\nBackend Developer (July 2021 – October 2021)\n Created the backend application of 2 websites with Django framework, and deployed them\nwith Heroku.\n Direct client communication for website requirements analysis and project planning .\n Technologies: Django, PostgreSQL, SQLite, and Heroku.\nPage 1 of 2\nSkills\nLanguages\nJavaScript, TypeScript, C++, Python, Java, C#, C.\nFrameworks\nDatabases\nOthers\nProjects\nNode.js, Express.js, Nest.js, Flask, Django, PyTorch.\nMongoDB, MySQL, PostgreSQL, MS SQL Server, SQLite\nHTML & CSS, Git, Docker, CircleCI, AWS, Arduino,\nMatlab.\nProjects\nRedditX Clone – Cairo University\n It is a MERN website to make a Reddit clone that was implemented for the Software\nEngineering Course by a team of 19 students, distributed into multiple small teams,\nBackend, Frontend, Cross-Platform, DevOps, and Testing teams.\n Created 31 API endpoints in the backend application.\n Created seeds and scripts to quickly drop and insert the seeds.\n Implemented end-to-end tests, unit tests and created API documentation using Swagger.\n Worked in an agile environment with weekly sprints and periodic meetings to refine sprint\nrequirements.\n Created function documentation using Jsdoc.\nTechnologies:\n Node.js, Express.js, MongoDB, Supertest, Jest, Swagger, Postman, Jsdoc, Nodemailer, and\nPug templates.\nDetails:\n GitHub Repository\nArabic Text Diacritization– Cairo University\n An NLP project that accurately restores diacritics of Arabic language sentences.\n We use characters level embedding with Bi-LSTM as the model network.\n We trained the model on 50K text lines, achieving 97.78% accuracy on the test set as an\naverage.\nTechnologies:\n Python, PyTorch, and Jupyter Notebook.\nDetails:\n GitHub Repository\nHand Gesture Recognition – Cairo University\n A machine learning-based project that accurately recognizes and interprets hand gestures\n(from 0 to 5).\n We used HOG for feature extraction, and SVM f or classification.\n This project has potential applications in robotics, healthcare, and gaming, offering a new\nway to interact with machines.\nTechnologies:\n Python, Jupyter Notebook, and OpenCV.\nDetails:\nGitHub Repository\nCertificates\n Advanced Cloud DevOps Course by Udacity, Certificate\n 2nd place in the 6th Undergraduate Engineering Mathematics Research Forum, Certificate\n Certificate of Completion - Safecotech Software Engineer Internship Program, Certificate\nExtra-curricular Activities\n Scouts Leader of my college Rovers Clan from 2019 to 2021.\n Member of my college Student Union from 2019 to 2020.\nPage 2 of 2"
    
    def test_remove_empty_lines(self):
        text = "Hello\n\nWorld"
        result = remove_empty_lines(text)
        self.assertEqual(result, "Hello\nWorld")
        
    def test_extract_text_from_pdf(self):
        filename = "api/tests/test_files/Moaz Mohamed Hassan CV.pdf"
        
        result = extract_text_from_pdf(filename)
        
        self.assertIn("Moaz Mohamed", result)
        self.assertIn("Backend Developer", result)
        
    def test_extract_sections(self):
        result = extract_sections(self.cv_text)
        
        self.assertIn("personal", result)
        self.assertIn("education", result)
        self.assertIn("experience", result)
        
        self.assertIn("Moaz Mohamed", result["personal"])
        self.assertIn("Bachelor's of Computer Engineering", result["education"])
        self.assertIn("Backend Developer", result["experience"])
        
    def test_extract_skills_parallel(self):
        words_list = ["skills", "Python", "Java", "C++"]
        result = extract_skills_parallel(words_list, similarity_threshold=0.9, num_threads=2)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C++", result)
        
    def test_extract_skills(self):
        text = "I've skills of Python, Java, C/C++"
        result = extract_skills(text, similarity_threshold=0.9)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C", result)
        self.assertIn("C++", result)
        
    def test_extract_project_skills(self):
        text = "I worked with Python, Java, C/C++, in this project\n I used Python, Java in this project"
        
        result = extract_project_skills(text)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C", result)
        self.assertIn("C++", result)
        self.assertEqual(result["Python"], 2)
        self.assertEqual(result["Java"], 2)
        self.assertEqual(result["C"], 1)
        self.assertEqual(result["C++"], 1)
        
    def test_parse_date(self):
        date_str = "June 2023"
        result = parse_date(date_str)
        
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.month, 6)
        
        date_str = "2023"
        result = parse_date(date_str)
        
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.month, 1)
        
        date_str = "Present"
        current_year = datetime.now().year
        result = parse_date(date_str)
        
        self.assertEqual(result.year, current_year)
        
        date_str = "invalid"
        result = parse_date(date_str)
        
        self.assertEqual(result, None)
        
    def test_calculate_years_of_experience(self):
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 1, 1)
        
        result = calculate_years_of_experience(start_date, end_date)
        
        self.assertEqual(result, 3)
        
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 1, 1)
        
        result = calculate_years_of_experience(start_date, end_date)
        
        self.assertEqual(result, 0)
        

    def test_extract_years_of_experience(self):
        text = "Backend Developer (June 2020 – June 2023)"
        
        result = extract_years_of_experience(text)
        
        self.assertEqual(result, 3)
        
        text = "Backend Developer (January 2020 – Present)"
        
        current_year = datetime.now().year
        
        result = extract_years_of_experience(text)
        
        self.assertEqual(int(result), int(current_year - 2020))
        
    def test_extract_name(self):
        text = "Moaz Mohamed\nEmail Address:..."

        result = extract_name(text)
        
        self.assertEqual(result, "Moaz Mohamed")
        
    def test_extract_email(self):
        text = "Moaz Mohamed\nEmail Address: moaz@gmail.com"
        
        result = extract_email(text)
        
        self.assertEqual(result, "moaz@gmail.com")
        
    def test_extract_education(self):
        text = "Education:\nBachelor's of Computer Engineering, Faculty of Engineering, Cairo University"
        result = extract_education(text)
        
        self.assertIn("Bachelor's of Computer Engineering", result)
        
    def test_extract_languages(self):
        text = "Languages:\nEnglish, Arabic"
        
        result = extract_languages(text)
        
        self.assertIn("English", result)
        self.assertIn("Arabic", result)
        
    @patch("api.extract_info.extract_info.extract_text_from_pdf")
    @patch("api.extract_info.extract_info.extract_sections")
    @patch("api.extract_info.extract_info.extract_skills")
    @patch("api.extract_info.extract_info.extract_project_skills")
    @patch("api.extract_info.extract_info.extract_years_of_experience")
    @patch("api.extract_info.extract_info.extract_name")
    @patch("api.extract_info.extract_info.extract_email")
    @patch("api.extract_info.extract_info.extract_education")
    @patch("api.extract_info.extract_info.extract_languages")
    def test_extract_info(self, mock_extract_languages, mock_extract_education, mock_extract_email, mock_extract_name, mock_extract_years_of_experience, mock_extract_project_skills, mock_extract_skills, mock_extract_sections, mock_extract_text_from_pdf):
        filename = "api/tests/test_files/Moaz Mohamed Hassan CV.pdf"
        
        mock_extract_text_from_pdf.return_value = self.cv_text
        mock_extract_sections.return_value = {
            "personal": "Moaz Mohamed",
            "education": "Bachelor's of Computer Engineering",
            "experience": "Backend Developer",
            "skills": "Python, Java, C++",
            "project": "Reddit's Clone\n Python, Java, C++",
            "summary": "I'm a backend developer with 3 years of experience in Python, Java, C++",
            "language": "English, Arabic",
            "certification": "Advanced Cloud DevOps Course by Udacity\n2nd place in the 6th Undergraduate Engineering Mathematics Research Forum\nCertificate of Completion - Safecotech Software Engineer Internship Program\n",
        }
        mock_extract_skills.return_value = ["Python", "Java", "C++"]
        mock_extract_project_skills.return_value = {
            "Python": 2,
            "Java": 1,
            "C++": 1
        }
        mock_extract_years_of_experience.return_value = 3
        mock_extract_name.return_value = "Moaz Mohamed"
        mock_extract_email.return_value = "moaz@gmail.com"
        mock_extract_education.return_value = ["Bachelor's of Computer Engineering"]
        mock_extract_languages.return_value = ["English", "Arabic"]
        
        result = extract_info(filename)
        
        self.assertIn("Python", result["skills"])
        self.assertIn("Java", result["skills"])
        self.assertIn("C++", result["skills"])
        self.assertIn("Python", result["projectSkills"])
        self.assertIn("Java", result["projectSkills"])
        self.assertIn("C++", result["projectSkills"])
        self.assertEqual(result["yearsOfExperience"], 3)
        self.assertEqual(result["name"], "Moaz Mohamed")
        self.assertEqual(result["email"], "moaz@gmail.com")
        self.assertIn("Bachelor's of Computer Engineering", result["education"])
        self.assertIn("English", result["languages"])
        self.assertIn("Arabic", result["languages"])
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(ExtractInfoTest))