import unittest, json
from unittest.mock import patch
from api.index import (
    health_check,
    generate_CV,
)

class IndexTest(unittest.TestCase):
        
    def test_health_check(self):
        self.assertEqual(health_check(), "Hello World From CV Generator Service!")
        
    @patch('api.index.logger')
    @patch('api.index.upload_file')
    def test_generate_CV(self, upload_file_mock, logger_mock):
        data = {
            "profile": {
                "fullName": "John Doe",
                "phoneNumber": "1234567890",
                "email": "john@example.com",
                "gitHub": "https://github.com/johndoe",
                "linkedIn": "https://linkedin.com/in/johndoe",
                "city": "City",
                "country": "Country",
                "summary": "Seeking a challenging position in software development.",
                "educations": [
                    {
                        "schoolName": "University of ABC",
                        "degree": "Bachelor of Science in Computer Science",
                        "startDate": "2020-09-01",
                        "endDate": "2024-05-01",
                        "description": "Studied various computer science subjects."
                    }
                ],
                "experiences": [
                    {
                        "jobTitle": "Software Engineer",
                        "companyName": "XYZ Corp",
                        "startDate": "2022-01-01",
                        "endDate": "Present",
                        "description": "Developing software applications."
                    }
                ],
                "projects": [
                    {
                        "name": "Project A",
                        "description": "Developed a web application using Django.",
                        "skills": ["Python", "Django"]
                    }
                ],
                "languages": ["English", "Spanish"],
                "skills": ["Python", "Java", "JavaScript"],
                "certificates": [
                    {
                        "title": "Certificate in Python Programming",
                        "authority": "XYZ Institute",
                        "issuedAt": "2023-03-15",
                        "validUntil": "2024-03-15",
                        "url": "https://example.com/certificate"
                    }
                ]
            }
        }
        
        link = "http://example.com/uploaded_file.docx"

        # Mocking the upload_file function to return a dummy link
        upload_file_mock.return_value = link

        # Calling the function
        result = generate_CV(data)
        
        result = json.loads(result)

        # Assertions
        logger_mock.info.assert_called_once_with("Generating CV")

        # Check if the function returns a JSON string containing the word link
        self.assertIn("word", result)
        
        # Check if the returned link == the mocked link
        self.assertEqual(result["word"], link)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(IndexTest))