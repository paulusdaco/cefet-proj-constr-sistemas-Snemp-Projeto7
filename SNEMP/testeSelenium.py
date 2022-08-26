from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get("http://localhost:5000/")

# Teste de importação
csv = driver.find_element("id","csvfile")
csv.send_keys(os.getcwd()+r"\static\csv\tce.csv")
csv.submit()

# Teste de busca
# FILTRAGEM NÃO IMPLEMENTADA
try:
    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.NAME, 'dropdownfiltro')))
except TimeoutException:
    print ("Loading took too much time!")

search = driver.find_element("id", "searchbar")
search.send_keys("MATERIAL DE CONSUMO")
search.submit()