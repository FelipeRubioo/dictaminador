from requests import options

import config


def solicitarFolio(page,folio,anio,solicitante,unidad,descripcion,elaboro,inventario):
    page.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/_layouts/15/listforms.aspx?cid=NDQ4Mjk4NTYtYzE1OC00MWUxLTgzZjYtZGQ3MjdiNWNjNjNh&nav=M2U4YzZiNDQtZTQ4Ni00OTRmLTlkZTItNWQ5YTFmOTVlYzQz',wait_until="domcontentloaded")
    if(len(inventario)==0):
        inventario = f"no existe numero de inventario para el equipo del ticket {folio}/{anio}"

    #esperar a que carguen todos los campos
    page.wait_for_selector('#combobox-id__13') #elaborado por
    page.wait_for_selector('#TextField15') #ticket de soporte
    page.wait_for_selector('#combobox-id__21') #persona solicitante
    page.wait_for_selector('#TextField23') #Unidad
    page.wait_for_selector('#TextField29') #Descripcion de la falla
    page.wait_for_selector('#TextField35') #Año
    page.wait_for_selector('#TextField41') #Numero Inventario
    page.wait_for_selector('#form-submit-button') #boton de enviar

    #llenado de campos, primero los normales, despues los de cuentas
    page.wait_for_timeout(200)
    page.locator('#TextField23').fill(unidad) #unidad
    page.locator('#TextField29').fill(descripcion) #descripcion de la fallas
    page.locator('#TextField35').fill(anio) #año
    page.locator('#TextField41').fill(inventario) #año
    folioAnio = f"{folio}/{anio}"
    page.wait_for_timeout(200)
    page.locator('#TextField15').fill(folioAnio) #ticket de soporte

    page.locator('#combobox-id__13').fill(config.NOMBRESTJ) #elaborado por
    picker = page.locator('#combobox-id__13')
    page.wait_for_timeout(6000)
    picker.press('Enter')

    
    page.wait_for_timeout(200)
    page.locator('#combobox-id__21').fill(solicitante) #persona solicitante
    page.wait_for_timeout(200)
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

    button = page.locator('#form-submit-button')
    page.wait_for_timeout(2000)
    button.click()
    
def obtenerFolio(page):
    page.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/Lists/Solicitud%20Dolio%20Dictamen/AllItems.aspx?sortField=FechaSolFolio&isAscending=false&viewid=6c8423da%2D1ff8%2D446a%2Db78e%2D65adc3bfef9d',wait_until="domcontentloaded")
    page.wait_for_selector('#virtualized-list_4_page-0')
    rows = page.locator(
    '#virtualized-list_4_page-0 .row_62580b62.perfRow_62580b62'
    )
    row_count = rows.count()
    print(f"inspecting {row_count} rows")
    for i in range(row_count):
        text = (
            rows.nth(i)
            .locator('[data-field-index="0"]')
            .inner_text()
            .strip()
        )
        parts = text.split()
        if len(parts) >= 2 and parts[-1].isdigit():
            number = int(parts[-1])
            print(f"number {number} found in row {i}")

            top_row_number = number + i
            print(f"Top number is {number} at row {i}")
            print(f"Top row should be {top_row_number}")
            break
        else:
            print(f"number not found in row {i}")
    return top_row_number

    page.wait_for_timeout(10000)