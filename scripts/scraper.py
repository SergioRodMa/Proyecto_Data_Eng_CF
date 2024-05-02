import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time 
from datetime import date



custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}

       
def product_info(url):
    response = requests.get(url, headers=custom_headers)
    if response.status_code != 200:
        print("error de respuesta al request")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    try:
        title_name = soup.select_one("#productTitle")
        title_text = title_name.text.strip()
    except:
        title_text = None

    try:
        price_value = soup.select_one('span.a-offscreen')
        price = price_value.text 
    except:
        price = None

    try:
        review_elemnt=soup.select_one('#acrCustomerReviewText')
        review_number=review_elemnt.text.strip()
    except:
        review_number=None

    try:
        rating_element = soup.select_one("#acrPopover")
        rating_text = rating_element.attrs.get("title")
        rating = rating_text.replace("out of 5 stars", "")
    except:
        rating = None
    return {
        "title": title_text,
        "price": price,
        "rating": rating,
        "review_number": review_number,
        "url": url
        }   
    

def fetch_links(web_url):
    list_url = set()
    data_extracted = {"title":[], "price":[], "rating":[], "review_number":[],"url":[]}
    response = requests.get(web_url, headers=custom_headers)
    soup_links = BeautifulSoup(response.content, "html.parser")
    links = soup_links.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    for link in links:
        url_full = urljoin(web_url,link.get('href'))
        if url_full not in list_url:
            list_url.add(url_full)
            print(f"obteniendo informacion de {url_full[:100]}")
            time.sleep(3) 
            product_detail =  product_info(url_full)
            if product_detail:
                data_extracted["title"].append(product_detail["title"])
                data_extracted["price"].append(product_detail["price"])
                data_extracted["rating"].append(product_detail["rating"])
                data_extracted["review_number"].append(product_detail["review_number"])
                data_extracted["url"].append(product_detail["url"])
    return data_extracted

if __name__ == "__main__":
    today = date.today()
    amazon_url='https://www.amazon.com.mx/s?k=samsung+a54+desbloquedo&rh=n%3A9687460011&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'
    product_data=fetch_links(amazon_url)
    amazon_df = pd.DataFrame.from_dict(product_data)
    amazon_df['title']=amazon_df['title'].replace('', None)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df["Fecha"]=today
    amazon_df["price"]=amazon_df["price"].astype("string").str.replace('$','').str.replace(',', '')
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(amazon_df)
    
