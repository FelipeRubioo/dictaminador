import pipojFunctions
import directorioFunctions
import fileGeneration
import folioDictamen
import config
import Logins
from playwright.sync_api import sync_playwright
from pathlib import Path



def run():
    modulo = "tickets administrador"
    folio,anio= input("escribe folio del ticket (folio/año):").split("/")
    inventario = input("escribe el numero de inventario:")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #set true if dont want to see browser
        context = browser.new_context()
        def runAutomation(context):
            page1 = context.new_page()
            page1.goto('https://pipoj.stjsonora.gob.mx/App/#',wait_until="domcontentloaded")
            page1.wait_for_timeout(5000) #espera a que cargue pipoj
            pipojFunctions.abrirModulo(page1,modulo)
            pipojFunctions.abrirTicket(page1,folio,anio)
            unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto = pipojFunctions.tomarDatosTicket(page1)
            
            #obtener datos de titular de la unidad y su puesto
            page2 = context.new_page()
            page2.goto('https://adison.stjsonora.gob.mx/Institucion/Directorio/#',wait_until="domcontentloaded")
            nombreTitular, puestoTitular = directorioFunctions.buscarUnidad(page2,unidad)
            fileGeneration.generarDictamen(unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,nombreTitular, puestoTitular)
            
            page3 = context.new_page()
            #llenar formulario de solicitud de folio de dictamen
            folioDictamen.solicitarFolio(page3,folio,anio,solicitante,unidad,descripcion,elaboro,inventario)
            
            #obtener numero de dictamen de teams
            page4 = context.new_page()
            numeroDictamen = folioDictamen.obtenerFolio(page4)

        def deleteContext():
            Path("ms_auth.json").unlink(missing_ok=True)
            context = browser.new_context()
            return context
            
        def verifyContext(context):
            if not Path(config.AUTH_FILE).exists():
                print("creating new context...")
                Logins.loginMS(context)
                Logins.loginPipoj(context)

                context.storage_state(path=config.AUTH_FILE)
                print(f"Session saved to {config.AUTH_FILE}")
            if Path(config.AUTH_FILE).exists():
                print("context exists...verifying if logged in")
                context = browser.new_context(storage_state=config.AUTH_FILE)
                page = context.new_page()
                #if pipoj requests password, current context has been logged out, delete and create another
                page.goto('https://pipoj.stjsonora.gob.mx/App/#')
                if page.locator('#LoginButton').count() > 0:
                    print("Login page detected, deleting current context and creating new one")
                    context = deleteContext()
                    verifyContext(context)
                else:
                    print("context is valid,starting automation...")
                    runAutomation(context)
        verifyContext(context)
        
        
if __name__ == "__main__":
    run()
