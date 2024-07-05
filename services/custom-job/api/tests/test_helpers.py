import unittest

from api.helpers.helper import (extract_company_names, extract_countries_cities, extract_job_end_dates,
                                extract_languages, extract_skills, is_country, normalize_job_title,
                                extract_job_titles, extract_locations, extract_job_types, extract_years_of_experience)


class HelpersTest(unittest.TestCase):

    def test_extract_skills_single(self):
        prompt = "We are looking for a developer with experience in Python and SQL."
        expected = ["Python", "SQL"]
        result = extract_skills(prompt)
        self.assertEqual(result, expected)

    def test_extract_skills_multiple(self):
        prompt = "The candidate should know Java, Spring, and React."
        expected = ["Java", "Spring", "React"]
        result = extract_skills(prompt)
        self.assertEqual(result, expected)

    def test_extract_skills_mixed_case(self):
        prompt = "Experience in docker and KUBERNETES is required."
        expected = ["docker", "KUBERNETES"]
        result = extract_skills(prompt)
        self.assertEqual([r.lower() for r in result], [e.lower() for e in expected])

    def test_extract_skills_no_match(self):
        prompt = "We need someone with expertise in C and Perl."
        expected = ['C', 'Perl']
        result = extract_skills(prompt)
        self.assertEqual(result, expected)

    def test_extract_skills_with_variations(self):
        prompt = "Knowledge of Node.js, Express, and Angular is essential."
        expected = ["Node.js", "Express", "Angular"]
        result = extract_skills(prompt)
        self.assertEqual(result, expected)

    def test_normalize_job_title_exact_match(self):
        input_title = "Software Engineer"
        expected = "Software Engineer"
        result = normalize_job_title(input_title)
        self.assertEqual(result, expected)

    def test_normalize_job_title_variation(self):
        input_title = "sr software engineer"
        expected = "Senior Software Engineer"
        result = normalize_job_title(input_title)
        self.assertEqual(result, expected)

    def test_normalize_job_title_mixed_case(self):
        input_title = "Front-End Developer"
        expected = "Frontend Developer"
        result = normalize_job_title(input_title)
        self.assertEqual(result, expected)

    def test_normalize_job_title_abbreviation(self):
        input_title = "swe"
        expected = "Software Engineer"
        result = normalize_job_title(input_title)
        self.assertEqual(result, expected)

    def test_normalize_job_title_no_match(self):
        input_title = "Data Entry Specialist"
        expected = None
        result = normalize_job_title(input_title)
        self.assertEqual(result, expected)

    def test_extract_job_titles_single(self):
        prompt = "We are hiring a software engineer to join our team."
        expected = ["Software Engineer"]
        result = extract_job_titles(prompt)
        self.assertEqual(result, expected)

    def test_extract_job_titles_multiple(self):
        prompt = "Looking for a frontend developer and a backend developer."
        expected = ["Frontend Developer", "Backend Developer"]
        result = extract_job_titles(prompt)
        self.assertEqual(result, expected)

    def test_extract_job_titles_mixed_case(self):
        prompt = "We need a Senior Software Engineer and a junior frontend developer."
        expected = set(["Software Engineer","Senior Software Engineer", "Frontend Developer"])
        result = set(extract_job_titles(prompt))
        self.assertSetEqual(result, expected)

    def test_extract_job_titles_no_match(self):
        prompt = "We need someone with experience in marketing."
        expected = []
        result = extract_job_titles(prompt)
        self.assertEqual(result, expected)

    def test_extract_job_titles_variation(self):
        prompt = "Hiring a sr software engineer and a full stack developer."
        expected = ["Software Engineer","Senior Software Engineer", "Full Stack Developer"]
        result = extract_job_titles(prompt)
        self.assertEqual(result, expected)

    def test_extract_job_titles_with_sliding_window(self):
        prompt = "Join us as a front end developer or a back end developer."
        expected = ["Frontend Developer", "Backend Developer"]
        result = extract_job_titles(prompt)
        self.assertEqual(result, expected)

    def test_extract_locations_single(self):
        prompt = "This is a remote position."
        expected = ["Remote"]
        result = extract_locations(prompt)
        self.assertEqual(result, expected)


    def test_extract_locations_mixed_case(self):
        prompt = "The role can be on-site in Austin or remote."
        expected = set(["On Site", "Remote"])
        result = set(extract_locations(prompt))
        self.assertSetEqual(result, expected)

    def test_extract_locations_no_match(self):
        prompt = "We are expanding our operations in Paris."
        expected = []
        result = extract_locations(prompt)
        self.assertEqual(result, expected)

    def test_extract_locations_with_variation(self):
        prompt = "This is a hybrid role based in Berlin."
        expected = ["Hybrid"]
        result = extract_locations(prompt)
        self.assertEqual(result, expected)


    def test_single_year_of_experience(self):
        prompt = "The candidate must have 5 years of experience."
        expected = ["5"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_range_of_experience(self):
        prompt = "We are looking for someone with 3-5 years of experience."
        expected = ["3-5"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_single_year_of_experience_with_years(self):
        prompt = "Required: experience of 4 years."
        expected = ["4"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_range_of_experience_with_years(self):
        prompt = "Candidates should have experience of 2-4 years."
        expected = ["2-4"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_single_year_experience(self):
        prompt = "The applicant must possess 6 years experience."
        expected = ["6"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_range_year_experience(self):
        prompt = "Applicants with 1-3 years experience will be preferred."
        expected = ["1-3"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_single_year_experience_yrs(self):
        prompt = "The candidate must have 7 yrs of experience."
        expected = ["7"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_range_year_experience_yrs(self):
        prompt = "We need someone with 2-6 yrs of experience."
        expected = ["2-6"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_single_year_plus_experience(self):
        prompt = "The job requires 5+ years experience."
        expected = ["5"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)

    def test_range_year_plus_experience(self):
        prompt = "Applicants with 4-8+ years of experience are encouraged to apply."
        expected = ["4-8"]
        result = extract_years_of_experience(prompt)
        self.assertEqual(result, expected)
    def test_month_day_year(self):
        prompt = "Apply by August 31, 2024."
        expected = ["August 31, 2024"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_month_day(self):
        prompt = "Apply by August 31."
        expected = ["August 31"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_mm_dd_yyyy(self):
        prompt = "The application deadline is 08/31/2024."
        expected = ["08/31/2024"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_mm_dd_yy(self):
        prompt = "The deadline is 08/31/24."
        expected = ["08/31/24"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_mm_dd(self):
        prompt = "Apply by 08/31."
        expected = ["08/31"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_mm_dd_yyyy_dash(self):
        prompt = "Submit your application by 08-31-2024."
        expected = ["08-31-2024"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_mm_dd_yy_dash(self):
        prompt = "The deadline is 08-31-24."
        expected = ["08-31-24"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_day_month_year(self):
        prompt = "Submit your application by 31 August 2024."
        expected = ["31 August 2024"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_day_month(self):
        prompt = "The deadline is 31 August."
        expected = ["31 August"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_yyyy_mm_dd(self):
        prompt = "The application deadline is 2024-08-31."
        expected = ["2024-08-31"]
        result = extract_job_end_dates(prompt)
        self.assertEqual(result, expected)

    def test_extract_single_country(self):
        prompt = "The job is based in the United States."
        expected_countries = ["United States"]
        expected_cities = []
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)

    def test_extract_single_city(self):
        prompt = "Our office is located in New York."
        expected_countries = []
        expected_cities = ["New York"]
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)

    def test_extract_multiple_countries_cities(self):
        prompt = "We have offices in Paris, Berlin, and Tokyo, but our headquarters are in the France."
        expected_countries = ["France"]
        expected_cities = ["Paris", "Tokyo"]
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)

    def test_extract_no_gpe(self):
        prompt = "We are hiring for various positions."
        expected_countries = []
        expected_cities = []
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)

    def test_extract_country_and_city_in_same_sentence(self):
        prompt = "Our main office is in Berlin, Germany."
        expected_countries = ["Germany"]
        expected_cities = ["Berlin"]
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)

    def test_extract_ambiguous_location(self):
        prompt = "The conference will be held in London, United Kingdom."
        expected_countries = ["United Kingdom"]
        expected_cities = ["London"]
        countries, cities = extract_countries_cities(prompt)
        self.assertEqual(countries, expected_countries)
        self.assertEqual(cities, expected_cities)
    
    def test_is_country(self):
        self.assertTrue(is_country("United States"))
        self.assertFalse(is_country("New York"))
        self.assertTrue(is_country("Germany"))
        self.assertFalse(is_country("Paris"))

    def test_extract_languages_single(self):
        prompt = "Candidates should be fluent in English."
        expected = ["English"]
        result = extract_languages(prompt)
        self.assertEqual(result, expected)

    def test_extract_languages_multiple(self):
        prompt = "Fluency in French and German is required."
        expected = ["French", "German"]
        result = extract_languages(prompt)
        self.assertEqual(result, expected)

    def test_extract_languages_mixed_case(self):
        prompt = "We need someone who speaks spanish and Chinese."
        expected = ["spanish", "Chinese"]
        result = extract_languages(prompt)
        self.assertEqual([r.lower() for r in result], [e.lower() for e in expected])

    def test_extract_languages_no_match(self):
        prompt = "We are looking for a candidate with good communication skills."
        expected = []
        result = extract_languages(prompt)
        self.assertEqual(result, expected)

    def test_extract_company_names_no_match(self):
        prompt = "We are looking for someone skilled in Python and Java."
        expected = []
        result = extract_company_names(prompt)
        self.assertEqual(result, expected)

    def test_extract_full_time(self):
        prompt = "We are looking for a full-time developer."
        expected = ["Full Time"]
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

    def test_extract_part_time(self):
        prompt = "The position is part time and offers flexible hours."
        expected = ["Part Time"]
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

    def test_extract_contract(self):
        prompt = "This is a contract position for 6 months."
        expected = ["Contract"]
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

    def test_extract_internship(self):
        prompt = "We have an internship opportunity available."
        expected = ["Internship"]
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

    def test_extract_freelance(self):
        prompt = "Looking for a freelancer for project-based work."
        expected = ["Freelance"]
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

    def test_extract_multiple_job_types(self):
        prompt = "We offer both full-time and part-time positions."
        expected = set(["Full Time", "Part Time"])
        result = set(extract_job_types(prompt))
        self.assertSetEqual(result, expected)

    def test_extract_no_job_type(self):
        prompt = "We are hiring developers."
        expected = []
        result = extract_job_types(prompt)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(HelpersTest))