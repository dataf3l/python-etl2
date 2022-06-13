import glob
import itertools
import os
import sys
import time
import platform
import argparse

import pandas as pd
import pyodbc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pathlib import Path

# set download directory
DOWNLOAD_DIRECTORY = './downloads'

# get_connection_db return a connection pointer to the database and a error string


def get_connection_db():
    # detect platform and create connection string
    if platform.system() == 'Windows':
        print("> System is Windows")
        SERVER_DRIVER = os.environ.get('SERVER_DRIVER')
        SERVER_NAME = os.environ.get('SERVER_NAME')
    elif platform.system() == 'Linux':
        print("> System is Linux:")
        SERVER_DRIVER = os.environ.get('SERVER_DRIVER')
        SERVER_NAME = os.environ.get('SERVER_NAME')
        print(" * SERVER_DRIVER: ", SERVER_DRIVER)
        print(" * SERVER_NAME: ", SERVER_NAME)

    DATABASE = os.environ.get('DATABASE')
    USER_NAME = os.environ.get('USER_NAME')
    PASSWORD = os.environ.get('PASSWORD')
    print(" * DATABASE: ", DATABASE)
    print(" * USERNAME: ", USER_NAME)
    print(" * PASSWORD: ", PASSWORD)

    cdn = 'DRIVER='+SERVER_DRIVER + ';SERVER=' + SERVER_NAME+';DATABASE=' + \
        DATABASE + ';SSPI=yes' + ';UID='+USER_NAME+';PWD=' + PASSWORD
    try:
        connection = pyodbc.connect(cdn)
    except Exception as e:
        return None, str(e)
    return connection.cursor(), None


def init_login(driver):
    # remove_files()
    driver.get("https://prestadores.minsalud.gov.co/habilitacion/work.aspx")
    time.sleep(4)

    WebDriverWait(driver, 4)

    driver.find_element(by=By.CLASS_NAME, value="btn-secondary").click()

    WebDriverWait(driver, 4)

    if driver.find_element(by=By.CLASS_NAME, value="btn-secondary").is_displayed():
        print("Button is displayed")
        driver.find_element(
            by=By.CLASS_NAME, value="btn-secondary").click()
    else:
        print("Button is not displayed")

    if not driver.find_element(by=By.ID, value="tbid_usuario").is_displayed():
        print("cannot login")
        sys.exit(0)

    driver.find_element(by=By.ID, value="tbid_usuario").clear()
    driver.find_element(
        by=By.ID, value="tbid_usuario").send_keys("invitado")
    driver.find_element(by=By.ID, value="tbcontrasena").clear()
    driver.find_element(
        by=By.ID, value="tbcontrasena").send_keys("invitado")
    driver.find_element(by=By.ID, value="Button1").click()

    WebDriverWait(driver, 2)

    return driver

# get_driver settings and return a driver pointer to the web browser


def get_driver():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        preferences = {}
        # preferences["profile.default_content_settings.popups"] = 0
        preferences["download.default_directory"] = DOWNLOAD_DIRECTORY
        options.add_experimental_option("prefs", preferences)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(options=options, service=service)
    except IOError:  # <!--REQUIRE:  IOError
        print("> get_driver: Error trying to setting webdriver: ", IOError)
    return browser


def download_files(driver):
    # webs have the URL target to download the files
    url_webs = [
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/habilitados_reps.aspx?pageTitle"
                    "=Registro%20Actual&pageHlp=",
            "seconds": 10,
            "file_name": "Prestadores.csv"
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sedes_reps.aspx",
            "seconds": 10,
            "file_name": "Sedes.csv"
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/serviciossedes_reps.aspx",
            "seconds": 30,
            "file_name": "Servicios.csv"
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/capacidadesinstaladas_reps.aspx",
            "seconds": 8,
            "file_name": "CapacidadInstalada.csv"
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/medidasseguridad_reps.aspx",
            "seconds": 8,
            "file_name": "MedidasSeguridad.csv"
        },
        {
            "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sanciones_reps.aspx",
            "seconds": 8,
            "file_name": "MedidasSeguridad (1).csv"
        },
    ]

    for web in url_webs:
        print("> Dowland: ", web["file_name"])
        get_csv(driver, web['link'], web['seconds'])
        # wait for the file to be downloaded
        while os.path.exists(DOWNLOAD_DIRECTORY + "/" + web['file_name']) == False:
            print(">> Waiting for file to be downloaded: "+web['file_name'])
            time.sleep(15)
        print(">> done...")


def main():
    print("Steep 2: Get DB connection...")
    connection, err = get_connection_db()
    if err is not None:
        print("> Error connecting to database: ", err)
        sys.exit(1)
    print("Steep 3: Get driver...")
    driver = get_driver()
    print("Steep 4: Login...")
    driver = init_login(driver)
    print("Steep 5: Get csv files...")
    download_files(driver)
    print("Steep 6: Finish spider job ...")
    driver.quit()
    print("Steep 7: Read cvs files...")
    search_files()


def get_csv(driver, report_url, second):
    URL_REPORT = report_url
    driver.get(URL_REPORT)
    driver.find_element(by=By.ID, value="_ctl0_ibBuscarFtr").click()
    driver.find_element(
        by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").clear()
    driver.find_element(
        by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").send_keys("|")
    driver.find_element(
        by=By.ID, value="_ctl0_ContentPlaceHolder1_ibText").click()
    time.sleep(second)


def get_files():
    return glob.glob(DOWNLOAD_DIRECTORY+"/"+"*.csv")


def search_files():
    files = get_files()
    print("search_files: ", files)

    if len(files):
        for file in files:
            sep = ';' if file != 'Prestadores.csv' else '|'
            read_csv(file, sep)


def read_csv(file, sep):
    data = pd.read_csv(file, sep, encoding="ISO-8859-1",
                       engine='python', error_bad_lines=False)
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

        sql_into = "INSERT INTO " + table + \
            "(" + ','.join(columns2) + ") VALUES (" + ','.join(wildcards) + ")"

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
    print("Removing files...", files)
    if len(files):
        for file in files:
            os.remove(file)

# initialize the program with the environment variables (production or development)

# initialize set of environment variables (production or development)


def initialize():
    # cli arguments
    parser = argparse.ArgumentParser(description='Automate scraper tool:')
    parser.add_argument('--mode', type=str, default='prod', choices=['prod', 'dev'],
                        help='production or development mode (default: production)')
    # parse arguments
    args = parser.parse_args()
    mode = args.mode.lower()
    print("Step 1: Initialize environment...")
    print("> Running in mode: " + mode)
    # select the .env file from the environment mode
    environment = Path('./config/env') / mode / '.env'
    # check if the environment file exists
    if not environment.exists():
        print("> Environment file not found: " + str(environment))
        return False
    # load the .env file
    load_dotenv(dotenv_path=environment)
    # check if the environment variables are set
    if (os.environ.get('SERVER_DRIVER') == ""):
        print("> Error loading .env file")
        return False
    return True


# principal function to run the program
if __name__ == "__main__":
    # check if the environment variables are set
    if initialize() == False:
        print(">> Step 1: Error initializing the environment")
        exit(1)  # exit with error
    # start the program
    main()
