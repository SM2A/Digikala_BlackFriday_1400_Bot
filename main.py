import os
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings()

pages = ['https://www.digikala.com/treasure-hunt/products/']

for p in range(47):
    pages.append(f'https://www.digikala.com/treasure-hunt/products/?sortby=4&pageno={p + 1}')

i = 0
j = 0

for p in pages:
    i += 1
    print(f'Page {i} ********************************************************')
    page = requests.get(url=p, verify=False)
    parser = BeautifulSoup(page.text, "html.parser")
    products_list = parser.find_all("div", {"class": "c-product-box"})
    for product in products_list:
        try:
            code = product.find_all('a', {'class': 'c-product-box__img'})[0].get('data-adro-ad-click-id')
            URL = f'https://www.digikala.com/product/{code}'
            j += 1
            print(f'Product {j}')
            try:
                result = requests.get(url=URL, verify=False)
                parser = BeautifulSoup(result.text, "html.parser")
                gallery = parser.find_all("div", {"class": "c-remodal-gallery__thumbs js-official-thumbs"})
                photos = BeautifulSoup(str(gallery), "html.parser")
                for img in photos.select('div'):
                    text = (img.get('class')[0] + img.get('class')[1])
                    if (img.get('class')[0] + img.get('class')[1]) == 'c-remodal-gallery__thumbjs-image-thumb':
                        src = img.find('img').get('data-src')
                        get_time = requests.get(src)
                        date = get_time.headers['Last-Modified']
                        if 'Sun, 28 Nov' in date:
                            print("-----------------------------------------------------------------------------------")
                            print(URL)
                            print(get_time.headers['Last-Modified'])
                            img_link = ""
                            for c in src:
                                if c != '?':
                                    img_link += c
                                else:
                                    break
                            discount_code = requests.get(img_link)
                            file = open(f'{code}.jpg', 'wb')
                            file.write(discount_code.content)
                            file.close()
                            os.startfile(f'{code}.jpg')
                            print("-----------------------------------------------------------------------------------")
            except:
                print(f"ERROR : {URL}")
        except:
            print(product)
