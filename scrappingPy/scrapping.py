from bs4 import BeautifulSoup #untuk mem-parse data html
import requests #untuk mengambil http request
import pandas as pd #untuk membuat,menganalsis dan memvisualisasi
import numpy as np #untuk melakukan operasi aritmatika dan manipulasi pada array data

# fungsi untuk mengekstrak title dari produk
def judul(soup):
    try:
        # Outer Tag Object
        title = new_soup.find('span',attrs={"id":"productTitle"})
        
        # Inner NavigatableString Object
        title_value = title.text.strip()

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def harga(soup):
    try:
        harga = soup.find("span", attrs={"class": "a-offscreen"}).text.strip()
    except AttributeError:
        harga = ""
    return harga

def rating(soup):
    try:
        rating = soup.find("span", attrs={"class": "a-icon-alt"}).text.strip()
    except AttributeError:
        rating = ""
    return rating
if __name__=='__main__':
    # tambahkan user agent
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})
    # url dari web yang ingin di scrapping
    URL ="https://www.amazon.com/s?k=smart+watch&ref=nb_sb_ss_ts-doa-p_1_4"
    webpage = requests.get(URL,headers=HEADERS)
    soup = BeautifulSoup(webpage.content,"html.parser")
    links = soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []
    # looping data
    for link in links:
        links_list.append(link.get('href'))
    d = {"title":[],"harga":[],"review":[]}
    
    # looping data dengan format untuk di display
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS,)
        new_soup = BeautifulSoup(new_webpage.content,"html.parser")
        d["title"].append(judul(new_soup))
        d['harga'].append(harga(new_soup))
        d["review"].append(rating(new_soup))
        
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].fillna(np.nan)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv",header=True,index=False)
    amazon_df
 