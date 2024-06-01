import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_tv_details(url):
    res = get(url, headers=headers)
    
    if res.status_code != 200:
        print("Une erreur est survenue lors du chargement de la page", url, res.status_code)
        return
    
    soup = bs(res.text, "html.parser")
    container = soup.find("div", class_ = "listing-item")

    if container == None:
        print("Il n'y a pas de contenu sur la page:", url)
        return;

    img = container.find("img", class_ = "gallery__image__resource vh-img")
    img = "NULL" if img == None else img["src"]

    # print("Image:", img)

    price = soup.find("span", class_ = "listing-card__price__value")
    price = "NULL" if price == None else price.text.replace("\n", "").strip()

    address = ""
    addr1 = soup.find('span', class_='listing-item__address-location').text.replace("\n", "").strip()
    addr2 = soup.find('span', class_='listing-item__address-region').text.replace("\n", "").strip()
    address = f"{addr1} {addr2}"

    details_div = soup.find('dl', class_='listing-item__properties')
    #   print(details_div)
    
    details = details_div.find_all('dd')

    # print("CURRENT URL:", url)
    item_details = [detail.text.replace("\n", "").strip() for detail in details]
    state = details[0]
    state = "NULL" if state == None else state.text.replace("\n", "").strip()
    brand = details[1] if len(details) > 1 else None
    brand = "NULL" if brand == None else brand.text.replace("\n", "").strip()

    data = {
        "Image_lien": img,
        "Prix": price,
        "Adresse": address,
        "Etat": state,
        "Marque": brand,
        "Details": item_details
    }
    
    return data

def scrape_details(url):
    res = get(url, headers=headers)
    
    if res.status_code != 200:
        print("Une erreur est survenue lors du chargement de la page", url, res.status_code)
        return
    
    soup = bs(res.text, "html.parser")
    container = soup.find("div", class_="listing-item")
    
    if container is None:
        print("Il n'y a pas de contenu sur la page:", url)
        return
    
    img = container.find("img", class_="gallery__image__resource vh-img")
    img = "NULL" if img is None else img["src"]
    
    price = soup.find("span", class_="listing-card__price__value")
    price = "NULL" if price is None else price.text.replace("\n", "").strip()
    
    address = ""
    addr1 = soup.find('span', class_='listing-item__address-location').text.replace("\n", "").strip()
    addr2 = soup.find('span', class_='listing-item__address-region').text.replace("\n", "").strip()
    address = f"{addr1} {addr2}"
    
    details_div = soup.find('dl', class_='listing-item__properties')
    details = details_div.find_all('dd')
    
    state = details[0].text.replace("\n", "").strip()
    brand = details[1].text.replace("\n", "").strip()
    item_details = [detail.text.replace("\n", "").strip() for detail in details]
    
    data = {
        "Image_lien": img,
        "Prix": price,
        "Adresse": address,
        "Etat": state,
        "Marque": brand,
        "Details": item_details
    }
    
    return data

def scrape_pages(url, pages, tv=False):
    urls = []
    items = []
    current_page = 1

    print("Scraping pages from", url, "with", pages, "pages")
    
    while url and current_page <= pages:
        url_to_scrape = f"{url}?page={current_page}"
        res = get(url_to_scrape, headers=headers)
        
        if res.status_code != 200:
            print("Une erreur est survenue lors du chargement de la page", url, res.status_code)
            return
        
        print("Le chargement de la page s'est bien passé", url_to_scrape, res.status_code)
        soup = bs(res.text, "html.parser")
        containers = soup.find_all("div", class_="listings-cards__list-item")
        
        if len(containers) == 0:
            return
        
        for container in containers:
            item_container = container.find("div", class_="listing-card listing-card--tab listing-card--has-contact listing-card--has-content")
            if item_container:
                href = item_container.find("a", class_="listing-card__inner")["href"]
                urls.append(href)
        
        current_page += 1
    
    for url in urls:
        if tv:
            items.append(scrape_tv_details(url))
        else:
            items.append(scrape_details(url))
    
    return items


def test(selected_page):
    df = pd.DataFrame()
    for p in range(1, selected_page+1):
        url=f'https://dakarvente.com/index.php?page=annonces_categorie&id=13&sort=&nb={p}'
        res = get(url)
        # soup = bs(res.text, "html.parser")
        bsoup = bs(res.text, "html.parser")#stocker le code html dans un objet bs
        conteneurs = bsoup. find_all('article', class_='col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3 post')
        data= []

        for conteneur in conteneurs:
            try:
                link = 'https://dakarvente.com/annonces-categorie-terrains-vendre-13.html' + conteneur. find('a', class_="") ['href']
                if link is not None:#Sauter Lien Location vente auto
                        res_c = get(link)
                        bsoup_c = bs(res_c.text, "html.parser")
                inf_gen = conteneur. find('div', class_='item-inner mv-effect-translate-1 mv-box-shadow-gray-1'). find_all('div')
                prix = inf_gen[3]. text.replace(" ", "").replace("FCFA", "").strip()
                details = inf_gen[4].text.strip()
                adresse = inf_gen[5].text.strip()
                image = conteneur. find ('img' )['src']
                dico = {
                    'V1': details,
                    'V2(FCFA)': prix,
                    'V3': adresse,
                    'V4': image
                }

                data. append (dico)
            except:
                pass
                
        df1 = pd. DataFrame(data)
        df = pd. concat ([df, df1],axis = 0). reset_index(drop = True)

    return df