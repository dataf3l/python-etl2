import glob
import itertools
import os
import sys
import time

import pandas as pd
import pyodbc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

parent_dir = os.path.join(os.path.dirname(__file__), 'driver')

SERVER_DRIVER = '{SQL Server};'
SERVER_NAME = 'ALDRINHO\SQLEXPRESS;'
SERVER_DATABASE = 'scrapper_data;'

try:
    connection = pyodbc.connect('Driver=' + SERVER_DRIVER +
                                'Server=' + SERVER_NAME +
                                'Database=' + SERVER_DATABASE +
                                'Trusted_Connection=yes;')

    cursor = connection.cursor()

except Exception as e:
    print('Error in connection')


def init_login():
    remove_files()
    driver_path = os.path.join(parent_dir, 'chromedriver.exe')
    chrome_options = Options()
    prefs = {"download.default_directory": parent_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    driver.get("https://prestadores.minsalud.gov.co/habilitacion/work.aspx")
    time.sleep(2)

    WebDriverWait(driver, 2)

    driver.find_element(by=By.CLASS_NAME, value="btn-secondary").click()

    WebDriverWait(driver, 2)

    if driver.find_element(by=By.CLASS_NAME, value="btn-secondary").is_displayed():
        print("Button is displayed")
        driver.find_element(by=By.CLASS_NAME, value="btn-secondary").click()
    else:
        print("Button is not displayed")

    if not driver.find_element(by=By.ID, value="tbid_usuario").is_displayed():
        print("cannot login")
        sys.exit(0)

    driver.find_element(by=By.ID, value="tbid_usuario").clear()
    driver.find_element(by=By.ID, value="tbid_usuario").send_keys("invitado")
    driver.find_element(by=By.ID, value="tbcontrasena").clear()
    driver.find_element(by=By.ID, value="tbcontrasena").send_keys("invitado")
    driver.find_element(by=By.ID, value="Button1").click()

    WebDriverWait(driver, 2)

    return driver


def main():
    driver = init_login()

    webs = [
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/habilitados_reps.aspx?pageTitle"
                    "=Registro%20Actual&pageHlp=",
            "seconds": 10
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sedes_reps.aspx",
            "seconds": 10
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/serviciossedes_reps.aspx",
            "seconds": 30
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/capacidadesinstaladas_reps.aspx",
            "seconds": 8
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/medidasseguridad_reps.aspx",
            "seconds": 8
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sanciones_reps.aspx",
            "seconds": 8
        },
    ]

    for web in webs:
        get_csv(driver, web['link'], web['seconds'])

    search_files()


def get_csv(driver, report_url, second):
    REPORTURL = report_url
    driver.get(REPORTURL)
    driver.find_element(by=By.ID, value="_ctl0_ibBuscarFtr").click()
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").clear()
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").send_keys("|")
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_ibText").click()
    time.sleep(second)


def get_files_folder():
    os.chdir(parent_dir)
    return glob.glob("*.csv")


def search_files():
    files = get_files_folder()
    if len(files):
        for file in files:
            sep = ';' if file != 'Prestadores.csv' else '|'
            read_csv(file, sep)


def read_csv(file, sep):
    data = pd.read_csv(file, sep, encoding="ISO-8859-1", engine='python', error_bad_lines=False)
    filename = file.split('.')[0].lower()
    table = filename.replace('(', '_').replace(' ', '').replace(')', '')
    columns = []
    columns2 = []
    table_created = False

    for d in data:
        columns.append(str(d))
        columns2.append(str(d).replace(' ', '_').lower())

    try:
        sql = """CREATE TABLE  """ + table + \
              " (" + " nvarchar(max),".join(columns2) + " nvarchar(max))"

        print("Creating table: " + table)

        cursor.execute(sql)

        table_created = True
    except Exception as error:
        print(error)

    if table_created:
        print("Creating rows...")

        wildcards = list(map(str.lower, itertools.repeat('?', len(columns))))

        print("Inserting data into " + table)

        sql_into = "INSERT INTO " + table + "(" + ','.join(columns2) + ") VALUES (" + ','.join(wildcards) + ")"

        rows = []

        for row in pd.read_csv(file, sep, encoding="ISO-8859-1", error_bad_lines=False,
                               usecols=columns, low_memory=False).itertuples():

            data_row = []
            for column in columns:

                if table == 'sedes':
                    if column == 'Municipio PDET':
                        column = '_42'
                    elif column == 'Municipio PNSR':
                        column = '_43'
                    elif column == 'Municipio ZOMAC':
                        column = '_44'

                data_insert = str(getattr(row, column))

                data_row.append(data_insert)
            rows.append(data_row)

        print("Please, wait inserting files...")

        cursor.executemany(sql_into, rows)

        print("Files inserted!")

    connection.commit()


def remove_files():
    files = get_files_folder()
    if len(files):
        for file in files:
            os.remove(file)


if __name__ == "__main__":
    main()