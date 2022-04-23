# The purpose of this program is to fetch data from the minsalud website
# and store it in a csv file.
# The program will use selenium to interact with the website.

import time
import selenium
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import the Options clas
from selenium.webdriver.chrome.options import Options

#from email.headerregistry import HeaderRegistry
from selenium import webdriver
# import the  WebDriverWait class
from selenium.webdriver.support.ui import WebDriverWait


# By
from selenium.webdriver.common.by import By



def main():
    # this must be downloaded from https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.15/
    # and stored on the same folder as the application itself
    driver_path = ".\\chromedriver.exe"
    chrome_options = Options()
    #chrome_options.add_argument('--user-data-dir=user-data') 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  
    #chrome_options.add_argument('--disable-notifications')      

    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options, executable_path= driver_path)
    #driver = webdriver.Chrome(PATH)

    #driver.find_element(by=By.ID, value="_ctl0_ibBuscarFtr").click()

    driver.get("https://prestadores.minsalud.gov.co/habilitacion/work.aspx")


    #timeout = 5
    #try:
    #    element_present = EC.presence_of_element_located((By.NAME, 'button'))
    #    WebDriverWait(driver, timeout).until(element_present)
    #except TimeoutException:
    #    print("Timed out waiting for page to load")
    #    return

    # wait 2 seconds
    time.sleep(2)


    wait = WebDriverWait(driver, 2)
    # click the cerrar button to close the modal form
    driver.find_element(by=By.CLASS_NAME, value="btn-secondary").click()

    # check if the btn btn-secondary is present
    # wait for selector for .btn-secondary
    wait = WebDriverWait(driver, 2)
    # wait.until(lambda driver: driver.find_element_by_class_name("btn-secondary"))
    #wait.until(lambda driver: driver.find_element_by_css_selector(".btn-secondary"))

    if driver.find_element(by=By.CLASS_NAME, value="btn-secondary").is_displayed():
        print("Button is displayed")
        driver.find_element(by=By.CLASS_NAME, value="btn-secondary").click()
    else:
        print("Button is not displayed")

    if not driver.find_element(by=By.ID, value="tbid_usuario").is_displayed():
        print("cannot login")
        sys.exit(0)
        

    # clear the username field
    driver.find_element(by=By.ID, value="tbid_usuario").clear()
    driver.find_element(by=By.ID, value="tbid_usuario").send_keys("invitado")
    driver.find_element(by=By.ID, value="tbcontrasena").clear()
    driver.find_element(by=By.ID, value="tbcontrasena").send_keys("invitado")
    driver.find_element(by=By.ID, value="Button1").click()
    
    

    # click a button with a class "btn btn-secondary"

    wait = WebDriverWait(driver, 2)

    # wait for XPATH
    
    #try:
    #    element_present = EC.presence_of_element_located((By.XPATH, "//a[title=\"Formularios REPS, por Entidad Departamental o Distrital de Salud.\"]"))
    #    WebDriverWait(driver, timeout).until(element_present)
    #except TimeoutException:
    #    print("Timed out waiting for page to load")
    #    return

    # click link by XPATH
    #driver.find_element_by_xpath("//a[title=\"Formularios REPS, por Entidad Departamental o Distrital de Salud.\"]").click()

    reportURL = "https://prestadores.minsalud.gov.co/habilitacion/consultas/habilitados_reps.aspx?pageTitle=Registro%20Actual&pageHlp="
    driver.get(reportURL)

    # select state in <select> select the option named "Bogota"
    # driver.find_element_by_xpath("//select[@id='_ctl0_ContentPlaceHolder1_ddets']/option[text()='Bogotá D.C']").click()
    
    driver.find_element(by=By.ID, value="_ctl0_ibBuscarFtr").click()
    # after allowing pop up


    # change text delimiter
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").clear()
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_tbSeparator").send_keys("|")

    # click the "texto" button
    driver.find_element(by=By.ID, value="_ctl0_ContentPlaceHolder1_ibText").click()
    
    time.sleep(10)

    #driver.find_element_by_id("buscar").click()

    #fill ^ in delimiter field using selenium

    #driver.find_element_by_id("delimitador").send_keys("^")
    #driver.find_element_by_id("texto").click()





if __name__ == "__main__":
    main()