# %%
from autoscraper import AutoScraper

#%%
#amazon_url="https://www.amazon.com.mx/s?k=iphones"
amazon_url="https://www.amazon.com.mx/s?k=samsung+a54+128gb+desbloqueado&rh=n%3A9687460011&dc&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=a9_sc_1"

wanted_list=["$6,372.20","SAMSUNG Galaxy A54 5G 6+128GB Verde","4.4 de 5 estrellas","https://www.amazon.com.mx/Samsung-Galaxy-Awesome-Violet-Desbloqueado/dp/B0C3K5XZPF/ref=sr_1_3?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.GeNaTTyig5qo81M524oildk0dk30MhuTu8Y1OuwZn6XWTjluWWQiWklXs_1zKv9qo76_NdtiF8C4wl6r6OH0bavzs2D2LQWVBUoPzSHPVJuI5ouO7TrrnhBJx1HBPXMtt3jfhgVOW9oYK1EaeH4H69j3gKdO3HVtgOZvS4dkSIRIWjIlVmhQSPnTIWDwySwqk7RQOgFCUj2_MW4dyygDMkm7SsIyAHRlINbUigebplrJxFdi86FT6qGJQ6ujVFtrO0IwxpL8zRIhznG49vPYqOrYOGWBC9-IizylTJHRsS8.IetWaPjH5Xy3HoHmNDu3qFfO7EXhfaN5yaP08yR8dmU&dib_tag=se&keywords=samsung+a54+128gb+desbloqueado&qid=1712633782&s=electronics&sr=1-3&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47"]

scraper=AutoScraper()
result=scraper.build(amazon_url,wanted_list)

sr=scraper.get_result_similar(amazon_url,grouped=True)

# %%
import requests
from bs4 import BeautifulSoup
url = amazon_url



custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}

response = requests.get(url, headers= custom_headers)
print(response.text)
soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

# Store the links
links_list = []

# Loop for extracting links from Tag Objects
for link in links:
    links_list.append(link.get('href'))
# %%
products="https://www.amazon.com.mx" + links_list[3]
response = requests.get(products, headers=custom_headers)
soup = BeautifulSoup(response.text, 'lxml')
# %%
title_element = soup.select_one('#productTitle')
price_element = soup.select_one('span.a-offscreen')
rating_element = soup.select_one('#acrPopover')
rating_text = rating_element.attrs.get('title')
# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
# custom_headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
#     'Accept-Language': 'da, en-gb, en',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Referer': 'https://www.google.com/'
# }


custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}

amazon_url="https://www.amazon.com.mx/s?k=samsung+a54+128gb+desbloqueado&rh=n%3A9687460011&dc&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=a9_sc_1"
response = requests.get(amazon_url, headers=custom_headers)
print(response.status_code)
print(response.text)
list_url = set()
soup_links = BeautifulSoup(response.content, "html.parser")
links = soup_links.find_all("a", attrs={'class':'a-link-normal s-no-outline'})


for link in links:
    url_full = urljoin(amazon_url,link.get('href'))
    if url_full not in list_url:
        list_url.add(url_full)
        print(f"obteniendo informacion de {url_full[:100]}")
        
        
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
            product_detail =  product_info(url_full)
            if product_detail:
                data_extracted["title"].append(product_detail["title"])
                data_extracted["price"].append(product_detail["price"])
                data_extracted["rating"].append(product_detail["rating"])
                data_extracted["review_number"].append(product_detail["review_number"])
                data_extracted["url"].append(product_detail["url"])
    return data_extracted

if __name__ == "__main__":
    
    
    
    

    