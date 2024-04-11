import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt, Cm, Inches

# constants
HEADINGLINESPACE = 1.15
SUBHEADINGLINESPACE = 1.15
CONTENTLINESPACE = 1.5
SKILLWIDTH = 9

def insert_hr(target_paragraph):
    """
    Insert a horizontal line into a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to insert the horizontal line into.
    """
    paragraph_element = target_paragraph._p
    paragraph_properties = paragraph_element.get_or_add_pPr()
    paragraph_border = docx.oxml.shared.OxmlElement('w:pBdr')
    paragraph_properties.insert_element_before(paragraph_border, *['w:' + tag for tag in ['shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap', 'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid', 'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection', 'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']])
    bottom_border = docx.oxml.shared.OxmlElement('w:bottom')
    for attribute, value in [('w:val', 'single'), ('w:sz', '6'), ('w:space', '1'), ('w:color', 'auto')]:
        bottom_border.set(docx.oxml.ns.qn(attribute), value)
    paragraph_border.append(bottom_border)

def get_or_create_hyperlink_style(document):
    """
    Get or create the hyperlink style in a document.
    
    Args:
        document: The document to get or create the hyperlink style in.
    Returns:
        The name of the hyperlink style.
    """
    if "Hyperlink" not in document.styles:
        if "Default Character Font" not in document.styles:
            default_style = document.styles.add_style("Default Character Font", docx.enum.style.WD_STYLE_TYPE.CHARACTER, True)
            default_style.element.set(docx.oxml.shared.qn('w:default'), "1")
            default_style.priority = default_style.hidden = 1
            default_style.unhide_when_used = True
            del default_style
        hyperlink_style = document.styles.add_style("Hyperlink", docx.enum.style.WD_STYLE_TYPE.CHARACTER, True)
        hyperlink_style.base_style = document.styles["Default Character Font"]
        hyperlink_style.unhide_when_used = True
        hyperlink_style.font.color.rgb = docx.shared.RGBColor(0x05, 0x63, 0xC1)
        hyperlink_style.font.underline = True
        del hyperlink_style
    return "Hyperlink"

def add_hyperlink(target_paragraph, hyperlink_text, hyperlink_url):
    """
    Add a hyperlink to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to add the hyperlink to.
        hyperlink_text: The text of the hyperlink.
        hyperlink_url: The URL of the hyperlink.
    Returns:
        The hyperlink element.
    """
    document_part = target_paragraph.part
    relationship_id = document_part.relate_to(hyperlink_url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink_element = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink_element.set(docx.oxml.shared.qn('r:id'), relationship_id)
    new_run = docx.text.run.Run(docx.oxml.shared.OxmlElement('w:r'), target_paragraph)
    new_run.text = hyperlink_text
    new_run.style = get_or_create_hyperlink_style(document_part.document)
    hyperlink_element.append(new_run._element)
    target_paragraph._p.append(hyperlink_element)
    return hyperlink_element

def heading_style(target_paragraph, is_dual_heading=True):
    """
    Apply the heading style to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to apply the heading style to.
        is_dual_heading: Whether the heading is a dual heading.
    """
    target_paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    target_paragraph.paragraph_format.space_before = target_paragraph.paragraph_format.space_after = 0
    target_paragraph.paragraph_format.line_spacing = HEADINGLINESPACE
    target_paragraph.runs[0].bold = True
    target_paragraph.runs[0].font.size = Pt(11)
    target_paragraph.runs[1].bold = False
    target_paragraph.runs[1].font.size = Pt(11)
    if is_dual_heading:
        target_paragraph.runs[2].bold = True
        target_paragraph.runs[2].font.size = Pt(11)
        target_paragraph.runs[3].bold = False
        target_paragraph.runs[3].font.size = Pt(11)

def sub_heading_style(target_paragraph):
    """
    Apply the sub-heading style to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to apply the sub-heading style to.
    """
    target_paragraph.paragraph_format.space_before = 0
    target_paragraph.paragraph_format.space_after = Cm(0.2)
    target_paragraph.paragraph_format.line_spacing = SUBHEADINGLINESPACE
    target_paragraph.runs[0].bold = True
    target_paragraph.runs[0].font.size = Pt(14)
    insert_hr(target_paragraph)

def content_heading_style(target_paragraph):
    """
    Apply the content heading style to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to apply the content heading style to.
    """
    target_paragraph.paragraph_format.space_before = target_paragraph.paragraph_format.space_after = 0
    target_paragraph.paragraph_format.line_spacing = CONTENTLINESPACE
    target_paragraph.runs[0].bold = True
    target_paragraph.runs[0].font.size = Pt(13)

def table_style(target_table):
    """
    Apply the table style to a target_table.
    
    Args:
        target_table: The table to apply the table style to.
    """
    target_table.autofit = target_table.allow_autofit = False
    target_table.cell(0,0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    target_table.cell(0,1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for cell_index in [0, 1]:
        cell_format = target_table.cell(0, cell_index).paragraphs[0].paragraph_format
        cell_format.space_before = cell_format.space_after = 0
        cell_format.line_spacing = CONTENTLINESPACE
        target_table.cell(0, cell_index).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for row in target_table.rows:
        row.height = Cm(0.1)

def bullet_list_style(target_paragraph):
    """
    Apply the bullet list style to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to apply the bullet list style to.
    """
    paragraph_format = target_paragraph.paragraph_format
    paragraph_format.space_before = paragraph_format.space_after = 0
    paragraph_format.line_spacing = CONTENTLINESPACE
    paragraph_format.left_indent = Inches(0.5)

def content_description_style(target_document, description_text):
    """
    Apply the content description style to a paragraph.
    
    Args:
        target_document: The document to apply the content description style to.
        description_text: The description text.
    """
    description_paragraph = target_document.add_paragraph(description_text, style="List Bullet")
    bullet_list_style(description_paragraph)

def skill_style(target_table):
    """
    Apply the skill style to a target_table.
    
    Args:
        target_table: The table to apply the skill style to.
    """
    target_table.autofit = target_table.allow_autofit = False
    for row in target_table.rows:
        row.height = Cm(0.1)
        row.cells[0].width = Cm(SKILLWIDTH)
        row.cells[1].width = 7052310 - SKILLWIDTH * 360000
        for cell_index in [0, 1]:
            cell_format = row.cells[cell_index].paragraphs[0].paragraph_format
            cell_format.space_before = cell_format.space_after = 0
            cell_format.line_spacing = CONTENTLINESPACE

def skill_heading_style(target_paragraph):
    """
    Apply the skill heading style to a target_paragraph.
    
    Args:
        target_paragraph: The paragraph to apply the skill heading style to.
    """
    paragraph_format = target_paragraph.paragraph_format
    paragraph_format.space_before = paragraph_format.space_after = 0
    paragraph_format.line_spacing = CONTENTLINESPACE
    target_paragraph.runs[0].bold = True
    target_paragraph.runs[0].font.size = Pt(11)
    