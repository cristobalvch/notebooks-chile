from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import numpy as np
from IPython.core.display import clear_output
import requests
from bs4 import BeautifulSoup



def obtain_urls(n_pages):
    
    print("Running Web Scraping....\n")
    target_urls = list()
    driver = webdriver.Chrome(ChromeDriverManager().install())

    for i in range(1,n_pages+1):

        url = 'https://www.falabella.com/falabella-cl/category/cat70057/Notebooks?facetSelected=true%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue&f.product.attribute.Tipo=Gamers%3A%3AMacbooks%3A%3ANotebooks&page='+str(i)
        
        driver.get(url)
        containers = driver.find_elements_by_xpath('//*[@id="testId-searchResults-products"]/div')

        for container in containers:

            url = container.find_element_by_tag_name('a')
            target_urls.append(str(url.get_attribute('href')))

    
    driver.close()

    return target_urls


def obtain_data(target_urls):

    titles = list() 
    processors = list() 
    graphics = list() 
    rams = list() 
    screens = list()
    storages = list()
    normal_price = list()
    sale_price = list()
    systems = list()
    brand = list()
    

    for url in target_urls:

        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        list_features = soup.find_all('td',class_='jsx-428502957 property-value')
        name_features = soup.find_all('td',class_='jsx-428502957 property-name')
        
        
        titles.append(soup.find('div',class_='jsx-3686231685 product-name fa--product-name').text)

        prices = soup.find_all('div',class_='jsx-1904860942 cmr-icon-container')

        brand.append(soup.find('a',class_='jsx-3572928369 product-brand-link').text)

        try:
            sale_price.append(prices[0].find('span').text)
        except (AttributeError, IndexError):
            sale_price.append(np.nan)
        
        try:
            normal_price.append(prices[1].find('span').text)
        except (AttributeError, IndexError):
            normal_price.append(np.nan)

   
        for i in range(len(name_features)):
            
            if name_features[i].text =='Procesador':
                processors.append(list_features[i].text)
                while len(processors) != len(titles):
                    processors.append(np.nan)
            
            if name_features[i].text == 'Tamaño de la pantalla':
                screens.append(list_features[i].text)
                while len(screens) != len(titles):
                    screens.append(np.nan)
                
            if name_features[i].text == 'Memoria RAM':
                rams.append(list_features[i].text)
                while len(rams) != len(titles):
                    rams.append(np.nan)
                
            if name_features[i].text == 'Modelo tarjeta de video':
                graphics.append(list_features[i].text)
                while len(graphics) != len(titles):
                    graphics.append(np.nan)
                
            if name_features[i].text == 'Unidad de estado sólido SSD':
                storages.append(list_features[i].text)
                while len(storages) != len(titles):
                    storages.append(np.nan)

            if name_features[i].text == 'Sistema operativo':
                systems.append(list_features[i].text)
        
        while len(systems) != len(titles):
            systems.append(np.nan)
            
        
            

    data = pd.DataFrame({'compania':'Falabella','titulo': titles,'marca':brand,'procesador':processors,
                            'ram': rams,'tarjeta_grafica':graphics,'pantalla':screens,
                            'almacenamiento':storages,'sistema_operativo':systems,
                            'precio_normal':normal_price,'precio_oferta':sale_price,'urls':target_urls})
    return data


def web_scraping_falabella(n_pages):

    
    clear_output(wait=True)
    
    target_urls = obtain_urls(n_pages)
    data = obtain_data(target_urls)

    print(f"Web Scraping finished:\nData extracted: {len(data)}")

    return data









    



