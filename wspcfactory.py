import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
from datetime import date
from  IPython.core.display import clear_output



def obtain_urls(n_pages=2):
    target_urls = list()

    for i in range(1,n_pages+1):

        url = 'https://www.pcfactory.cl/notebooks?categoria=735&papa=636&pagina='+str(i)

        response =  requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        containers = soup.find_all('div',class_='center-caluga')

        for container in containers:

            target_urls.append('https://www.pcfactory.cl/' + container.find('a',class_='noselect')['href'])

   
    
    return target_urls

def obtain_data(target_urls):

    titles = list() 
    brand = list()
    processors = list() 
    graphics = list() 
    rams = list() 
    screens = list()
    storages = list()
    osystem = list()
    normal_price = list()
    sale_price = list()
    

    for url in target_urls:

        response =  requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        features = soup.find('div',class_='lista-contenido-ficha')
        try:
            list_features = features.find_all('li')
        except (AttributeError,IndexError):
            list_features = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]

        try:
            titles.append(soup.find('span',{'itemprop':'name'}).text)
        except (AttributeError,IndexError):
            titles.append(np.nan)
        try:
            brand.append(list_features[0].text)
        except (AttributeError,IndexError):
            brand.append(np.nan)
        try:
            processors.append(list_features[3].text)
        except (AttributeError,IndexError):
            processors.append(np.nan)
        try:
            rams.append(list_features[5].text)
        except (AttributeError,IndexError):
            rams.append(np.nan)
        try:
            storages.append(list_features[6].text)
        except (AttributeError,IndexError):
            storages.append(np.nan)
        try:
            screens.append(list_features[7].text)
        except (AttributeError,IndexError):
            screens.append(np.nan)
        try:
            graphics.append(list_features[8].text)
        except (AttributeError,IndexError):
            graphics.append(np.nan)
        try:
            osystem.append(list_features[9].text)
        except (AttributeError,IndexError):
            osystem.append(np.nan)
        try:
            normal_price.append(soup.find('div',class_='ficha_precio_normal').find('h2').text)
        except (AttributeError,IndexError):
            normal_price.append(np.nan)
        try:
            sale_price.append(soup.find('div',class_='ficha_precio_efectivo').find('h2').text)
        except (AttributeError,IndexError):
            sale_price.append(np.nan)

        lens = [len(titles),len(processors),len(rams),len(storages),len(screens),len(graphics),
               len(normal_price),len(sale_price),len(target_urls),len(osystem),len(brand)]



    data = pd.DataFrame({'compania':'Pc Factory','titulo': titles,'marca':brand,'procesador':processors,
                            'ram': rams,'tarjeta_grafica':graphics,'pantalla':screens,
                            'almacenamiento':storages,'sistema_operativo':osystem,
                            'precio_normal':normal_price,'precio_oferta':sale_price,'urls':target_urls})

    return data


def web_scraping_pc_factory(n_pages):

    print("Running Web Scraping....")
    clear_output(wait=True)
    
    target_urls = obtain_urls(n_pages)
    data = obtain_data(target_urls)

    print(f"Web Scraping finished:\nData extracted: {len(data)}")

    return data 



    








        











    

   








