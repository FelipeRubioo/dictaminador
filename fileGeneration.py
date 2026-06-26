from docx import Document
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from datetime import datetime
from docx.shared import Cm, Pt

    
def get_spanish_month(month_number):
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return months[month_number - 1]

def agregarEncabezado(doc: Document,numeroDictamen,folio,anio):
    now = datetime.now()

    day = now.day
    month = get_spanish_month(now.month)
    year = now.year

    textoFecha = f"Hermosillo, Sonora, a {day} de {month} de {year}"

    logo_path = Path(__file__).parent / "images" / "logoSTJ.png"
    stacked_text = f"\tDictamen:{numeroDictamen}/{anio}\n\tReferencia a la solicitud de Soporte Técnico {folio}/{anio}\n\t{textoFecha}"
    for section in doc.sections:
    
      header = section.header
      paragraph1 = header.paragraphs[0] if header.paragraphs else header.add_paragraph()

      run = paragraph1.add_run()
      run.add_picture(str(logo_path), width=Cm(2.5))
    
      paragraph2 = header.add_paragraph()
      paragraph2.alignment = WD_ALIGN_PARAGRAPH.RIGHT

      run = paragraph2.add_run(stacked_text)
      run.bold = True
      run.font.size = Pt(10)

def agregarTitular(doc: Document,nombreTitular, puestoTitular,unidad):
    stacked_text = f"\t{nombreTitular}\n\t{puestoTitular}\n\t{unidad}\n\tPresente.-"
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(stacked_text)
    run.bold = True
    run.font.size = Pt(12)

def generarDictamen(folio,anio,unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,inventario,serie,fechaCompra,nombreTitular, puestoTitular,numeroDictamen):
    #creates file
    doc = Document()
    #set global style
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    #make all changes to file
    agregarEncabezado(doc,numeroDictamen,folio,anio)
    agregarTitular(doc,nombreTitular,puestoTitular,unidad)
    #doc.add_paragraph("Contenido del documento...")
    #generates file     
    doc.save("output.docx")