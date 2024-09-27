# import psycopg2
# from psycopg2 import Error
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from datetime import datetime
# import time

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("-headless")  # Executar o Chrome em modo headless (sem janela visível)
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://economia.uol.com.br/cotacoes/cambio/")
# time.sleep(2)

# data_hora = datetime.now() 
# data = data_hora.strftime("%Y-%m-%d")
# print(data)
# hora = data_hora.strftime("%H:%M:%S")
# print(hora)

# cotacao_dolar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/section[1]/div[1]/a/div/span[2]').text
# cotacao_dolar = float (cotacao_dolar.replace(',', '.'))
# print(cotacao_dolar)

# try:
#     connection = psycopg2.connect(user="admin",
#                                     password="qyXcctOHObv9k1OIXHCRYTakaIhdiDFn",
#                                     host="dpg-crr01q2j1k6c73e7jj7g-a.oregon-postgres.render.com",
#                                     port="5432",
#                                     database="db_teste_0ssl")
#     cursor = connection.cursor()

#     cursor.execute('CALL inserir_cotacao_dolar(%s, %s, %s)', (data, hora, cotacao_dolar))
#     connection.commit()
#     print("Dados inseridos com sucesso!")

# except (Exception, Error) as error:
#     print("Erro ao inserir os dados:", error)

# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Conexão encerrada.")

from datetime import datetime
from selenium import webdriver
import psycopg2

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

url = 'https://www.google.com/finance/quote/USD-BRL?sa=X&sqi=2&ved=2ahUKEwjHod2jweyEAxV4LrkGHTzSCNsQmY0JegQIDhAv'
driver.get(url)

dolar_element = driver.find_element('xpath', "/html/body/c-wiz[2]/div/div[4]/div/main/div[2]/div[1]/c-wiz/div/div[1]/div/div[1]/div/div[1]/div/span/div/div")

dolar = float(dolar_element.text.replace(',', '.'))

data_hora_atual = datetime.now()
data_formatada = data_hora_atual.strftime("%m/%d/%Y")
hora_formatada = data_hora_atual.strftime("%H:%M")

print(f'Na data {data_formatada} e no horário {hora_formatada} um dólar está cotado em R${dolar}')

dados = {'cotacao': [dolar], 'data': [data_formatada], 'hora': [hora_formatada]}

user="admin",
password="qyXcctOHObv9k1OIXHCRYTakaIhdiDFn",
host="dpg-crr01q2j1k6c73e7jj7g-a.oregon-postgres.render.com",
port="5432",
database="db_teste_0ssl"

try:
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    
    # sql_create_table  = """
    # CREATE TABLE cotacao_dolar (
	#     id SERIAL PRIMARY KEY,
	#     data DATE,
	#     hora TIME,
	#     cotacao DECIMAL(10,2)
    # );
    # """

    # cursor.execute(sql_create_table)

    # sql_create_procedure = """
    # CREATE OR REPLACE PROCEDURE inserir_cotacao_dolar(
    # data_in DATE,
    # hora_in TIME,
    # cotacao_in DECIMAL(10,2)
    # )
    # LANGUAGE SQL
    # AS $$
    # INSERT INTO cotacao_dolar (data, hora, cotacao)
    # VALUES (data_in, hora_in, cotacao_in);
    # $$;
    # """

    #cursor.execute(sql_create_procedure)

    cursor.execute("CALL inserir_cotacao_dolar(%s, %s, %s);", (data_formatada, hora_formatada, dolar))

    connection.commit()

    cursor.execute("SELECT * FROM cotacao_dolar;")
    records = cursor.fetchall()
    
    for row in records:
        print(row)
        
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL:", error)
