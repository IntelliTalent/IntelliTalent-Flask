from .helpers.docx_helpers import *
from .helpers.helper import *
from .logger import logger
from instance import config
from flask.helpers import send_file
from datetime import datetime
import json

def health_check():
    logger.info("Health check")
    return "Hello World From CV Generator Service!"

heading_data = {
    "fullname": "John Doe",
    "phoneNumber": "123456789",
    "email": "moaz25jan2015@gmail.com",
    "gitHub": "https://github.com",
    "linkedIn": "https://linkedin.com",
    "city": "Cairo",
    "country": "Egypt"
}
objective_data = {
    "summary": "I'm a software engineer with a passion for learning and teaching. I love working with Python, Django, and JavaScript. I'm currently looking for a full-time software engineering position."
}
education_data = [
    {
        "schoolName": "University of Engineering and Technology, Lahore",
        "degree": "Bachelor of Science in Computer Science",
        "startDate": "Sep 2019",
        "endDate": "Present",
        "description": "Relevant Coursework: Data Structures, Algorithms, Database Systems, Operating Systems, Computer Networks"
    },
    {
        "schoolName": "University of Engineering and Technology, Lahore",
        "degree": "Bachelor of Science in Computer Science",
        "startDate": "Sep 2019",
        "endDate": "Present",
        "description": "Relevant Coursework: Data Structures, Algorithms, Database Systems, Operating Systems, Computer Networks"
    }
]
projects_data = [
    {
        "name": "Project 1",
        "description": "Project Description 1",
        "skills": "Python, Django, HTML, CSS, JavaScript"
    },
    {
        "name": "Project 2",
        "description": "Project Description 2",
        "skills": "HTML, CSS, JavaScript"
    }
]
experience_data = [
    {
        "jobTitle": "Software Engineer Intern",
        "companyName": "Company Name",
        "startDate": "June 2021",
        "endDate": "August 2021",
        "description": "Worked on a project"
    },
    {
        "jobTitle": "Software Engineer Intern",
        "companyName": "Company Name",
        "startDate": "June 2021",
        "endDate": "Present",
        "description": "Worked on a project"
    }
]
skills_data = [
    {
        "category": "Languages",
        "list": "English, Arabic"
    },
    {
        "category": "Technologies",
        "list": "Python, Django, HTML, CSS, JavaScript"
    }
]
certificates_data = [
    {
        "title": "Certificate 1",
        "authority": "Authority 1",
        "issuedAt": "June 2021",
        "validUntil": "Present",
        "url": "https://certificate.com"
    },
    {
        "title": "Certificate 2",
        "authority": "Authority 2",
        "issuedAt": "June 2021",
        "validUntil": "Jan 2022",
        "url": "https://certificate2.com"
    }
]

def generate_CV(data):
    logger.info("Generating CV")
    logger.debug("for data: %s", data)
    
    # Create Document
    document = Document()
    style = document.styles["Normal"]
    style.paragraph_format.space_before = Cm(0.2)
    style.paragraph_format.space_after = 0
    style.paragraph_format.line_spacing = 1.5
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(11)
    font.bold = False

    sections = document.sections
    for section in sections:
        section.top_margin = Cm(1)
        section.bottom_margin = Cm(1)
        section.left_margin = Mm(7.5)
        section.right_margin = Mm(7.5)
        # A4 size
        section.page_height = Mm(297)
        section.page_width = Mm(210)

    heading(document, heading_data)
    objective(document, objective_data)
    education(document, education_data)
    experience(document, experience_data)
    projects(document, projects_data)
    skills(document, skills_data)
    certificates(document, certificates_data)

    # Meta Data
    document.core_properties.author = heading_data["fullname"]
    document.core_properties.title = heading_data["fullname"] + " CV"
    document.core_properties.subject = "CV"
    document.core_properties.keywords = "CV, Resume, " + heading_data["fullname"]
    document.core_properties.category = "CV"
    document.core_properties.language = "en-US"
    
    user_fullname = heading_data["fullname"].replace(" ", "-")
    
    filename = f'api/generated-cvs/{user_fullname}-{datetime.now().strftime("%d-%m-%Y,%H-%M-%S")}.docx'

    document.save(filename)
    
    # remove api word from the filename, because when routing to the file, it will be added automatically
    filename = filename.replace("api/", "")
    
    response = {
        "word": f"http://{config.server_ip}:3008/{filename}"
    }
    return json.dumps(response)

def get_file(filename):
    return send_file(f"generated-cvs/{filename}")
