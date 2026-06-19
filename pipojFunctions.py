import config

def login(page):
      # Wait for the inputs to appear
    page.wait_for_selector('[name="UserNameInput"]')
    page.wait_for_selector('[name="UserPasswordInput"]')
    page.wait_for_selector('#LoginButton')

    page.locator('[name="UserNameInput"]').fill(config.USER)
    page.locator('[name="UserPasswordInput"]').fill(config.PASSWORD)
    page.click('#LoginButton')

def abrirModulo(page,modulo):
    page.wait_for_selector('[id="FindGeneral"]')
    searchGeneral = page.locator('[id="FindGeneral"]')
    searchGeneral.fill(modulo)
    searchGeneral.press("Enter")

def abrirTicket(page,folio,anio):
    page.wait_for_selector('#Folio')
    page.wait_for_selector('#Anio')
    page.wait_for_selector('#btnBuscar')
    page.locator('#Folio').fill(folio)
    page.locator('#Anio').fill(anio)
    page.wait_for_timeout(2000)
    page.click('#btnBuscar')
    #open the ticket
    page.wait_for_selector('#Listatickets')
    button = page.locator('#ListaTickets tbody tr').first.locator('td').nth(8).locator('button')
    button.click()
    page.wait_for_timeout(10000) 