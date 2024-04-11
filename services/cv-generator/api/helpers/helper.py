from .docx_helpers import *
from docx import Document
from docx.shared import Pt, Cm, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def heading(document, heading_content):
    """
    Add the heading to the document.
    
    Args:
        document: The document to add the heading to.
        heading_content: The content of the heading.
    """
    # first Line
    name = document.add_paragraph(heading_content["fullname"])
    name_format = name.paragraph_format
    name_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_format.space_before = 0
    name_format.space_after = Cm(0.2)
    name_format.line_spacing = 1
    name.runs[0].bold = True
    name.runs[0].font.size = Pt(26)
    
    # second Line
    second_line = document.add_paragraph("Phone: ")
    second_line.add_run(heading_content["phoneNumber"])
    second_line.add_run(" Email: ")
    # add dummy run, because indecies are used in heading_style
    second_line.add_run("")
    add_hyperlink(second_line, heading_content["email"], "mailto:" + heading_content["email"])
    heading_style(second_line)

    # third Line
    third_line = document.add_paragraph("Github: ")
    # add dummy run, because indecies are used in heading_style
    third_line.add_run("")
    add_hyperlink(third_line, heading_content["gitHub"], heading_content["gitHub"])
    third_line.add_run(" LinkedIn: ")
    # add dummy run, because indecies are used in heading_style
    third_line.add_run("")
    add_hyperlink(third_line, heading_content["linkedIn"], heading_content["linkedIn"])
    heading_style(third_line)
    
    # fourth Line
    fourth_line = document.add_paragraph("City: ")
    fourth_line.add_run(heading_content["city"])
    fourth_line.add_run(" Country: ")
    fourth_line.add_run(heading_content["country"])
    heading_style(fourth_line)
    
def objective(document, objective_content):
    """
    Add the objective to the document.
    
    Args:
        document: The document to add the objective to.
        objective_content: The content of the objective.
    """
    heading = document.add_paragraph("OBJECTIVE")
    objective = document.add_paragraph(objective_content["summary"] + "\n")
    objective_format = objective.paragraph_format
    objective_format.space_before = 0
    objective_format.space_after = 0
    objective_format.line_spacing = CONTENTLINESPACE
    objective.runs[0].bold = False
    objective.runs[0].font.size = Pt(11)
    sub_heading_style(heading)

def education(document, education_content):
    """
    Add the education to the document.
    
    Args:
        document: The document to add the education to.
        education_content: The content of the education.
    """
    # subheading
    heading = document.add_paragraph("EDUCATION")
    sub_heading_style(heading)
    # add content
    for component in education_content:
        education = document.add_paragraph(component["schoolName"])
        table = document.add_table(rows=1, cols=2)
        heading_cells = table.rows[0].cells
        heading_cells[0].text = component["degree"]
        if component["startDate"] and component["endDate"]:
            heading_cells[1].text = component["startDate"] + " - " + component["endDate"]
        else:
            heading_cells[1].text = ""
        table_style(table)

        content_description_style(document, component["description"])
        content_heading_style(education)
        
        document.add_paragraph("")
        
def experience(document, experience_content):
    """
    Add the experience to the document.
    
    Args:
        document: The document to add the experience to.
        experience_content: The content of the experience.
    """
    # subheading
    experience = document.add_paragraph("EXPERIENCE")
    sub_heading_style(experience)

    # add content
    for component in experience_content:
        experience = document.add_paragraph(component["jobTitle"])
        table = document.add_table(rows=1, cols=2)
        heading_cells = table.rows[0].cells
        heading_cells[0].text = component["companyName"]
        if component["startDate"] and component["endDate"]:
            heading_cells[1].text = component["startDate"] + " - " + component["endDate"]
        else:
            heading_cells[1].text = ""
        table_style(table)
        content_heading_style(experience)
        content_description_style(document, component["description"])
        
        document.add_paragraph("")

def projects(document, projects_content):
    """
    Add the projects to the document.
    
    Args:
        document: The document to add the projects to.
        projects_content: The content of the projects.
    """
    projects = document.add_paragraph("PROJECTS")
    sub_heading_style(projects)
    # add content
    for component in projects_content:
        table = document.add_table(rows=1, cols=2)
        heading_cells = table.rows[0].cells
        heading_cells[0].text = component["name"]
        content_heading_style(heading_cells[0].paragraphs[0])
        table_style(table)
        content_description_style(document, component["description"])
        
        # add content
        table = document.add_table(rows=0, cols=2)
        table.add_row()
        heading_cells = table.rows[-1].cells
        heading_cells[0].text = "Technologies"
        heading_cells[1].text = component["skills"]
        skill_heading_style(heading_cells[0].paragraphs[0])

        skill_style(table)
        
        document.add_paragraph("")

def skills(document, skills_content):
    """
    Add the skills to the document.
    
    Args:
        document: The document to add the skills to.
        skills_content: The content of the skills.
    """
    # subheading
    skills = document.add_paragraph("SKILLS")
    sub_heading_style(skills)

    # add content
    table = document.add_table(rows=0, cols=2)
    for skill in skills_content:
        table.add_row()
        heading_cells = table.rows[-1].cells
        heading_cells[0].text = skill["category"]
        heading_cells[1].text = skill["list"]
        skill_heading_style(heading_cells[0].paragraphs[0])

    skill_style(table)
    
    document.add_paragraph("")
    
def certificates(document, certificates_content):
    """
    Add the certificates to the document.
    
    Args:
        document: The document to add the certificates to.
        certificates_content: The content of the certificates.
    """
    # subheading
    certificates = document.add_paragraph("CERTIFICATES")
    sub_heading_style(certificates)

    # add content
    for component in certificates_content:
        certificates = document.add_paragraph(component["title"])
        table = document.add_table(rows=1, cols=2)
        heading_cells = table.rows[0].cells
        heading_cells[0].text = component["authority"]
        heading_cells[1].text = "Issued at: " + component["issuedAt"] + " Valid until: " + component["validUntil"]
        
        table_style(table)
        content_heading_style(certificates)
        
        description = document.add_paragraph("", style="List Bullet")
        add_hyperlink(description, component["url"], component["url"])
        bullet_list_style(description)
        
        document.add_paragraph("")