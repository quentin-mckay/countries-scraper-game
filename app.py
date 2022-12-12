import requests
from bs4 import BeautifulSoup


country = input('Country: ')
response = requests.get(f'https://en.wikipedia.org/wiki/{country}')

# response = requests.get(f'https://en.wikipedia.org/wiki/Argentina')

soup = BeautifulSoup(response.text, 'html.parser')

# ==== working ====
p_tags = soup.select('.mw-parser-output > p')
info_paragraph = p_tags[1].get_text()
# print(info_paragraph)

th_tags = soup.select('.ib-country')[0].find_all('th')
# print(th_tags)

info = {}
for th_tag in th_tags:
    strings = list(th_tag.strings)
    if strings and strings[0] == 'Capital':
        td = th_tag.find_next_sibling('td')
        # get string of first <a> in the <td>
        capital = td.find('a').string
        info['capital'] = capital
    if strings and strings[0] == 'Currency':
        td = th_tag.find_next_sibling('td')
        # get string of first <a> in the <td>
        currency = td.find('a').string
        info['currency'] = currency

print(info)
        

# tr_tags = soup('div', string="and largest city")[0].parent.strings
# print(list(tr_tags))

