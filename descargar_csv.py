#This is an mini program for web scrapping from a meteoroly station web from Brasil
#
#importación de libreria para utilizar el motor de navegación web
import mechanicalsoup
import webbrowser
import urllib.request
import urllib.parse
import json
import csv
from bs4 import BeautifulSoup

#Conexion y validación de usuario del sistema
# Create a browser object
browser = mechanicalsoup.Browser()
estacion = "AM"
nom_ar_est = estacion + "_estacion" + ".csv"
nom_ar_datos = estacion + "_result" + ".csv"
dataInicial= "2004-09-01"
dataFinal = "2017-03-27"
enlace = "http://www.agritempo.gov.br/agritempo/jsp/PesquisaClima/index.jsp?siglaUF=" + estacion

page = urllib.request.urlopen(enlace)
#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")

# con esto obtengo el listado del select (todas las estaciones meteorologicas)
estaciones = soup.select("select")
mylist = []
for option in estaciones[0].find_all('option'):
    mylist.append([option['value'],option.text])


with open(nom_ar_est, "w", encoding='utf-8') as fichero:
    writer = csv.writer(fichero)
    writer.writerows(mylist)
#guardo los datos de todas las estaciones meteorologicas de un estado en particular
for i in range(0,len(mylist)):
    try:
        print(f"Hola. Ahora i vale {i} y esta imprimiendo la idEstacao "+mylist[i][0])
        idEstacao = mylist[i][0]

        browser = mechanicalsoup.StatefulBrowser()
        browser.open(enlace)

        # encontramos el formulario para la carga de datos necesarios
        browser.select_form("#formularioPesquisaClimaDiario")
        # encontramos el input para los datos
        browser["idEstacao"] = idEstacao
        browser["dataInicial"] = dataInicial
        browser["dataFinal"] = dataFinal
        browser["temperaturaMinima"] = ""
        browser["temperaturaMedia"] = ""
        browser["temperaturaMaxima"] = ""
        browser["precipitacao"] = ""
        browser["umidadeMinima"] = ""
        browser["umidadeMaxima"] = ""
        browser["comparadorPrecipitacao"] = ""
        browser["comparadorTemperaturaMaxima"] = ""
        browser["comparadorTemperaturaMedia"] = ""
        browser["comparadorTemperaturaMinima"] = ""
        browser["comparadorUmidadeMaxima"] = ""
        browser["comparadorUmidadeMinima"] = ""

        # submit form
        page2 = browser.submit_selected()

        #jdata = json.loads(page2)
        #print(page2.json()["items"]);
    except requests.ConnectionError as e:
        print("Oops paso un error")
        idEstacaoCopia = idEstacao #voy a mantener una copia de la ultima estacao
        time.sleep(300) #voy a esperar 5min para reintentar
    finally:
        items = page2.json()["items"]
        cols = ["id","idEstacao", "data", "temperaturaMinima", "temperaturaMinimaDuvidosa", "temperaturaMinimaEstimada",
        "temperaturaMedia", "temperaturaMediaDuvidosa", "temperaturaMediaEstimada", "temperaturaMaxima",
        "temperaturaMaximaDuvidosa", "temperaturaMaximaEstimada", "precipitacao",
        "precipitacaoDuvidosa", "precipitacaoEstimada", "editavel", "disponibilidadeAguaSolo", "estiagemAgricola",
        "umidadeMinima","umidadeMinimaEstimada", "umidadeMaximaEstimada", "pontoOrvalhoMinimo", "umidadeMaxima", "evapotranspiracaoPotencial", "direcaoVento", "pressaoMaxima",
        "estiagem", "velocidadeVento", "radiacaoSolar", "horarioVento", "pontoOrvalhoMaximo", "evapotranspiracaoReal", "pressaoMinima",
        "pontoOrvalhoMinimoEstimado", "pontoOrvalhoMaximoEstimado"]
        with open(nom_ar_datos, 'a') as outfile:
            writer = csv.DictWriter(outfile, cols)
            if i == 0:
                #print("es el primer registro de mi primera estacion")
                writer.writeheader()
                print(f"Guardando los registros de mi estacion nro {i}")
                writer.writerows(items)
            else:
                print(f"Guardando los registros de mi estacion nro {i}")
                writer.writerows(items)



    #termina el for que recorre la lista de las estaciones meteorologicas
