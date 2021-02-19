import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
os.makedirs('Supremenewyork/', exist_ok=True)
if os.path.exists("links.txt"):
    os.remove("links.txt")

with open('Supremenewyork/all_data.csv', 'w', encoding='utf-8') as file:
    file.write('Product Name, Price, Description,')

def download_image(url,product_name,sub_title,index):
    try:
        dirName = 'Supremenewyork/'+product_name.strip()+'/' 
        os.makedirs(dirName, exist_ok=True)
        file_path = dirName + product_name.strip() + '_'+sub_title.strip()+'_' + str(index) + '.jpg'
        print(file_path)
        if os.path.isfile(file_path):
            print('already exist ...')
        else:
            print('Processing '+product_name+" ......")
            urllib.request.urlretrieve(url,file_path)
    except:
        print("An exception occurred")

# Variable
title  = ''
brand = ''
price = ''
features =''
description = ''
img = ''
category = ''
total_products_page_links = []
img_urls = []
record = []

#Access The page
r =  requests.get('https://www.supremenewyork.com/previews/springsummer2021/all',headers=headers)

if r.status_code == 200:    
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    list_all_links = soup.select('.inner-article a')
    for l in list_all_links:
        total_products_page_links.append('https://www.supremenewyork.com'+l['href'])

with open('links.txt', 'a+', encoding='utf-8') as file:
    file.write('\n'.join(total_products_page_links))

with open('links.txt',encoding='utf-8') as f:
    lines = f.readlines()
    count = 0
    for link in lines:

        #Access The page
        r =  requests.get(link.replace('\n', '').strip(), headers=headers)
        
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')

            item_name = soup.find("h1", {"itemprop" : "name"})
            item_dec = soup.find("p", {"itemprop": "description"})
            item_price = soup.find("span", {"itemprop": "price"})
            item_modal = soup.find("p", {"itemprop": "model"})

            # IMg  
            img_sec = soup.select('figure img')
            if img_sec and img_sec[0]:
                img = 'https:'+img_sec[0]['src']

            #sub Titile
            if item_modal:
                sub_title = item_modal.text.replace(',', '').strip().replace('/',' ')
            # Title 
            if item_name:
                title = item_name.text.replace(',', '').strip().replace('/',' ')
                category = item_name['data-category']
            # Description 
            if  item_dec:
                description = item_dec.text.replace(',', '').strip().replace('/',' ')

            #price
            if item_price:
                price = item_price.text.replace(',', '').strip()
            # get images
            #Access li image
            parent = soup.find('a', {'class' :'selected'})
            if parent:
                parent = parent.find_parent()
                parent = parent.select('img')
                for i in parent:
                    img_urls.append('https:'+i['src'].replace('sw','zo'))   
            else:
                # for last product havn't li .selected
                parent = soup.find('figure')
                parent = parent.find('img')
                img_urls.append('https:'+parent['src'])

            record.append(title)
            record.append(price)
            record.append(description)

            # Store Data in CSV
            with open('Supremenewyork/all_data.csv', 'a+', encoding='utf-8') as file:
                file.write('\n')
                file.write(','.join(record))
            record = []
            print(title)
            #Category
            count = 0
            for index, img_url in enumerate(img_urls, start=0):
                count = count + 1 
                download_image(img_url,title, sub_title,count )
            img_urls = []
            # count = 0
                
os.remove("links.txt")
print('End....')
