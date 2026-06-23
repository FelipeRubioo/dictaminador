from requests import options

import config


def loginInstitucional(page):
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

    #no mantener sesión iniciada
    page.wait_for_selector('#idBtn_Back')
    page.click('#idBtn_Back')

def solicitarFolio(page,folio,anio,solicitante,unidad,descripcion,elaboro):
    #esperar a que carguen todos los campos
    page.wait_for_selector('#combobox-id__13') #elaborado por
    page.wait_for_selector('#TextField15') #ticket de soporte
    page.wait_for_selector('#combobox-id__21') #persona solicitante
    page.wait_for_selector('#TextField23') #Unidad
    page.wait_for_selector('#TextField29') #Descripcion de la falla
    page.wait_for_selector('#TextField35') #Año
    page.wait_for_selector('#TextField41') #Numero Inventario

    #llenado de campos
    page.locator('#combobox-id__13').fill(config.NOMBRESTJ) #elaborado por
    picker = page.locator('#combobox-id__13')
    page.wait_for_timeout(6000)
    picker.press('Enter')

    folioAnio = f"{folio}/{anio}"
    page.locator('#TextField15').fill(folioAnio) #ticket de soporte
    
    page.locator('#combobox-id__21').fill(solicitante) #persona solicitante
    #si la persona solicitante no existe, se agrega quien genero el ticket, si ni una de las dos tiene cuenta, se pone el mismo tecnico
    people = [solicitante,elaboro, config.NOMBRESTJ]
    picker = page.locator('#combobox-id__21')
    options = page.get_by_role("option") 
    for person in people:
        picker.fill(person)
        page.wait_for_timeout(6000)
        if options.count() > 0:
            picker.press("Enter")
            break
        else:
            print(f"No suggestions for {person}")
    
    page.locator('#TextField23').fill(unidad) #unidad
    page.locator('#TextField29').fill(descripcion) #descripcion de la falla
    page.locator('#TextField35').fill(anio) #año
    page.wait_for_timeout(10000)