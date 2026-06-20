import pipojFunctions
import directorioFunctions
import fileGeneration
import folioDictamen
from playwright.sync_api import sync_playwright

def run():
    modulo = "tickets administrador"
    folio,anio= input("escribe folio del ticket (folio/año):").split("/")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #set true if dont want to see browser
        page = browser.new_page()
        page.goto('https://pipoj.stjsonora.gob.mx/App/#')
        #login
        pipojFunctions.login(page)
        page.wait_for_timeout(10000)  # 10,000 ms = 10 seconds, espera al autenticador
        pipojFunctions.abrirModulo(page,modulo)
        pipojFunctions.abrirTicket(page,folio,anio)
        unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto = pipojFunctions.tomarDatosTicket(page)
        
        #obtener datos de titular de la unidad y su puesto
        page2 = browser.new_page()
        page2.goto('https://adison.stjsonora.gob.mx/Institucion/Directorio/#')
        nombreTitular, puestoTitular = directorioFunctions.buscarUnidad(page2,unidad)
        fileGeneration.generarDictamen(unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,nombreTitular, puestoTitular)
        page2.close()
        #obtener numero de dictamen
        page3 = browser.new_page()
        page3.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/_layouts/15/listforms.aspx?cid=NDQ4Mjk4NTYtYzE1OC00MWUxLTgzZjYtZGQ3MjdiNWNjNjNh&nav=M2U4YzZiNDQtZTQ4Ni00OTRmLTlkZTItNWQ5YTFmOTVlYzQz')
        folioDictamen.loginInstitucional(page3)
        page3.wait_for_timeout(10000) 

if __name__ == "__main__":
    run()
