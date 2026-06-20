import config


def loginInstitucional(page):
    page.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/_layouts/15/listforms.aspx?cid=NDQ4Mjk4NTYtYzE1OC00MWUxLTgzZjYtZGQ3MjdiNWNjNjNh&nav=M2U4YzZiNDQtZTQ4Ni00OTRmLTlkZTItNWQ5YTFmOTVlYzQz')
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

    #no mantener sesión iniciada
    page.wait_for_selector('#idBtn_Back')
    page.click('#idBtn_Back')

