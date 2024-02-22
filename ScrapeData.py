import pandas as pd
import requests
from bs4 import BeautifulSoup


def search_query(query):
    api_key = "AIzaSyAL4Qcr-1NN4ORudhZFAFwq90iXskgqoYA"
    cx = "f1baa89bdf454472e"
    num_results = 5
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}&num={num_results}"
    response = requests.get(url)
    data = response.json()
    search_results = data.get("items", [])
    return search_results


def scrape_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = '\n'.join(paragraph.get_text() for paragraph in paragraphs)
        return text_content
    except Exception as e:
        print(f"Error scraping content from {url}: {e}")
        return None


def structure_data(data):
    columns = ["Wikipedia", "MPDV", "LV", "CEO", "Crunchbase"]
    df = pd.DataFrame([data], columns=columns)
    return df


def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)


def start(query):
    results = search_query(query)
    links = []
    for i in results:
        links.append(i["link"])

    scraped_data = []
    for link in links:
        data = scrape_content(link)
        scraped_data.append(data)

    df = structure_data(scraped_data)
    save_to_csv(df, "company_info.csv")
    text = '\n'.join(scraped_data)
    return text


