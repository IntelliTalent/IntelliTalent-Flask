from .helpers.docx_helpers import *
from .helpers.helper import (
    heading,
    objective,
    education,
    experience,
    projects,
    skills,
    certificates,
    upload_file,
)
from .logger import logger
from datetime import datetime
from docx import Document
from docx.shared import Pt, Cm, Mm
import os, json

def health_check():
    logger.info("Health check")
    return "Hello World From CV Generator Service!"

def generate_CV(data):
    try:
        logger.info("Generating CV")
        logger.debug("for data: %s", data)
        
        profile = data["profile"]
        
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
            section.page_height = Mm(297)
            section.page_width = Mm(210)
            
        # handling profile data
        
        # objective data
        summary = profile.get("summary")
        
        objective_data = {
            "summary": summary
        }
        
        # cleanup objective keys
        del profile["summary"]
        
        # education data
        education_data = profile.get("educations")
        
        # cleanup education keys
        if education_data:
            del profile["educations"]
        
        # experience data
        experience_data = profile.get("experiences")
        
        # cleanup experience keys
        if experience_data:
            del profile["experiences"]
            
        # projects data
        projects_data = profile.get("projects")
        
        for project in projects_data:
            if project.get("skills"):
                project["skills"] = ", ".join(project["skills"])
            
        # cleanup projects keys
        if projects_data:
            del profile["projects"]
            
        # skills data
        languages_list = profile.get("languages")
        skills_list = profile.get("skills")
        
        skills_data = []
        
        if languages_list and len(languages_list) > 0:
            skills_data.append({
                "category": "Languages",
                "list": ", ".join(languages_list)
            })
            
        if skills_list and len(skills_list) > 0:
            skills_data.append({
                "category": "Technologies",
                "list": ", ".join(skills_list)
            })
        
        # cleanup skills keys
        if languages_list:
            del profile["languages"]
        if skills_list:
            del profile["skills"]
            
        # certificates data
        certificates_data = profile.get("certificates")
        
        # cleanup certificates keys
        if certificates_data:
            del profile["certificates"]
            
        # heading data
        heading_data = profile

        heading(document, heading_data)
        objective(document, objective_data)
        if education_data and len(education_data) > 0:
            education(document, education_data)
        if experience_data and len(experience_data) > 0:
            experience(document, experience_data)
        if projects_data and len(projects_data) > 0:
            projects(document, projects_data)
        if skills_data and len(skills_data) > 0:
            skills(document, skills_data)
        if certificates_data and len(certificates_data) > 0:
            certificates(document, certificates_data)

        # Meta Data
        document.core_properties.author = heading_data["fullName"]
        document.core_properties.title = heading_data["fullName"] + " CV"
        document.core_properties.subject = "CV"
        document.core_properties.keywords = "CV, Resume, " + heading_data["fullName"]
        document.core_properties.category = "CV"
        document.core_properties.language = "en-US"
        
        user_fullname = heading_data["fullName"].replace(" ", "-")
        
        filename = f'api/generated-cvs/{user_fullname}-{datetime.now().strftime("%d-%m-%Y,%H-%M-%S")}.docx'
        
        # if the directory is not created, create it
        directory = 'api/generated-cvs'

        if not os.path.exists(directory):
            os.makedirs(directory)

        document.save(filename)
        
        word_link = upload_file(filename)
        
        # TODO: delete the generated file, here and in cover letter service
        
        response = {
            "word": word_link,
        }
        return json.dumps(response)
    except Exception as e:
        logger.exception("Error while generating CV: %s", e)
        return json.dumps({
            "message": "Error while generating CV!",
            "error": str(e),
            "status": 500
        })
