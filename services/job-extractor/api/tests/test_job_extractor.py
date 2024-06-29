import unittest
from api.job_extractor.job_extractor import (
    SIMILARITY_THRESHOLD,
    remove_stopwords,
    extract_skills_parallel,
    extract_skills,
    handle_current_skills,
    extract_years_of_experience,
    extract_education_level,
    extract_is_computer_science,
    prepare_job,
)

class JobExtractorTest(unittest.TestCase):

    def test_remove_stopwords(self):
        text = "This is a test sentence."
        result = remove_stopwords(text)
        self.assertEqual(result, "test sentence .")
    
    def test_extract_skills_parallel(self):
        words_list = ["Required", "skills", "include", "Python", "Java", "C++"]
        result = extract_skills_parallel(words_list, similarity_threshold=SIMILARITY_THRESHOLD, num_threads=2)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C++", result)
        
    def test_extract_skills(self):
        text = "Required skills include Python, Java, C/C++"
        result = extract_skills(text, similarity_threshold=SIMILARITY_THRESHOLD)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C", result)
        self.assertIn("C++", result)

    def test_handle_current_skills(self):
        current_skills = ["Python", "Java", "C++", "NotSkill"]
        result = handle_current_skills(current_skills, similarity_threshold=SIMILARITY_THRESHOLD)
        
        self.assertIn("Python", result)
        self.assertIn("Java", result)
        self.assertIn("C++", result)
        
    def test_extract_years_of_experience(self):
        text = "Min 5 years of experience required\n Max years of experience is 10."
        result = extract_years_of_experience(text)
        
        self.assertEqual(result, (5, 10))
        
    def test_extract_education_level(self):
        text = "Bachelor's degree in Computer Science or related field required."
        result = extract_education_level(text)
        
        self.assertEqual(result, "Bachelor's")
        
    def test_extract_education_level_PhD(self):
        text = "PhD degree in Computer Science or related field required."
        result = extract_education_level(text)
        
        self.assertEqual(result, "PhD")
        
    def test_extract_education_level_Masters(self):
        text = "Master's degree in Computer Science or related field required."
        result = extract_education_level(text)
        
        self.assertEqual(result, "Master's")
    
    def test_extract_is_computer_science(self):
        text = "Bachelor's degree in Computer Science or related field required."
        result = extract_is_computer_science(text)
        
        self.assertTrue(result)
        
    def test_prepare_job(self):
        job = {
            "title": "Software Engineer",
            "description": """Required skills include Python, Java, C/C++.
        Min 5 years of experience required.
        Max years of experience is 10.
        Bachelor's degree in Computer Science or related field required.""",
            "skills": ["R"],
        }
        
        result = prepare_job(job)
        
        self.assertEqual(result["title"], "Software Engineer")
        self.assertIn("Python", result["skills"])
        self.assertIn("Java", result["skills"])
        self.assertIn("C", result["skills"])
        self.assertIn("C++", result["skills"])
        self.assertIn("R", result["skills"])
        self.assertEqual(result["neededExperience"], 5)
        self.assertEqual(result["education"], "Bachelor's")
        self.assertTrue(result["csRequired"])
        
    def test_prepare_job_less_detailed_description(self):
        job = {
            "title": "Software Engineer",
            "description": """Required skills include Python, Java, C/C++.""",
            "skills": ["R"],
        }
        
        result = prepare_job(job)
        
        self.assertEqual(result["title"], "Software Engineer")
        self.assertIn("Python", result["skills"])
        self.assertIn("Java", result["skills"])
        self.assertIn("C", result["skills"])
        self.assertIn("C++", result["skills"])
        self.assertIn("R", result["skills"])
        self.assertEqual(result["neededExperience"], None)
        self.assertEqual(result["education"], "Not Specified")
        self.assertFalse(result["csRequired"])
        
    def test_prepare_job_no_title(self):
        job = {
            "description": """Required skills include Python, Java, C/C++.""",
            "skills": ["R"],
        }
        
        result = prepare_job(job)
        
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(JobExtractorTest))