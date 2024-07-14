import unittest
from unittest.mock import MagicMock, patch
from api.scrapped_websites.wuzzuf import (
    get_search_queries,
    get_jobs_details,
    get_jobs,
    wuzzuf_scrape_thread,
    is_expired,
    wuzzuf_check_active_jobs,
)
from instance import config

class WuzzufTest(unittest.TestCase):
        
    def test_get_search_queries(self):
        # assert that the function returns a list and its length is 27 (JOBS_TITLES len) * 22 (JOB_LOCATIONS len)
        self.assertIsInstance(get_search_queries(), list)
        self.assertEqual(len(get_search_queries()), len(config.JOB_TITLES) * len(config.JOB_LOCATIONS))
        
    @patch('api.scrapped_websites.wuzzuf.requests.get')
    def test_get_jobs_details(self, mock_get):
        mock_response_data = {
            "data": [
                {
                    "id": "123",
                    "attributes": {
                        "title": "Software Engineer",
                        "description": "<p>Exciting software engineering opportunity</p>",
                        "requirements": "<p>Strong Python skills</p>",
                        "postedAt": "01/01/2023 00:00:00",
                        "location": {
                            "country": {
                                "name": "Egypt"
                            }
                        },
                        "uri": "jobs/software-engineer",
                        "workTypes": [
                            {
                                "displayedName": "Full-time"
                            }
                        ],
                        "keywords": [
                            {
                                "name": "Python"
                            },
                            {
                                "name": "Django"
                            }
                        ],
                        "workplaceArrangement": {
                            "displayedName": "On-site"
                        },
                        "workExperienceYears": {
                            "min": 2
                        },
                        "candidatePreferences": {
                            "educationLevel": {
                                "name": "Bachelor's"
                            }
                        }
                    }
                }
            ]
        }

        mock_get.return_value.json.return_value = mock_response_data

        jobs_input = [
            {
                "id": "123",
                "attributes": {
                    "computedFields": [
                        {
                            "name": "company_name",
                            "value": ["Tech Corp"]
                        }
                    ]
                }
            }
        ]

        expected_output = [
            {
                "jobId": "123",
                "title": "Software Engineer",
                "company": "Tech Corp",
                "description": "Exciting software engineering opportunity\nStrong Python skills",
                "jobLocation": "Egypt",
                "publishedAt": "2023-01-01",
                "url": "https://wuzzuf.net/jobs/software-engineer",
                "type": "Other",
                "skills": ["Python", "Django"],
                "jobPlace": "On Site",
                "neededExperience": 2,
                "education": "Bachelor's",
            }
        ]

        result = get_jobs_details(jobs_input)

        self.assertEqual(result, expected_output)
        
    @patch('api.scrapped_websites.wuzzuf.get_jobs_details')
    @patch('api.scrapped_websites.wuzzuf.requests.post')
    def test_get_jobs(self, mock_post, mock_get_jobs_details):
        mock_response_data = {
            "data": [
                {
                    "id": "123",
                    "attributes": {
                        "title": "Software Engineer",
                        "description": "Exciting software engineering opportunity",
                        "postedAt": "01/01/2023",
                        "location": {
                            "country": {
                                "name": "Egypt"
                            }
                        },
                        "uri": "jobs/software-engineer",
                        "keywords": [
                            {
                                "name": "Python"
                            }
                        ]
                    }
                }
            ]
        }

        # Mock the JSON response
        mock_post.return_value.json.return_value = mock_response_data

        # Mock the get_jobs_details function to return a simplified job detail
        mock_get_jobs_details.return_value = [
            {
                "jobId": "123",
                "title": "Software Engineer",
                "description": "Exciting software engineering opportunity",
                "jobLocation": "Egypt",
                "publishedAt": "2023-01-01",
                "url": "https://wuzzuf.net/jobs/software-engineer",
                "skills": ["Python"]
            }
        ]

        search_queries = [
            {
                "title": "Software Engineer",
                "location": "Egypt"
            }
        ]

        expected_output = [
            {
                "jobId": "123",
                "title": "Software Engineer",
                "description": "Exciting software engineering opportunity",
                "jobLocation": "Egypt",
                "publishedAt": "2023-01-01",
                "url": "https://wuzzuf.net/jobs/software-engineer",
                "skills": ["Python"]
            }
        ]

        result = get_jobs(search_queries, 1)

        self.assertEqual(result, expected_output)
        
    @patch('api.scrapped_websites.wuzzuf.get_search_queries')
    @patch('api.scrapped_websites.wuzzuf.get_jobs')
    @patch('api.scrapped_websites.wuzzuf.insert_jobs')
    @patch('api.scrapped_websites.wuzzuf.logger')
    @patch('api.scrapped_websites.wuzzuf.tm.perf_counter')
    def test_wuzzuf_scrape_thread(self, mock_perf_counter, mock_logger, mock_insert_jobs, mock_get_jobs, mock_get_search_queries):
        mock_get_search_queries.return_value = [{"title": "Software Engineer", "location": "Egypt"}]
        mock_get_jobs.return_value = [
            {
                "jobId": "123",
                "title": "Software Engineer",
                "description": "Exciting software engineering opportunity",
                "jobLocation": "Egypt",
                "publishedAt": "2023-01-01",
                "url": "https://wuzzuf.net/jobs/software-engineer",
                "skills": ["Python"]
            }
        ]

        unstructured_jobs_db = MagicMock()
        
        mock_perf_counter.side_effect = [1, 2]  # simulate 1 second elapsed

        wuzzuf_scrape_thread(unstructured_jobs_db)

        mock_get_search_queries.assert_called_once()
        mock_get_jobs.assert_called_once_with(mock_get_search_queries.return_value)
        mock_insert_jobs.assert_called_once_with(unstructured_jobs_db, mock_get_jobs.return_value)
        mock_logger.debug.assert_called_with("(Wuzzuf) Total job cards scraped: 1")
        mock_logger.info.assert_called_with("Scraping Wuzzuf finished in 1.00 seconds")
        mock_logger.info.assert_called()
        
    def test_is_expired_expired(self):
        self.assertTrue(is_expired("12/31/2020 11:59:59"))
        
    def test_is_expired_not_expired(self):
        self.assertFalse(is_expired("01/01/2050 00:00:00"))

    @patch('api.scrapped_websites.wuzzuf.requests.get')
    def test_wuzzuf_check_active_jobs(self, mock_get):
        jobs = [
            {"jobId": "1", "url": "http://example.com/job/1"},
            {"jobId": "2", "url": "http://example.com/job/2"}
        ]
        job_details = {
            "data": [
                {"id": "1", "attributes": {"expireAt": "01/01/2050 00:00:00"}},
                {"id": "2", "attributes": {"expireAt": "12/31/2020 11:59:59"}}
            ]
        }
        mock_get.return_value.json.return_value = job_details

        updated_jobs = wuzzuf_check_active_jobs(jobs)

        self.assertTrue(updated_jobs[0]["isActive"])
        self.assertFalse(updated_jobs[1]["isActive"])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(WuzzufTest))