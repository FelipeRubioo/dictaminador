import pipojFunctions,directorioFunctions,fileGeneration,folioDictamen,config,Logins
from playwright.sync_api import sync_playwright
from pathlib import Path
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create the upload folder if it does not exist
imgDir = Path(__file__).parent / "images"
os.makedirs(imgDir, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    tipoBaja = ""
    imgDiagnosticoPath = ""
    modulo = "tickets administrador"
    tipoDictamen = request.form["tipo_dictamen"]
    if(tipoDictamen == "baja"):
        tipoBaja = request.form["tipo_baja"]
    folio = request.form["folio"]
    anio = request.form["anio"]
    numeroInventario = request.form["numeroInventario"]
    numeroSerie = request.form["numeroSerie"]
    modelo = request.form["modelo"]
    fallaEquipo = request.form["fallaEquipo"]
    diagnostico = request.form["diagnostico"]
    imgDiagnostico = request.files.get("img_diagnostico")
    if imgDiagnostico and imgDiagnostico.filename != "":
        imgDiagnosticoPath = os.path.join(imgDir,imgDiagnostico.filename)
        imgDiagnostico.save(imgDiagnosticoPath)
    componente = request.form["componente"]
    linkCompra = request.form["linkCompra"]


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #set true if dont want to see browser
        context = browser.new_context()
        def runAutomation(context):
            page1 = context.new_page()
            page1.goto('https://pipoj.stjsonora.gob.mx/App/#',wait_until="domcontentloaded")
            page1.wait_for_timeout(5000) #espera a que cargue pipoj
            pipojFunctions.abrirModulo(page1,modulo)
            pipojFunctions.abrirTicket(page1,folio,anio)
            unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,modelo,inventario,serie,fechaCompra = pipojFunctions.tomarDatosTicket(page1,numeroInventario,numeroSerie)
            
            #obtener datos de titular de la unidad y su puesto
            page2 = context.new_page()
            page2.goto('https://adison.stjsonora.gob.mx/Institucion/Directorio/#',wait_until="domcontentloaded")
            nombreTitular, puestoTitular = directorioFunctions.buscarUnidad(page2,unidad)
            
            
            page3 = context.new_page()
            #llenar formulario de solicitud de folio de dictamen
            folioDictamen.solicitarFolio(page3,folio,anio,solicitante,unidad,fallaEquipo,elaboro,inventario)
            
            #obtener numero de dictamen de teams
            page4 = context.new_page()
            numeroDictamen = folioDictamen.obtenerFolio(page4)
            
            #generar el dictamen
            fileGeneration.generarDictamen(folio,anio,unidad,solicitante,inventario,serie,fechaCompra,nombreTitular, puestoTitular,numeroDictamen,modelo,tipoDictamen,diagnostico,imgDiagnosticoPath,tipoBaja,componente,linkCompra)
        def deleteContext():
            Path("ms_auth.json").unlink(missing_ok=True)
            
            
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
                    deleteContext()
                    verifyContext(context)
                else:
                    print("context is valid,starting automation...")
                    runAutomation(context)
        verifyContext(context)
    return "el dictaminador dictamino..."
        
if __name__ == "__main__":
    app.run(debug=True)
    
