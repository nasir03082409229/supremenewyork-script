import requests
from bs4 import BeautifulSoup
import os
import json
import urllib.request
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
os.makedirs('Supremenewyork/', exist_ok=True)
if os.path.exists("links.txt"):
    os.remove("links.txt")

with open('Supremenewyork/all_data.csv', 'w', encoding='utf-8') as file:
    file.write('Title, Caption,')

def download_image(url,product_name,category,index):
    # try:
        url =   "https://"+ url[2:]
        product_name = product_name.replace('/',' ')
        product_name = product_name.replace('<br>','')
        dirName = 'Supremenewyork/'+category+'/'+product_name.strip()+'/' 
        os.makedirs(dirName, exist_ok=True)
        file_path = dirName + product_name.strip() +'_' + str(index) + '.jpg'
        if os.path.isfile(file_path):
            print('already exist ...')
        else:
            print('Processing '+url)
            print('Processing '+product_name)
            urllib.request.urlretrieve(url,file_path)
    # except:
    #     print("An exception occurred")

# Variable
title  = ''
caption = ''
category = ''

total_products_page_links = []
record = []

#Access The page
r =  requests.get('https://www.supremenewyork.com/previews/springsummer2021/',headers=headers)
if r.status_code == 200:    
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    list_all_links = soup.select('#container a')
    for l in list_all_links:
        total_products_page_links.append('https://www.supremenewyork.com'+l['href'])

with open('links.txt', 'a+', encoding='utf-8') as file:
    file.write('\n'.join(total_products_page_links))

with open('links.txt',encoding='utf-8') as f:
    lines = f.readlines()
    count = 0
    for link in lines:
        category = link.split('/')[5]
        #Access The page
        r =  requests.get(link.replace('\n', '').strip(), headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml') 
            product_arr = json.loads(soup.select('#container')[0]['data-images'])
            record = [product_arr[0]['title'], product_arr[0]['caption'] if product_arr[0]['caption'] is not None else "" ]
            # Store Data in CSV
            with open('Supremenewyork/all_data.csv', 'a+', encoding='utf-8') as file:
                file.write('\n')
                file.write(','.join(record))
            index = 0
            for one_product in product_arr:
                index = index + 1
                download_image(one_product['imageUrl'],one_product['title'],category,index)

os.remove("links.txt")
print('-x-x-x-x-x-x- Scraping Complete -x-x-x-x-x-x-')