import config

def loginMS(context):
    page = context.new_page()
    page.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/_layouts/15/listforms.aspx?cid=NDQ4Mjk4NTYtYzE1OC00MWUxLTgzZjYtZGQ3MjdiNWNjNjNh&nav=M2U4YzZiNDQtZTQ4Ni00OTRmLTlkZTItNWQ5YTFmOTVlYzQz',wait_until="domcontentloaded")

    #poner correo
    page.wait_for_selector('#i0116')
    page.locator('#i0116').fill(config.USER)
    page.wait_for_timeout(2000)
    page.click('#idSIButton9')

    #poner contraseña
    page.wait_for_selector('#i0118')
    page.locator('#i0118').fill(config.PASSWORD)
    page.wait_for_timeout(2000)
    page.click('#idSIButton9')

    #mantner sesion iniciada
    page.wait_for_selector('#idSIButton9')
    page.click('#idSIButton9')
    #wait for the selectors to save the context
    page.wait_for_selector('#combobox-id__13') #elaborado por
    page.wait_for_selector('#TextField15') #ticket de soporte
    page.wait_for_selector('#combobox-id__21') #persona solicitante
    page.wait_for_selector('#TextField23') #Unidad
    page.wait_for_selector('#TextField29') #Descripcion de la falla
    page.wait_for_selector('#TextField35') #Año
    page.wait_for_selector('#TextField41') #Numero Inventario
    page.close()

def loginPipoj(context):
    page = context.new_page()
    page.goto('https://pipoj.stjsonora.gob.mx/App/#',wait_until="domcontentloaded")
      # Wait for the inputs to appear
    page.wait_for_selector('[name="UserNameInput"]')
    page.wait_for_selector('[name="UserPasswordInput"]')
    page.wait_for_selector('#LoginButton')

    page.locator('[name="UserNameInput"]').fill(config.USER)
    page.locator('[name="UserPasswordInput"]').fill(config.PASSWORD)
    page.click('#LoginButton')

    page.wait_for_timeout(10000)  # 10,000 ms = 10 seconds, espera al autenticador
    page.close()