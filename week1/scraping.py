from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

# Caminho para o GeckoDriver
gecko_path = "/home/ariel/Desktop/geckodriver-v0.35.0-linux64"

# Configurar o serviço do Firefox
service = Service(executable_path=gecko_path)

# Iniciar o navegador Firefox
driver = webdriver.Firefox(service=service)

try:
    # Abrir uma página
    driver.get("https://github.com")

    # Esperar a página carregar completamente (opcional)
    driver.implicitly_wait(10)

    # Extrair o título da página
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    print("Título da página:", titulo)

finally:
    # Fechar o navegador
    driver.quit()
