import psycopg2
from psycopg2 import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("-headless")  # Executar o Chrome em modo headless (sem janela visível)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://economia.uol.com.br/cotacoes/cambio/")
time.sleep(2)

data_hora = datetime.now() 
data = data_hora.strftime("%Y-%m-%d")
print(data)
hora = data_hora.strftime("%H:%M:%S")
print(hora)

cotacao_dolar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/section[1]/div[1]/a/div/span[2]').text
cotacao_dolar = float (cotacao_dolar.replace(',', '.'))
print(cotacao_dolar)

try:
    connection = psycopg2.connect(user="avnadmin",
                                    password="AVNS_I2YSg3hf2GFrMM8X7eZ",
                                    host="pg-126b320f-ncgaloni-ec04.d.aivencloud.com",
                                    port="21577",
                                    database="dbCotacoes")
    cursor = connection.cursor()

    cursor.execute('CALL inserir_cotacao_dolar(%s, %s, %s)', (data, hora, cotacao_dolar))
    connection.commit()
    print("Dados inseridos com sucesso!")

except (Exception, Error) as error:
    print("Erro ao inserir os dados:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexão encerrada.")
