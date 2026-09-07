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
    page.wait_for_selector('[data-automationid="clientFormField-Elaboradopor"] input') #elaborado por
    page.wait_for_selector('[data-automationid="clientFormField-TicketdeSoporte"] input') #ticket de soporte
    page.wait_for_selector('[data-automationid="clientFormField-PersonaSolicitante"] input') #persona solicitante
    page.wait_for_selector('[data-automationid="clientFormField-Unidad"] input') #Unidad
    page.wait_for_selector('[data-automationid="clientFormField-Descripci_x00f3_ndelaFalla"] input') #Descripcion de la falla
    page.wait_for_selector('[data-automationid="clientFormField-A_x00f1_o"] input') #Año
    page.wait_for_selector('[data-automationid="clientFormField-NumeroOnventario"] input') #Numero Inventario
    page.wait_for_selector('#form-submit-button') #boton de enviar

    #asignaciones
    elaboradoInput = page.locator('[data-automationid="clientFormField-Elaboradopor"] input')
    ticketInput = page.locator('[data-automationid="clientFormField-TicketdeSoporte"] input')
    unidadInput = page.locator('[data-automationid="clientFormField-Unidad"] input')
    descripcionInput = page.locator('[data-automationid="clientFormField-Descripci_x00f3_ndelaFalla"] input')
    anioInput = page.locator('[data-automationid="clientFormField-A_x00f1_o"] input')
    inventarioInput = page.locator('[data-automationid="clientFormField-NumeroOnventario"] input')

    #llenado de campos, primero los normales, despues los de cuentas
    #page.wait_for_timeout(200)
    unidadInput.fill(unidad) #unidad
    descripcionInput.fill(descripcion) #descripcion de la fallas
    anioInput.fill(anio) #año
    inventarioInput.fill(inventarioFormato) #numero de inventario
    folioAnio = f"{folio}/{anio}"
    #page.wait_for_timeout(200)
    ticketInput.fill(folioAnio) #ticket de soporte

    elaboradoInput.fill(config.NOMBRESTJ) #elaborado por
    page.wait_for_timeout(6000)
    elaboradoInput.press('Enter')

    #si la persona solicitante no existe, se agrega quien genero el ticket, despues titular, si nadie tiene, se pone el tecnico
    people = [solicitante,elaboro,titular, config.NOMBRESTJ]
    picker = page.locator('[data-automationid="clientFormField-PersonaSolicitante"] input') #persona solicitante
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
    # esperar a que exista al menos una celda de la columna "consecutivo"
    # (no usar clases tipo row_62580b62: son hashes que SharePoint cambia entre versiones)
    page.wait_for_selector('[id^="virtualized-list"] [data-field-index="0"]')
    rows = page.locator(
        '[id^="virtualized-list"] [role="row"]:has([data-field-index="0"])'
    )
    row_count = rows.count()
    print(f"inspecting {row_count} rows")
    top_row_number = None
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
    if top_row_number is None:
        raise RuntimeError(
            "No se encontro ningun consecutivo en la lista de SharePoint "
            f"(se inspeccionaron {row_count} filas)"
        )
    return top_row_number
