def description(company):
    response = requests.get(f'https://www.morningstar.com/stocks/xnse/{company}/quote')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Gives summary for the company being scraped
        description = soup.find_all('span', {'itemprop': 'description'})[0].text
        print(description)
    else:
        print("Error retrieving the information")

def exectuive(company):
    response = requests.get(f"https://www.morningstar.com/stocks/xnse/{company}/executive")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Gives summary for the company being scraped
        print(soup)
        with open("soup.txt", "w") as f:
            f.write(soup.prettify())
        executives = soup.find_all('h3', class_='mds-executive__name')
        print(executives)
    else:
        print("Error retrieving the information")

def ownership(comp):
    response = requests.get(f"https://www.morningstar.com/stocks/xnse/{comp}/ownership")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Gives summary for the company being scraped
        print(soup)
        with open("owner.txt", "w") as f:
            f.write(soup.prettify())
        executives = soup.find_all('h3', class_='mds-executive__name')
        print(executives)
    else:
        print("Error retrieving the information")
    
