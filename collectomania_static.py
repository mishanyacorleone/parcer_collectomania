import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

agent = UserAgent()


def parse_urls_cards(url):
    response = requests.get(url=url, headers={
        'user-agent': f'{agent.random}'
    }).content
    soup = BeautifulSoup(response, 'lxml')
    catalog = soup.find('div', class_='catalog').find_all('div', class_='product-preview__title')
    urls_cards = list()
    for card in catalog:
        urls_cards.append(f"https://collectomania.ru{card.find('a').get('href')}")
    print(urls_cards, end='\n')
    parse_card(urls_cards)


def parse_card(urls_cards):
    for url in urls_cards:
        response = requests.get(url=url, headers={
            'user-agent': f'{agent.random}'
        }).text
        soup = BeautifulSoup(response, 'lxml')
        name = soup.find('h1', class_='product__title heading').text.strip()
        price = soup.find('span', class_='current-price').text.strip()
        params = soup.find('div', class_='product__chars--list').find_all('div')

        print(f'Название: {name}')
        print(f'Цена: {price}')

        for param_name in params:
            for param in param_name.find_all('div', class_='product__chars--item'):
                title = param.find('span', class_='product__chars--item--title').text.strip().replace('\n', '').replace(':', '')

                value = param.find('span', class_='product__chars--item--value').text.strip().replace('\n', '')

                if 'состояние' in title.lower() and 'new' in value.lower():
                    value = 'New'
                if 'состояние' in title.lower() and 'old' in value.lower():
                    value = 'old'
                if 'состояние' in title.lower() and value.lower() not in ['old', 'new']:
                    value = 'n/a'

                if ',' in value:
                    value = value.strip().split()
                    value = ' '.join(value)

                print(f'{title}: {value}')
        print(end='\n')
        input()


def main():
    url = input('Введите url страницы: ')
    parse_urls_cards(url)


if __name__ == '__main__':
    main()