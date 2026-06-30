from requests import options

import config


def solicitarFolio(page,folio,anio,solicitante,unidad,descripcion,elaboro,inventario,titular):
    inventarioFormato = ""
    page.goto('https://stjsh.sharepoint.com/sites/SoporteTcnicoySoftwareSTJS-SolicitudFolioDictamenes/_layouts/15/listforms.aspx?cid=NDQ4Mjk4NTYtYzE1OC00MWUxLTgzZjYtZGQ3MjdiNWNjNjNh&nav=M2U4YzZiNDQtZTQ4Ni00OTRmLTlkZTItNWQ5YTFmOTVlYzQz',wait_until="domcontentloaded")
    if(len(inventario)==0):
        inventarioFormato = f"no existe numero de inventario para el equipo del ticket {folio}/{anio}"
    #evita error de que ya se solicito dictamen para este equipo 
    if(len(inventario)>0):
        inventarioFormato = f"ticket {folio}/{anio} con numero de inventario {inventario}"
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
    #page.wait_for_timeout(200)
    page.locator('#TextField23').fill(unidad) #unidad
    page.locator('#TextField29').fill(descripcion) #descripcion de la fallas
    page.locator('#TextField35').fill(anio) #año
    page.locator('#TextField41').fill(inventarioFormato) #año
    folioAnio = f"{folio}/{anio}"
    #page.wait_for_timeout(200)
    page.locator('#TextField15').fill(folioAnio) #ticket de soporte

    page.locator('#combobox-id__13').fill(config.NOMBRESTJ) #elaborado por
    page.wait_for_timeout(6000)
    page.locator('#combobox-id__13').press('Enter')

    #si la persona solicitante no existe, se agrega quien genero el ticket, despues titular, si nadie tiene, se pone el tecnico
    people = [solicitante,elaboro,titular, config.NOMBRESTJ]
    picker = page.locator('#combobox-id__21') 
    for person in people:
        picker.fill(person)
        page.wait_for_timeout(6000)
        descendant = picker.get_attribute('aria-activedescendant') 
        if descendant != "sug-noResultsFound":
            picker.press("Enter")
            break
        else:
            print(f"No suggestions for {person}")

    page.wait_for_timeout(2000)
    page.locator('#form-submit-button').click()
    

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
    page.close()
    return top_row_number
