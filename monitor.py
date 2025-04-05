from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

ULTIMO_VALOR_ARQUIVO = 'ultimo_valor.txt'

def obter_valor_produto():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/lib/chromium/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.fadel.io/missioncontrolplus")
        time.sleep(5)
        elemento = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/nav/a[1]/strong/span")
        valor = elemento.text
        print(f"✅ Valor encontrado: {valor}")
        return valor
    except Exception as e:
        print("❌ Erro ao obter valor:", e)
        return None
    finally:
        driver.quit()

def verificar_e_notificar():
    novo_valor = obter_valor_produto()

    if not novo_valor:
        print("❌ Erro ao obter valor.")
        return

    try:
        with open(ULTIMO_VALOR_ARQUIVO, 'r') as f:
            valor_antigo = f.read().strip()
    except FileNotFoundError:
        valor_antigo = None

    if novo_valor != valor_antigo:
        print(f"💡 O preço mudou! Novo valor: {novo_valor}")
        with open(ULTIMO_VALOR_ARQUIVO, 'w') as f:
            f.write(novo_valor)
    else:
        print(f"ℹ️ Preço não mudou. Valor atual: {novo_valor}")

if __name__ == "__main__":
    verificar_e_notificar()
