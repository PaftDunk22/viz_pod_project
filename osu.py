import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas

def scrape_page(page_number):
    url = f"https://osu.ppy.sh/rankings/osu/country?page={page_number}#scores"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr', class_='ranking-page-table__row') 

    country_data = []
    
    for row in rows:
        try:
            country_name = row.find_all('td', class_='ranking-page-table__column')[1].text.strip()
            active_users = row.find_all('td', class_='ranking-page-table__column')[2].text.strip()
            total_score = row.find_all('td', class_='ranking-page-table__column')[3].text.strip()
            ranked_score = row.find_all('td', class_='ranking-page-table__column')[4].text.strip()
            total_play_count = row.find_all('td', class_='ranking-page-table__column')[5].text.strip()
            performance = row.find_all('td', class_='ranking-page-table__column')[6].text.strip()

            country_data.append([country_name, active_users, total_score, ranked_score, total_play_count, performance])
        except Exception as e:
            print(f"Error scraping row: {e}")
    
    return country_data

csv_filename = "osu_country_rankings.csv"
csv_file = open(csv_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Country', 'Active Users', 'Total Score', 'Ranked Score', 'Total Play Count', 'Performance'])

for page in range(1, 6): 
    print(f"Scraping page {page}...")
    country_data = scrape_page(page)
    
    if country_data:  
        csv_writer.writerows(country_data)
    else:
        print(f"No data found on page {page}.")
    
    time.sleep(2)

    
csv_file.close()

df = pandas.read_csv(csv_filename)

df["Active Users"] = df["Active Users"].str.replace(",", "").astype(int)

df = df.sort_values("Active Users", ascending=False)

df.to_csv(csv_filename, index=False)

print("Data has been saved to osu_country_rankings.csv")
