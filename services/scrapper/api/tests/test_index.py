from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
from api.index import (
    health_check,
    scrape,
    check_active_jobs,
)
from api.unstructured_jobs.unstructured_jobs_service import (
    insert_jobs,
)
import json

class IndexTest(unittest.TestCase):
        
    def test_health_check(self):
        self.assertEqual(health_check(), "Hello World From Scrapper Service!")
            
    @patch('api.index._thread.start_new_thread')
    def test_scrape(self, mock_start_new_thread):
        scrape(MagicMock())
        
        self.assertEqual(mock_start_new_thread.call_count, 2)
        
    def test_no_jobs_found(self):
        result = check_active_jobs({"jobs": []})
        self.assertEqual(result, '{"jobs": []}')

    def test_no_linkedin_or_wuzzuf_jobs(self):
        jobs = [{"url": "https://example.com/job1"}, {"url": "https://example.com/job2"}]
        result = check_active_jobs({"jobs": jobs})
        self.assertEqual(result, '{"jobs": []}')

    @patch('api.index.linkedin_check_active_jobs')
    @patch('api.index.wuzzuf_check_active_jobs')
    def test_linkedin_jobs_present(self, mock_wuzzuf_check, mock_linkedin_check):
        jobs = [{"url": "https://linkedin.com/job1"}]
        
        mocked_jobs = [{"url": "https://linkedin.com/job1", "isActive": True}]
        mock_linkedin_check.return_value = mocked_jobs
        mock_wuzzuf_check.return_value = []
        result = check_active_jobs({"jobs": jobs})
        result = json.loads(result)
        self.assertEqual(result["jobs"][0]["isActive"], True)

    @patch('api.index.linkedin_check_active_jobs')
    @patch('api.index.wuzzuf_check_active_jobs')
    def test_wuzzuf_jobs_present(self, mock_wuzzuf_check, mock_linkedin_check):
        jobs = [{"id": 1, "url": "https://wuzzuf.net/job1"}]
        
        mocked_jobs = [{"id": 1, "url": "https://wuzzuf.net/job1", "isActive": True}]
        mock_linkedin_check.return_value = []
        mock_wuzzuf_check.return_value = mocked_jobs
        result = check_active_jobs({"jobs": jobs})
        result = json.loads(result)
        self.assertEqual(result["jobs"][0]["isActive"], True)

    @patch('api.index.linkedin_check_active_jobs')
    @patch('api.index.wuzzuf_check_active_jobs')
    def test_both_linkedin_and_wuzzuf_jobs_present(self, mock_wuzzuf_check, mock_linkedin_check):
        jobs = [{"url": "https://linkedin.com/job1"}, {"id": 1, "url": "https://wuzzuf.net/job2"}]
        mock_linkedin_check.return_value = [{"url": "https://linkedin.com/job1", "isActive": True}]
        mock_wuzzuf_check.return_value = [{"id": 1, "url": "https://wuzzuf.net/job2", "isActive": True}]
        result = check_active_jobs({"jobs": jobs})
        result = json.loads(result)
        self.assertEqual(result["jobs"][0]["isActive"], True)
        self.assertEqual(result["jobs"][1]["isActive"], True)

    def test_insert_jobs_adds_scrappedAt_and_inserts(self):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        jobs = [
            {"title": "Software Engineer", "company": "Tech Co"},
            {"title": "Data Scientist", "company": "Data Co"}
        ]
        insert_jobs(mock_db, jobs)

        for job in jobs:
            self.assertIn("scrappedAt", job)
            self.assertIsInstance(job["scrappedAt"], datetime)

        mock_collection.insert_many.assert_called_once_with(jobs, ordered=False)

    def test_insert_jobs_handles_exception(self):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        jobs = [
            {"title": "Software Engineer", "company": "Tech Co"},
            {"title": "Data Scientist", "company": "Data Co"}
        ]
        
        mock_collection.insert_many.side_effect = Exception("Duplicate key error")

        # this should not raise exception
        insert_jobs(mock_db, jobs)

        mock_collection.insert_many.assert_called()

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(IndexTest))