import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email =os.getenv("CORREO")
password =os.getenv("PASSWORD")
to_email=os.getenv("TO_EMAIL")


url = "https://www.amazon.com/-/es/pulgadas-i5-1135G7-Graphics-Windows-15-dy2024nr/dp/B09FXFDGN3/ref=sr_1_3?qid=1641588059&s=computers-intl-ship&sr=1-3"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "es-EC,es-419;q=0.9,es;q=0.8,en;q=0.7"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")

price = float(soup.find(name="span", class_="a-price-whole").text)
title = soup.find(name="span", id="productTitle").string

print(f"El precio actual de tu producto es: ${price}")
# precio en dolares us
precio_deseado = 590

if price < precio_deseado:

    contenido = f"El producto:{title.lstrip()}\n\nAhora mismo vale: US${price}\n\nVe a {url}\n\nY compralo ya!"
    msg=f"Subject:Amazon Price Alert!\n\n{contenido}".encode('utf-8')
    print(msg)
    with smtplib.SMTP("smtp.office365.com:587") as conexion:
        conexion.starttls()
        conexion.login(email, password)
        conexion.sendmail(from_addr=email, to_addrs=to_email,msg=msg)
    print("Correo enviado")