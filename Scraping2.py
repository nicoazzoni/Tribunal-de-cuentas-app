import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

post_url = "http://app.tribunaldecuentas.mendoza.gov.ar/leyrespfiscal/MostrarAnexo.php"

def ejecutar_scraping(años, trimestres, municipio, anexo):
    

    df_vacio = pd.DataFrame()

    for año in años:
        for trimestre in trimestres:
            payload = {
                        "source": "frmConsulta",
                        "ejercicio": año ,
                        "trimestre": trimestre,
                        "organismo": municipio,
                        "anexo": anexo,
                        "registros": "100"
                    }
            
            s = requests.Session()
            post_response = s.post(post_url, data=payload)
            status_code = post_response.status_code
            
            soup = BeautifulSoup(post_response.text, "html.parser")
            tabla = soup.find_all("table")[1]

#------------------------------Automatizamos el nombre de las columnas y ajustamos si tienen dos filas----------------------------------------------------------------------------------
            encabezado = tabla.find("thead")
            filas_encabezado = encabezado.find_all("tr")
                
            primera_fila = filas_encabezado[0].find_all("th")
            columnas = []
            colspan_map = []
            
            for th in primera_fila:
                    colspan = int(th.get("colspan",1))
                    text = th.get_text(strip=True)
                    columnas.extend([text]*colspan)
                    colspan_map.extend([colspan]*colspan)
            
            sub_headers = []
            if len(filas_encabezado) > 1:
                    segunda_fila = filas_encabezado[1].find_all("th")
                    for th in segunda_fila:
                        sub_headers.append(th.get_text(strip=True))
            
            final_headers = []
            sub_index = 0
            
            for i, col in enumerate(columnas):
                if colspan_map[i] > 1:
                    final_headers.append(f"{col} - {sub_headers[sub_index]}")
                    sub_index += 1
            
                else: 
                    final_headers.append(col)
                    
            final_headers.append("Año")
            final_headers.append("Trimestre")
            
#-----------------------------------------Le asignamos los titulos al dataframe------------------------------------------------------------------------------------------------------------
            
            if df_vacio.empty:
                df_vacio = pd.DataFrame(columns = final_headers)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            data1 = tabla.find("tbody")
            data2 = data1.find_all("tr")
        
            for row in data2:
                row_data = row.find_all("td")
                individual_row_data = [data.text for data in row_data]
                individual_row_data.append(año)
                individual_row_data.append(trimestre)
                ###### ACA AGREGAS CUANDO QUIERAS QUE SE AGREGUE EL AÑO, TRIMESTRE Y JURISDICCION PERO TENES QUE TENER CUIDADO DE CREAR LAS COLUMNAS EN EL DATA FRAME Y ADEMAS EN EL ORDEN CORRECTO
        
                
                length = len(df_vacio)
                df_vacio.loc[length] = individual_row_data

            st.write(f"Extrayendo información del Año: {año} y Trimestre: {trimestre}")
        
            df_vacio.drop(df_vacio[df_vacio[df_vacio.columns[0]] == "TOTAL"].index, inplace=True)
            df_vacio.drop(df_vacio[df_vacio[df_vacio.columns[0]] == "SUBTOTAL"].index, inplace=True) 
            
#--------------------Hacemos que todas menos la primer columna se convierta a numero y haga los reemplazos de puntos a comas y asi----------------------------------------------------------
        
        
    for col in final_headers[1:]:
        try:
            df_vacio[col] = df_vacio[col].astype(str).str.replace(".", "", regex=False)
            df_vacio[col] = df_vacio[col].str.replace(",", ".", regex=False).astype(float)
            
        except ValueError:
            continue
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
            
    return df_vacio



def to_excel(funcion):
    output = BytesIO() 
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        funcion.to_excel(writer, index=False, sheet_name="Datos")
    return output.getvalue()

