import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup
import requests
from api.index import (
    health_check,
    scrape
)
from api.scrapped_websites.linkedin import (
    linkedin_scrape_thread,
    get_search_queries,
    remove_duplicates,
    get_with_retry,
    get_job_cards_main_info,
    get_job_description,
    get_job_cards,
    check_closed_class,
    linkedin_check_active_jobs,
)

class IndexTest(unittest.TestCase):
        
    def test_health_check(self):
        self.assertEqual(health_check(), "Hello World From Scrapper Service!")
        
    def test_get_search_queries(self):
        # assert that the function returns a list and its length is 27 (JOBS_TITLES len) * 22 (JOB_LOCATIONS len) * 3 (JOBS_PLACES len)
        self.assertIsInstance(get_search_queries(), list)
        self.assertEqual(len(get_search_queries()), 27 * 22 * 3)
        
    def test_remove_duplicates(self):
        # assert that the function removes duplicates based on the title and company
        joblist = [
            {"title": "title 1", "company": "company 1"},
            {"title": "title 1", "company": "company 1"},
            {"title": "title 2", "company": "company 2"},
        ]
        self.assertEqual(remove_duplicates(joblist), [
            {"title": "title 1", "company": "company 1"},
            {"title": "title 2", "company": "company 2"},
        ])
        
    @patch('api.scrapped_websites.linkedin.get_job_cards')
    @patch('api.scrapped_websites.linkedin.get_with_retry')
    @patch('api.scrapped_websites.linkedin.get_job_description')
    @patch('api.scrapped_websites.linkedin.insert_jobs')
    @patch('api.scrapped_websites.linkedin.logger')
    @patch('api.scrapped_websites.linkedin.tm.perf_counter')
    def test_linkedin_scrape_thread(self, mock_perf_counter, mock_logger, mock_insert_jobs, mock_get_job_description, mock_get_with_retry, mock_get_job_cards):
        mock_get_job_cards.return_value = [
            {
                "jobId": 1,
                "title": "title 1",
                "company": "company 1",
                "jobLocation": "location 1",
                "publishedAt": "2021-01-01",
                "url": "url 1",
                "jobPlace": "On Site",
            }
        ]
        mock_get_with_retry.return_value = MagicMock()
        mock_get_job_description.return_value = "Job Description"
        mock_perf_counter.side_effect = [1, 2]  # Simulate 1 second elapsed

        linkedin_scrape_thread(MagicMock())

        mock_get_job_cards.assert_called_once_with(get_search_queries())
        self.assertEqual(mock_get_with_retry.call_count, len(mock_get_job_cards.return_value))
        mock_insert_jobs.assert_called_once()
        mock_logger.info.assert_called_with("Scraping LinkedIn finished in 1.00 seconds")
        
    @patch('api.scrapped_websites.linkedin.get_job_cards')
    @patch('api.scrapped_websites.linkedin.get_with_retry')
    @patch('api.scrapped_websites.linkedin.get_job_description')
    @patch('api.scrapped_websites.linkedin.insert_jobs')
    @patch('api.scrapped_websites.linkedin.logger')
    @patch('api.scrapped_websites.linkedin.tm.perf_counter')
    def test_linkedin_scrape_thread_no_jobs(self, mock_perf_counter, mock_logger, mock_insert_jobs, mock_get_job_description, mock_get_with_retry, mock_get_job_cards):
        mock_get_job_cards.return_value = []
        mock_get_with_retry.return_value = MagicMock()
        mock_get_job_description.return_value = "Job Description"
        mock_perf_counter.side_effect = [1, 2]  # simulate 1 second elapsed

        linkedin_scrape_thread(MagicMock())

        mock_get_job_cards.assert_called_once_with(get_search_queries())
        self.assertEqual(mock_get_with_retry.call_count, len(mock_get_job_cards.return_value))
        mock_logger.info.assert_called_with("Scraping LinkedIn finished in 1.00 seconds")
        
    @patch('api.index._thread.start_new_thread')
    def test_scrape(self, mock_start_new_thread):
        scrape(MagicMock())
        
        self.assertEqual(mock_start_new_thread.call_count, 2)
    
    @patch('api.scrapped_websites.linkedin.requests.get')
    def test_get_with_retry(self, mock_requests_get):
        mock_requests_get.return_value = MagicMock()
        mock_requests_get.return_value.content = "content"
        
        result = get_with_retry("url")
        
        self.assertEqual(result, BeautifulSoup("content", "html.parser"))
        self.assertEqual(mock_requests_get.call_count, 1)
        
    @patch('api.scrapped_websites.linkedin.requests.get')
    @patch('api.scrapped_websites.linkedin.logger')
    @patch('api.scrapped_websites.linkedin.tm.sleep')
    def test_get_with_retry_timeout_and_exception(self, mock_sleep, mock_logger, mock_get):
        url = "http://example.com"
        delay = 2

        mock_get.side_effect = [requests.exceptions.Timeout(), Exception("Generic error")]

        result = get_with_retry(url)

        self.assertIsNone(result)

        mock_sleep.assert_called_with(delay)

        mock_logger.debug.assert_called_with(f"Timeout occurred for URL: {url}, retrying in {delay}s...")
        mock_logger.error.assert_called_with(f"An error occurred while retrieving the URL: {url}")
        mock_logger.exception.assert_called()
        
    def test_jon_cards_main_info_empty(self):
        soup = BeautifulSoup("", 'html.parser')
        place = "Remote"
        expected_result = []
        result = get_job_cards_main_info(soup, place)
        self.assertEqual(result, expected_result)
        
    @patch('api.scrapped_websites.linkedin.logger')
    def test_get_job_description_success(self, mock_logger):
        HTML_CONTENT = """
        <div class="description__text description__text--rich">
            <span>Unwanted span</span>
            <a href="#">Unwanted link</a>
            <ul>
                <li>Point one</li>
                <li>Point two</li>
            </ul>
            <p>End of description. Show less</p>
        </div>
        """
        soup = BeautifulSoup(HTML_CONTENT, 'html.parser')
        expected_description = "- Point one\n- Point two\nEnd of description. "
        self.assertEqual(get_job_description(soup), expected_description)
        mock_logger.error.assert_not_called()

    @patch('api.scrapped_websites.linkedin.logger')
    def test_get_job_description_failure(self, mock_logger):
        HTML_CONTENT = "<div class='wrong_class'>No job description here.</div>"
        soup = BeautifulSoup(HTML_CONTENT, 'html.parser')
        self.assertEqual(get_job_description(soup), "Could not find Job Description")
        mock_logger.error.assert_called_once_with("(LinkedIn) Could not find Job Description, retrying...")
        
    @patch('api.scrapped_websites.linkedin.get_with_retry')
    @patch('api.scrapped_websites.linkedin.get_job_cards_main_info')
    @patch('api.scrapped_websites.linkedin.remove_duplicates')
    @patch('api.scrapped_websites.linkedin.logger')
    def test_get_job_cards(self, mock_logger, mock_remove_duplicates, mock_get_job_cards_main_info, mock_get_with_retry):
        search_queries = [
            {"keywords": "Software Engineer", "location": "New York", "place": "2"},
            {"keywords": "Data Scientist", "location": "San Francisco", "place": "2"}
        ]
        rounds = 1
        pages_to_scrape = 1
        mock_get_with_retry.return_value = MagicMock()
        mock_get_job_cards_main_info.return_value = [{'id': 1, 'title': 'Software Engineer'}]
        mock_remove_duplicates.return_value = [{'id': 1, 'title': 'Software Engineer'}]

        result = get_job_cards(search_queries, rounds, pages_to_scrape)
        self.assertEqual(len(result), 1)
        mock_remove_duplicates.assert_called_once()
        mock_logger.debug.assert_called()
        
    @patch('api.scrapped_websites.linkedin.get_with_retry')
    @patch('api.scrapped_websites.linkedin.get_job_cards_main_info')
    @patch('api.scrapped_websites.linkedin.remove_duplicates')
    @patch('api.scrapped_websites.linkedin.logger')
    def test_get_job_cards_no_jobs(self, mock_logger, mock_remove_duplicates, mock_get_job_cards_main_info, mock_get_with_retry):
        search_queries = [
            {"keywords": "Software Engineer", "location": "New York", "place": "2"},
            {"keywords": "Data Scientist", "location": "San Francisco", "place": "2"}
        ]
        rounds = 1
        pages_to_scrape = 1
        mock_get_with_retry.return_value = MagicMock()
        mock_get_job_cards_main_info.return_value = []
        mock_remove_duplicates.return_value = []

        result = get_job_cards(search_queries, rounds, pages_to_scrape)
        self.assertEqual(len(result), 0)
        mock_remove_duplicates.assert_called_once()
        mock_logger.debug.assert_called()
        
    def test_job_open(self):
        HTML_CONTENT = "<div><h1>Job Title</h1><p>Job Description</p></div>"
        soup = BeautifulSoup(HTML_CONTENT, 'html.parser')
        self.assertTrue(check_closed_class(soup))

    def test_job_closed(self):
        HTML_CONTENT = "<div class='closed-job'><h1>Job Title</h1><p>This job is closed.</p></div>"
        soup = BeautifulSoup(HTML_CONTENT, 'html.parser')
        self.assertFalse(check_closed_class(soup))
        
    @patch('api.scrapped_websites.linkedin.get_with_retry')
    @patch('api.scrapped_websites.linkedin.check_closed_class')
    def test_linkedin_check_active_jobs(self, mock_check_closed_class, mock_get_with_retry):
        jobs = [
            {"url": "http://example.com/job1", "jobId": "1"},
            {"url": "http://example.com/job2", "jobId": "2"},
            {"url": "http://example.com/job3", "jobId": "3"}
        ]
        
        mock_get_with_retry.side_effect = [MagicMock(), None, MagicMock()]
        mock_check_closed_class.side_effect = [True, False]
        
        expected_jobs = [
            {"isActive": True},
            {"isActive": False},
            {"isActive": False}
        ]
        
        result = linkedin_check_active_jobs(jobs)
        
        self.assertEqual(result, expected_jobs)
        mock_get_with_retry.assert_called()
        mock_check_closed_class.assert_called()

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(IndexTest))