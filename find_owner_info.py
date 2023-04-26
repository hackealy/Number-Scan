import phonenumbers
import requests
from bs4 import BeautifulSoup
import re

def find_owner_info(number):
    # Validando o número de telefone
    try:
        parsed_number = phonenumbers.parse(number, "BR")
        if not phonenumbers.is_valid_number(parsed_number):
            print("Número de telefone inválido!")
            return
    except phonenumbers.phonenumberutil.NumberParseException:
        print("Número de telefone inválido!")
        return
    
    # Obtendo informações da lista telefônica
    url = f"https://www.guiamais.com.br/busca/telefonica/{number}"
    response = requests.get(url)
    if response.status_code == 404:
        print("Número não encontrado na lista telefônica.")
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find("h1", {"class": "listing-title"}).text.strip()
        address = soup.find("div", {"class": "address"}).text.strip()
        print(f"Nome do proprietário: {name}")
        print(f"Endereço: {address}")
    
    # Obtendo informações da API do Truecaller
    url = f"https://api.truecaller.com/v1/search?countryCode=BR&phoneNumber={number}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/B12",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            spam = "Sim" if data["data"][0]["spam"] else "Não"
            print(f"Spam: {spam}")
    
    # Obtendo informações do site Quem Perturba
    url = f"https://quemperturba.com.br/{number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find("span", {"class": "h1"}).text.strip()
        address = soup.find(text=re.compile("Endereço:")).next_element.text.strip()
        spam = soup.find(text=re.compile("É um golpe")).parent.text.strip()
        print(f"Nome do proprietário (Quem Perturba): {name}")
        print(f"Endereço (Quem Perturba): {address}")
        print(f"Golpe (Quem Perturba): {spam}")

# Exemplo de uso
find_owner_info("+5511987654321")
