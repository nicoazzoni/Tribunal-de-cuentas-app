import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Scraping2 import ejecutar_scraping
from Scraping2 import to_excel
from io import BytesIO

años = ["2014","2015","2016","2017","2018","2019","2020","2021","2022","2023", "2024","2025"]

municipios = {
    "Ciudad de Mendoza":"52",
    "General Alvear":"53",
    "Godoy Cruz":"54",
    "Guaymallén":"55",
    "Junín":"56",
    "La Paz":"57",
    "Las Heras":"58",
    "Lavalle":"59",
    "Luján de Cuyo":"60",
    "Maipú":"61",
    "Malargüe":"62",
    "Rivadavia":"63",
    "San Carlos":"64",
    "San Martín":"65",
    "San Rafael":"66",
    "Santa Rosa":"67",
    "Tunuyán":"68",
    "Tupungato":"69"
}

trimestres = ["1", "2", "3", "4"]

anexos = {
    "1 - PROGRAMACION FINANCIERA ART. 22 LEY 7314": "ProFin",
    "2 - DE LA EJECUCION DEL PRESUPUESTO CON RELACION A LOS CREDITOS ACUMULADA AL FIN DEL TRIMESTRE": "EjePreCreAcu",
    "2 bis - DE LA EJECUCION DEL PRESUPUESTO CON RELACION A LOS CREDITOS CORRESPONDIENTE AL TRIMESTRE": "EjePreRelCre",
    "3 - DE LA EJECUCION DEL PRESUPUESTO CON RELACION AL CALCULO DE RECURSOS Y FINANCIAMIENTO ACUMULAD...": "EjePreCalRecFinAcu",
    "4 - EJECUCION PRESUPUESTARIA DEL TRIMESTRE. CUMPLIMIENTO DE METAS": "EjePreCumMeta",
    "5 - EVOLUCION DE LA DEUDA PÚBLICA CONSOLIDADA ACUMULADA AL FIN DEL TRIMESTRE": "EvoDeuConAcu",
    "6 - EVOLUCION DE LA DEUDA FLOTANTE ACUMULADA AL FIN DEL TRIMESTRE": "EvoDeuFloAcu",
    "17 - DETALLE DE JUICIOS EN EJECUCION Según Art 30 inc a) y Art 34 inc f)": "DetJuiEjec",
    "18 - DETALLE DE JUICIOS CON SENTENCIA DEFINITIVA Según Art 30 inc b) y Art 34 inc g)": "DetJuiSenDef",
    "19 - DETALLE DE LA PLANTA DE PERSONAL Y CONTRATOS DE LOCACION. IMPORTES LIQUIDADOS ACUMULADOS AL …": "DetPerPlaLocImpLiqAcu",
    "22 - INFORME CINCUENTA PRINCIPALES CONTRIBUYENTES CON DEUDA Según Art 34 inc d) por cada uno de l...": "InfContDeuDerTasRee",
    "23 - INFORME DE MOROSIDAD Según Art 34 inc d) por cada uno de los Derechos, Tasas Municipales y R...": "InfMorDerTasRee",
    "30 - ANEXO 30 ARTICULO 14 INCISO E": "IE-14-E",
    "30 - ANEXO 30 ARTICULO 27": "IE-27",
    "30 - ANEXO 30 ARTICULO 28": "IE-28",
    "30 - ANEXO 30 ARTICULO 34 INCISO H": "IE-34-H",
    "30 - ANEXO 30 ARTICULO 5 INCISO C": "IE-05-C",
    "30 - ANEXO 30 ARTICULO 5 INCISO D": "IE-05-D",
    "30 - ANEXO 30 OTRAS EXPLICACIONES": "IE-OTRASEXP"
}

st.title("Tribunal de cuentas - Mendoza")

lista_municipio = st.selectbox("Selecciona el Municipio:", list(municipios.keys()))
municipio_numero = municipios[lista_municipio]

lista_año = st.multiselect("Selecciona uno o más años:", sorted(años,reverse=True) , default=["2024"])
lista_trimestre = st.multiselect("Selecciona uno o más trimestres:", trimestres, default=["4"])
lista_anexo = st.selectbox("Selecciona el Informe:", list(anexos.keys()))
anexo_codigo = anexos[lista_anexo]

if st.button ("Vista Previa"):
    st.write(f"Iniciando Scrap para: {lista_municipio}")
    funcion = ejecutar_scraping(lista_año, lista_trimestre, municipio_numero, anexo_codigo)
    funcion["Municipio"] = lista_municipio
    
    st.markdown('<p style="color:green; font-weight:bold;">Finalizado ✅</p>', unsafe_allow_html=True)
    st.dataframe(funcion)
    excel_data = to_excel(funcion)
      
    st.download_button(
            label="Descargar el archivo Excel",
            data=excel_data,
           file_name=f"{lista_municipio}_datos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

