def buscarUnidad(page,unidad):
    selectUnidad = page.locator('#IdUnidad')
    selectUnidad.select_option(label=unidad)
    page.click('#BtnBuscar')
    page.wait_for_selector('#TableDirectorio')

    #toma el nombre y el puesto
    first_card = page.locator('#TableDirectorio .card').first
    nombreTitular = first_card.locator('h4 span').text_content().strip()
    puestoTitular = first_card.locator('p').text_content().strip()
    
    return nombreTitular,puestoTitular
    
