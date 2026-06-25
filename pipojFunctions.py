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

def tomarDatosTicket(page,numeroInventario,numeroSerie):
    rows = page.locator('.panel-body .row')
    values = []

    for i in range(rows.count()):
        cols = rows.nth(i).locator('div')

        for j in range(cols.count()):
            text = cols.nth(j).text_content().strip()

            if text:  # ignore empty divs
                value = text.split('\n')[-1].strip()
                values.append(value)
    unidad = values[0]
    solicitante = values[1]
    elaboro = values[2]
    asignado = values[3]
    fechaRegistro = values[4]
    tipoServicio = values[5]
    fechaAtendido = values[6]
    descripcion = values[7]
    numeroContacto = values[8]
    modelo,serie, fechaCompra = tomarDatosEquipo(page,numeroInventario,numeroSerie)
    return unidad,solicitante,elaboro,asignado,fechaRegistro,tipoServicio,fechaAtendido,descripcion,numeroContacto,modelo,serie,fechaCompra

def tomarDatosEquipo(page,numeroInventario="",numeroSerie=""):
     modelo=""
     fechaCompra=""
     page.wait_for_selector('#btnOpenModalActivo')
     page.click('#btnOpenModalActivo')
    
     def obtenerDatos():
          page.wait_for_selector('#MD_BuscarActivo_lblModelo')
          page.wait_for_selector('#MD_BuscarActivo_lblNumeroSerie')
          page.wait_for_selector('#MD_BuscarActivo_lblFechaCompra')
          modelo = page.locator("#MD_BuscarActivo_lblModelo").text_content().strip()
          numeroSerie = page.locator("#MD_BuscarActivo_lblNumeroSerie").text_content().strip()
          fechaCompra = page.locator("#MD_BuscarActivo_lblFechaCompra").text_content().strip()
          print(f"modelo:{modelo},numeroSerie:{numeroSerie},fechaCompra:{fechaCompra}")
          return modelo,numeroSerie,fechaCompra
     
     def verificarError():
         #si busqueda de inventario da error, intentar busqueda por numero de serie
         if page.locator('#modalContentId').count() > 0:
                    print(f"no se encontro un activo con numero de inventario {numeroInventario}")
                    page.keyboard.press("Enter")
                    return True
                    
     #busqueda por inventario
     if(len(numeroInventario)>0):
         page.wait_for_selector('#MD_BuscarActivo_Txt_Clave')
         page.locator('#MD_BuscarActivo_Txt_Clave').fill(numeroInventario)
         page.click('#MD_BuscarActivo_BtnBuscar')
         if verificarError():
             busquedaSerie()
         else: 
            modelo,numeroSerie,fechaCompra = obtenerDatos()
     else:
        busquedaSerie()
     #busqueda por numero de serie
     def busquedaSerie():
        if(len(numeroSerie)>0):
            page.wait_for_selector('#MD_BuscarActivo_Txt_Serie')
            page.locator('#MD_BuscarActivo_Txt_Serie').fill(numeroSerie)
            page.click('#MD_BuscarActivo_BtnBuscar')
            if verificarError():
                print(f"no se encontro activo por numero de serie {numeroSerie}")
            else: 
                modelo,numeroSerie,fechaCompra = obtenerDatos()
     return modelo,numeroSerie,fechaCompra