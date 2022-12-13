import requests
from bs4 import BeautifulSoup
import re
import os
from random import choice

os.system('clear')

# country = input('Country: ')

country = 'Argentina'
country = 'Morocco'
response = requests.get(f'https://en.wikipedia.org/wiki/{country}')


soup = BeautifulSoup(response.text, 'html.parser')

# ===== get info paragraph =====
p_tags = soup.select('.mw-parser-output > p') # hook in and get list of <p>'s

info_paragraph = p_tags[1].get_text() # get text from 1st <p>

def filter_country_name(string, country_name):
	start_name = country_name[:4] # slice the first 4 letters
	end_name = country_name[-4:] # slice the last 4 letters 

	# regex test for words that include either first or last part of country name
	# preceded or followed by any number of letters
	# note: uses a raw f-string and the re.I makes it case-insensitive
	regex = re.compile(rf'\w*({start_name}|{end_name})\w*', re.I) 

	return regex.sub('_', string) # substitute _ wherever the word would have appeared


def remove_footnotes_and_parens(string):
	# match either (.....) or [.....]
	# note: uses non-greedy capture modifier and
	regex = re.compile(r'\[.*?\]|\(.*?\)\)*')
	return regex.sub('', string)


info_paragraph = filter_country_name(info_paragraph, country) # filter the 

print(info_paragraph)
print(remove_footnotes_and_parens((info_paragraph)))
# print(info_paragraph.split('.')[0]) 
# print(choice(info_paragraph.split('.')))


# ===== get table data =====

th_tags = soup.select('.ib-country')[0].find_all('th') # get list <th>'s
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

print()
print(info)
        

# tr_tags = soup('div', string="and largest city")[0].parent.strings
# print(list(tr_tags))

