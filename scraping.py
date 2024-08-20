from flask import Flask, render_template
# @ author Devang Sharma
import requests
from bs4 import BeautifulSoup
import re
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from flask import request
import firebase_admin
from firebase_admin import credentials, storage
import os

cred = credentials.Certificate("./credence-data-firebase-adminsdk-9s5se-2441a8845e.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'credence-data.appspot.com'})
bucket = storage.bucket()



PATH = "/Users/devangsharma/Downloads/chromedriver-mac-arm64"

driver = webdriver.Chrome()

# Open the URL
app = Flask(__name__)

@app.route("/main", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        q = request.form['query']
        exec_sel(q)
        news_sel(q)
        owner_sel(q)
        # news_sel(q)
        # owner_sel(q)
        comp = ""
        for c in q[::-1]:
            if c == "/":
                break
            else:
                comp += c
        owner_file_name = f"owner_{comp}.csv"
        news_file_name = f"news_{comp}.txt"
        exec_file_name = f"executives_{comp}"
        blob_e = bucket.blob(exec_file_name)
        blob_o = bucket.blob(owner_file_name)
        blob_n = bucket.blob(news_file_name)
        blob_e.upload_from_filename(exec_file_name, content_type="text/plain")
        blob_o.upload_from_filename(owner_file_name)
        blob_n.upload_from_filename(news_file_name)
        blob_e.make_public()
        blob_n.make_public()
        blob_o.make_public()
        links = {'exec': blob_e.public_url, 'owner': blob_o.public_url, 'news': blob_n.public_url}
        return render_template('index.html', **links)
    else:
        return render_emplate('index.html')

# @app.route("/scrape", methods=["POST"])
# def scrape():
    
#     return f"{blob.public_url}"

    
def exec_sel(base):
    driver.get(f"{base}/executive")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="boardOfDirectors"]'))
    )
    button.click()

    time.sleep(3)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    with open("exec_sel.txt", "w") as f:
        f.write(soup.prettify())
    person_names = soup.find_all('span', class_='person-name')
    titles = soup.find_all('span', class_="title")
    comp = ""
    for c in base[::-1]:
        if c == "/":
            break
        else:
            comp += c
    # os.makedirs(f'./executives_{base}', exist_ok=True)
    with open(f"executives_{comp}", "w") as f:
        f.write("Name, Title")
        for i in range(len(titles)):
            f.write(f'{person_names[i].text}, {titles[i].text}')


def owner_sel(base):
    driver.get(f"{base}/ownership")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="funds"]'))
    )
    button.click()

    time.sleep(5)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    with open("owner_sel.txt", "w") as f:
        f.write(soup.prettify())
    table = soup.find('table')

    rows = table.find_all('tr')
    comp = ""
    for c in base[::-1]:
        if c == "/":
            break
        else:
            comp += c
    with open(f'owner_{comp}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.get_text(strip=True) for col in cols]
            writer.writerow(cols)

def news_sel(base):
    driver.get(f"{base}/news")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    news = soup.find_all('li', class_="stock-news__list-item__mdc")
    names = []
    links = []
    if news:
        for i in range(len(news)):
            names.append(news[i].find('a').text)
            temp = news[i].find('a').get('href')
            links.append(f'https://www.morningstar.com{temp}')
    
    comp = ""
    for c in base[::-1]:
        if c == "/":
            break
        else:
            comp += c
            
    with open(f'news_{comp}.txt', 'w') as file:
        if len(names) == 0:
            file.write('No news articles found on morningstar')
        else:
            for i in range(len(names)):
                file.write(f"{names[i]}, {links[i]}\n")

    

if __name__ == "__main__":
    # company = input("What company do you want to request: ")
    # description(company)
    # exectuive('auropharma')
    # ownership('auropharma')
    # exec_sel('auropharma')
    # owner_sel('auropharma')
    app.run(debug=True)


"""
Things to do:
News articles, with links and headings
Share holding:
    Funds, Instituitions Top 10 in table format
Executive:
    Need name, designation and any other information
    Year of appointment
Try finding widgets/apis from news sites such as investing.com, motley fool etc.
Compile information, to 
"""


"""
Export data from financials 

Summary, 5 sections under profile
Competitors

"""
"""
Financials (all three, income statements, balance sheet, cash flow)
about us
"""