from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

    
def get_spanish_month(month_number):
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return months[month_number - 1]

def add_header(doc: Document):
    now = datetime.now()

    day = now.day
    month = get_spanish_month(now.month)
    year = now.year

    header_text = f"Hermosillo, Sonora, a {day} de {month} de {year}"

    for section in doc.sections:
        header = section.header
        paragraph = header.paragraphs[0] if header.paragraphs else header.add_paragraph()

        paragraph.text = header_text
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def generarDictamen(unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,nombreTitular, puestoTitular):
    #creates file
    doc = Document()
    #make all changes to file
    add_header(doc)

    doc.add_paragraph("Contenido del documento...")
    #generates file
    doc.save("output.docx")