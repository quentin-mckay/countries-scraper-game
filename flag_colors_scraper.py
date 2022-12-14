import requests
from bs4 import BeautifulSoup
from countries import countries
from time import sleep
from pprint import pp

flag_colors = {}

for country in countries[:10]:

	country_for_url = country

	# edge cases for flagcolorcodes.com
	if country == 'Netherlands':
		country_for_url = 'the-netherlands'
	elif country == 'United_States':
		country_for_url = 'usa'

	# wikipedia uses underscores but flagcolorcodes.com uses hyphens 
	country_for_url = country_for_url.replace('_', '-')

	res = requests.get(f'https://www.flagcolorcodes.com/{country_for_url}')
	soup = BeautifulSoup(res.text, 'html.parser')
	
	# exract the data-clipboard attribute from all the <li>'s inside of the element with class .
	colors = [el['data-clipboard-text'] for el in soup.select('.main-circles > li')]

	flag_colors[country] = colors

	sleep(0.5)

pp(flag_colors)