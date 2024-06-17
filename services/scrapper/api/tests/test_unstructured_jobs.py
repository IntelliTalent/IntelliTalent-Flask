from datetime import datetime
import unittest
from unittest.mock import MagicMock
from api.unstructured_jobs.unstructured_jobs_service import (
    insert_jobs,
)

class UnstructuredJobsTest(unittest.TestCase):

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
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(UnstructuredJobsTest))