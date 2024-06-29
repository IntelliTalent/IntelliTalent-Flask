import unittest, json
from unittest.mock import patch
from api.index import (
    health_check,
    get_job_info,
)

class IndexTest(unittest.TestCase):
        
    def test_health_check(self):
        self.assertEqual(health_check(), "Hello World From Job Extractor Service!")
        
    @patch('api.index.prepare_job')
    def test_get_job_info(self, prepare_job_mock):
        data = {
            "jobs": [
                {
                    "title": "Software Engineer",
                    "company": "ABC Corp",
                    "location": "City, Country",
                    "description": "Developing software applications.",
                    "startDate": "2022-01-01",
                    "endDate": "Present"
                }
            ]
        }
        
        new_job = {
            "title": "Software Engineer",
            "company": "ABC Corp",
            "location": "City, Country",
            "description": "Developing software applications.",
            "startDate": "2022-01-01",
            "endDate": "Present"
        }
        
        prepare_job_mock.return_value = new_job

        result = get_job_info(data)
        
        result = json.loads(result)

        self.assertIn("jobs", result)
        
        self.assertEqual(result["jobs"][0], new_job)
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(IndexTest))