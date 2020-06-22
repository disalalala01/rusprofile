from flask import Flask, jsonify

import requests

from bs4 import BeautifulSoup


def get_html(url):
    if url:
        html = requests.get(url, 'lxml')
        return html.text
    return None


def get_json(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = requests.get(url, headers=headers).json()
    try:
        if resp['ul_count'] == 0:
            return None
        return resp['ul'][0]['link']
    except:
        return None

def get_main_page_url(url):
    if url:
        id = url.split('/')[2]
        return f'https://www.rusprofile.ru/founders/{id}?filter=org_foreign'
    return None


def get_data_okpo(id):

    url = f'https://www.rusprofile.ru/{id}'

    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    okpo = soup.find(id='clip_okpo').text

    name = soup.find('div', class_='company-name').text.strip()

    return okpo, name


def get_page_data(html, id):

    okpo = ''
    com_name = ''

    if id:
        okpo, com_name = get_data_okpo(id)

    if html:

        soup = BeautifulSoup(html, 'lxml')

        ads = soup.find_all('div', class_='company-item')

        alims = []
        for ad in ads:

            try:
                name = ad.find('a').text.strip()

            except:
                name = ''
            try:
                summa = ad.find('div', class_='company-item-info').find('dd').text

            except:
                summa = ''
            try:
                address = ad.find('address', class_='company-item__text').text.strip()

            except:
                address = ''
            try:
                reg = ad.find_all('div', class_='company-item-info')[1].find_all('dl')[0].text.strip()

            except:
                reg = ''
            try:
                post_time = ad.find_all('div', class_='company-item-info')[1].find_all('dl')[1].find('dd').text

            except:
                post_time = ''


            content = {
                'Имя': name,
                'Сумма': summa,
                'Адрес': address,
                'Рег': reg,
                'Дата': post_time
            }
            alims.append(content)



        return { 'status': True ,'okpo': okpo ,'name': com_name ,'content': alims }
    return {'status': False, 'okpo': okpo,'name': com_name ,'content': None }







app = Flask(__name__)




@app.route('/rusprofile/<inn>')
def index(inn):

    main_url = f'https://www.rusprofile.ru/ajax.php?&query={inn}&action=search'

    id = get_json(main_url)


    url = get_main_page_url(id)

    html = get_html(url)

    data = get_page_data(html, id)

    return jsonify(data)





if __name__ == '__main__':

    app.run( port='5001' ,debug=True)
