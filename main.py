import pipojFunctions
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
        pipojFunctions.tomarDatosTicket(page)

if __name__ == "__main__":
    run()
