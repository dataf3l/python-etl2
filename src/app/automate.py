import glob
import itertools
import os
import sys
import time
import platform
import argparse
import re

import pandas as pd
import pyodbc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pathlib import Path
from csv import reader


# set download directory
def get_download_directory():
    return str(Path.home() / "Downloads")


# get_ODBC_driver_name return the odbc driver name installed in the system
def get_odbc_driver_name():
    odbc_driver_name = '{'+sorted(pyodbc.drivers()).pop()+'}'
    return odbc_driver_name


# get_connection_db return a connection pointer to the database and a error string
def get_connection_db():
    # set the connection string
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SERVER_DRIVER = get_odbc_driver_name()
    DATABASE = os.environ.get('DATABASE')
    USER_NAME = os.environ.get('USER_NAME')
    PASSWORD = os.environ.get('PASSWORD')
    DOWNLOAD_DIRECTORY = get_download_directory()
    print(" * SERVER_NAME: ", SERVER_NAME)
    print(" * SERVER_DRIVER: ", SERVER_DRIVER)
    print(" * DATABASE: ", DATABASE)
    print(" * USERNAME: ", USER_NAME)
    print(" * DOWNLOAD_DIRECTORY: ", DOWNLOAD_DIRECTORY)

    cdn = 'DRIVER='+SERVER_DRIVER + ';SERVER=' + SERVER_NAME+';DATABASE=' + \
        DATABASE + ';SSPI=yes' + ';UID='+USER_NAME+';PWD=' + PASSWORD
    try:
        connection = pyodbc.connect(cdn)
    except Exception as e:
        return None, str(e)
    return connection, None


# init_login login to the website
def init_login(driver):
    # open the website
    driver.get("https://prestadores.minsalud.gov.co/habilitacion/work.aspx")
    # wait for the page to be loaded
    time.sleep(10)
    # find the login button and click on it
    button = driver.find_element(by=By.CLASS_NAME, value="btn-secondary")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(button).click(button).perform()
    # wait for the page to be loaded
    WebDriverWait(driver, 4)
    # find the username and password fields and fill them
    if driver.find_element(by=By.CLASS_NAME, value="btn-secondary").is_displayed():
        try:
            driver.find_element(
                by=By.CLASS_NAME, value="btn-secondary").click()
        except Exception as e:
            print("> Error trying to click on the button: ", e)
            print("Retrying...")
            time.sleep(5)
            init_login(driver)
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
        preferences["download.default_directory"] = get_download_directory()
        options.add_experimental_option("prefs", preferences)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(options=options, service=service)
    except IOError:
        print("> get_driver: Error trying to setting webdriver: ", IOError)
        system.exit(1)
    return browser


# get_url_webs return the url of the website and the file name to download
def get_url_webs(files_to_download):
    if files_to_download == 'all':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/habilitados_reps.aspx?pageTitle"
                "=Registro%20Actual&pageHlp=",
                "seconds": 5,
                "file_name": "Prestadores.csv",
                "table_name": "prestadores"
            },
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sedes_reps.aspx",
                "seconds": 5,
                "file_name": "Sedes.csv",
                "table_name": "sedes"
            },
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/serviciossedes_reps.aspx",
                "seconds": 5,
                "file_name": "Servicios.csv",
                "table_name": "servicios"
            },
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/capacidadesinstaladas_reps.aspx",
                "seconds": 5,
                "file_name": "CapacidadInstalada.csv",
                "table_name": "capacidad_instalada"
            },
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/medidasseguridad_reps.aspx",
                "seconds": 5,
                "file_name": "MedidasSeguridad.csv",
                "table_name": "medidas_seguridad"
            },
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sanciones_reps.aspx",
                "seconds": 5,
                "file_name": "MedidasSeguridad (1).csv",
                "table_name": "sanciones"
            },
        ]
    if files_to_download == 'prestadores':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/habilitados_reps.aspx?pageTitle"
                "=Registro%20Actual&pageHlp=",
                "seconds": 5,
                "file_name": "Prestadores.csv",
                "table_name": "prestadores"
            },
        ]
    if files_to_download == 'sedes':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sedes_reps.aspx",
                "seconds": 5,
                "file_name": "Sedes.csv",
                "table_name": "sedes"
            },
        ]
    if files_to_download == 'servicios':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/serviciossedes_reps.aspx",
                "seconds": 5,
                "file_name": "Servicios.csv",
                "table_name": "servicios"
            },
        ]
    if files_to_download == 'capacidad':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/capacidadesinstaladas_reps.aspx",
                "seconds": 5,
                "file_name": "CapacidadInstalada.csv",
                "table_name": "capacidad_instalada"
            },
        ]
    if files_to_download == 'seguridad':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/medidasseguridad_reps.aspx",
                "seconds": 5,
                "file_name": "MedidasSeguridad.csv",
                "table_name": "medidas_seguridad"
            },
        ]
    if files_to_download == 'sanciones':
        return [
            {
                "link": "https://prestadores.minsalud.gov.co/habilitacion/consultas/sanciones_reps.aspx",
                "seconds": 5,
                "file_name": "MedidasSeguridad.csv",
                "table_name": "sanciones"
            },
        ]


# download_files download the files from the url
def download_files(driver, url_webs):
    for web in url_webs:
        print("> Downloading: ", web["file_name"])
        if get_csv(driver, web['link']):
            maximum_attempts = 20
            number_of_attemps = 0
            # wait for the file to be downloaded
            while os.path.exists(get_download_directory() + "/" + web['file_name']) == False:
                number_of_attemps = number_of_attemps + 1
                print(">> Waiting for file to be downloaded: " + get_download_directory() + "/" +
                      web['file_name'])
                time.sleep(15)
                if number_of_attemps == maximum_attempts:
                    print(">> Error trying to download file: " +
                          web['file_name'])
                    break
            print(">> done...")
        else:
            print(">> Error downloading: "+web['file_name'])
            continue


# get_csv set the separator character and click on the link to download the file
def get_csv(driver, report_url):
    try:
        driver.get(report_url)
        # wait for the page to be loaded
        time.sleep(5)
        driver.find_element(by=By.ID, value="_ctl0_ibBuscarFtr").click()
        driver.find_element(
            by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").clear()
        driver.find_element(
            by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").send_keys("|")
        driver.find_element(
            by=By.ID, value="_ctl0_ContentPlaceHolder1_ibText").click()
        return True
    except Exception as e:
        print("> get_csv: Error trying to get the CSV: ", e)
        return False


# get_files return all files in the download directory
def get_files():
    return glob.glob(get_download_directory()+"/"+"*.csv")


# check_separator_character fix issues with the separator character in the csv files
# Note: for any reason the separator character is not the same in the csv files
def check_separator_character(files):
    # reemplace character (;) for (|) if exists
    for file in files:
        print("> Checking separator character: ", file)
        try:
            with open(file, encoding='latin-1', mode='r') as f:
                lines = f.readlines()
                if lines[0].find(";") != -1:
                    print(">> Separator character found: ", file)
                    with open(file, 'w') as f:
                        for line in lines:
                            f.write(line.replace(";", "|"))
                    print(">> Separator character replaced: ", file)
        except IOError:
            print("> Error trying to check separator character: ", IOError)
            return False
    return True


# process_files process the files and save them in the database
def process_files(connection, url_webs):
    # search for the files in the download directory
    files = get_files()
    if check_separator_character(files):
        print(">> Separator character checked")
    else:
        print(">> Separator character failed")
        sys.exit(1, "Error trying to check separator character")
    if len(files) == len(url_webs):
        for file in url_webs:
            read_csv(file, connection)


# read_csv read the csv file and insert the data into the database
def read_csv(file, connection):
    path_to_file = get_download_directory() + "/" + file['file_name']
    # read the with pandas and get the DataFrame
    try:
        data = pd.read_csv(path_to_file, delimiter="|", encoding="latin-1",
                           engine='python', error_bad_lines=False)
    except IOError as e:
        print("> Error trying to read csv file: ", path_to_file)
        print("> Error: ", e)
        sys.exit(1)
    print("> Creating {0} table... ".format(file['table_name']))
    columns = []
    columns2 = []
    for d in data:
        columns.append(str(d))
        columns2.append(str(d).replace(' ', '_').lower())
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + file['table_name'])
        sql = """CREATE TABLE  """ + file['table_name'] + \
              " (" + " nvarchar(max),".join(columns2) + " nvarchar(max))"
        cursor.execute(sql)
        table_created = True
    except Exception as error:
        table_created = False
        print("> Error trying to create table: ", error)

    if table_created:
        print("> Creating rows...")
        wildcards = list(map(str.lower, itertools.repeat('?', len(columns))))
        print("> Inserting data into {0} table".format(file['table_name']))
        sql_into = "INSERT INTO " + file['table_name'] + \
            "(" + ','.join(columns2) + ") VALUES (" + ','.join(wildcards) + ")"
        rows = []
        for row in data.itertuples():
            data_row = []
            for column in columns:
                if file['table_name'] == 'sedes':
                    if column == 'Municipio PDET':
                        column = '_42'
                    elif column == 'Municipio PNSR':
                        column = '_43'
                    elif column == 'Municipio ZOMAC':
                        column = '_44'
                data_insert = str(getattr(row, column))
                data_row.append(data_insert)
            rows.append(data_row)
        # delete DataFrame to free memory
        del data
        print("> Please, wait inserting records...")
        try:
            cursor.executemany(sql_into, rows)
            connection.commit()
            print(
                "> Records successfully inserted into table ", file['table_name'])
        except Exception as err:
            print("> Error trying to insert data  into table {0} error: {1}".format(
                file['table_name'], err))
            return


# remove_files remove the files from the download directory
def remove_files():
    files = get_files()
    print("Removing files...", files)
    if len(files):
        for file in files:
            os.remove(file)


# initialize set of environment variables (production or development)
def initialize():
    # cli arguments
    parser = argparse.ArgumentParser(description='Automate scraper tool:')
    parser.add_argument('--mode', type=str, default='prod', choices=['prod', 'dev'],
                        help='production or development mode (default: production)')
    parser.add_argument('-f', type=str, default='all', choices=['all', 'prestadores',
                        'sedes', 'servicios', 'capacidad', 'seguridad', 'sanciones'],
                        help='specifically select which file you want to download (default: all)')
    # parse arguments
    args = parser.parse_args()
    mode = args.mode.lower()
    files_to_download = args.f.lower()
    # display process progress information to the user
    print("Step 1: Initialize environment...")
    print("> Running in mode: " + mode)
    print("> Files selected: " + files_to_download)
    # select the .env file from the environment mode (prod/dev)
    environment = Path('./config/env') / mode / '.env'
    # check if the environment file exists
    if not environment.exists():
        print("> Environment file not found: " + str(environment))
        return files_to_download, False
    # load the .env file
    load_dotenv(dotenv_path=environment)
    return files_to_download,  True


# main function to run the scraper
def main(files_to_download):
    print("Step 2: Get DB connection...")
    connection, err = get_connection_db()
    if err is not None:
        print("> Error connecting to database: ", err)
        sys.exit(1)
    print("Step 3: Get SELENIUM driver...")
    driver = get_driver()
    print("Step 4: Login in website...")
    driver = init_login(driver)
    print("Step 5: Get csv files...")
    # url_webs have the url of the files to download
    url_webs = get_url_webs(files_to_download)
    download_files(driver, url_webs)
    print("Step 6: Finish spider job ...")
    driver.quit()
    print("Step 7: Read cvs files...")
    process_files(connection, url_webs)
    print(">> Program finished successfully")


# principal function to run the program
if __name__ == "__main__":
    # remove the previous files in the download directory
    remove_files()
    # check if the environment variables are set
    files_to_download, success = initialize()
    if success == False:
        print(">> Step 1: Error initializing the environment")
        exit(1)  # exit with error
    # start the program
    main(files_to_download)
