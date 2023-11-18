import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    for product in soup.find_all('div', class_='product-item'):
        name = product.find('a', class_='product-title')
        reviews = product.find('span', class_='count')
        price = product.find('span', class_='price')

        if name and reviews and price:
            name = name.text.strip()
            reviews = reviews.text.strip()
            price = price.text.strip()

            products.append({'Name': name, 'Reviews': reviews, 'Price': price})

    return products


def filter_discounted_products(products):
    return [product for product in products if 'знижка' in product['Name'].lower()]


def save_to_txt(products, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for product in products:
            file.write(f"{product['Name']}\nКількість відгуків: {product['Reviews']}\nЦіна: {product['Price']}\n\n")


def save_to_excel(products, filename):
    df = pd.DataFrame(products)
    df.to_excel(filename, index=False)


categories = [
    'https://allo.ua/ua/televizory/',
    'https://allo.ua/ua/zarjadnye-stancii/',
    'https://allo.ua/ua/products/mobile/',
    'https://allo.ua/ua/products/internet-planshety/',
    'https://allo.ua/ua/products/notebooks/'
]

all_products = []

for category in categories:
    all_products.extend(parse_product(category))

save_to_txt(all_products, 'all_products.txt')
save_to_excel(all_products, 'all_products.xlsx')

discounted_products = filter_discounted_products(all_products)

save_to_txt(discounted_products, 'discounted_products.txt')
save_to_excel(discounted_products, 'discounted_products.xlsx')