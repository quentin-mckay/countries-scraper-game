import requests
from bs4 import BeautifulSoup
import re
import os
from random import choice, randint
from countries import countries # list of 32 countries
from colr import color

def random_color():
	return (randint(0, 256), randint(0, 256), randint(0, 256))


text = color('hello', fore=random_color())
# text2 = color('hello', fore=(255, 128, 0))

sentence = "This is a random sentence of words"

sentence = ' '.join([color(word, fore=random_color()) for word in sentence.split()])

print(text)

print(sentence)

# os.system('clear')

# print(countries)

# country = input('Country: ')


country = 'Argentina'
country = 'Denmark'
# country = 'Japan'
# country = 'Saudi_Arabia'
# country = 'Wales'
# country = 'South_Korea'

country = choice(countries)

print()
print(country)

response = requests.get(f'https://en.wikipedia.org/wiki/{country}')
soup = BeautifulSoup(response.text, 'html.parser')

# ===== get info paragraph =====
p_tags = soup.select('.mw-parser-output > p') # hook in and get list of <p>'s
info_paragraph = p_tags[1].get_text() # get text from 1st <p>


# ============================== regex cleaning functions ==============================

def filter_country_name(string, country_name, replacement=''):
	country_name = country_name.replace('_', ' ') # ex turn 'Saudi_Arabia' into 'Saudi Arabia'

	start_name = country_name[:4] # slice the first 4 letters
	end_name = country_name[-4:] # slice the last 4 letters 

	# regex test for words that include either first or last part of country name
	# preceded or followed by any number of letters
	# note: uses a raw f-string and the re.I makes it case-insensitive
	regex = re.compile(rf'\w*({start_name}|{end_name})\w*', re.I) 

	return regex.sub(replacement, string) # substitute _ wherever the word would have appeared


def remove_footnotes_and_parens(string):
	# match either (.....) or [.....]
	# note: uses non-greedy capture modifier and
	regex = re.compile(r'\[.*?\]|\(.*?\)\)*')
	return regex.sub('', string)


info_paragraph = filter_country_name(info_paragraph, country, replacement='_') # filter the 

# print(info_paragraph)
# print(remove_footnotes_and_parens((info_paragraph)))
# print(info_paragraph.split('.')[0]) 
# print(choice(info_paragraph.split('.')))


# ============================== Fill info dictionary ========================================
info = {}


# ===== get anthem =====
anthem = ''
try:
	td_tag = soup.select('.anthem')[0]
	strings_list = list(td_tag.stripped_strings)
	last_few = strings_list[-3:] # anthem is always in one of the last few spots
	anthem = [s for s in last_few if len(s) > 5][-1] # find the one that's not a punctuation

	# print()
	# print(list(strings_list))
	print()
	print(anthem.replace('"', ''))
except IndexError: # for some reason Denmark is different to every other country
	print('no anthem')


info['anthem'] = anthem.replace('"', '') # get rid of quotes if needed



# ===== get table data =====
th_tags = soup.select('.vcard')[0].find_all('th') # get list <th>'s
# print(th_tags)


for th_tag in th_tags:

	strings = list(th_tag.strings)
	# print(strings)

	if strings:

		if strings[0] == 'Capital':
			td = th_tag.find_next_sibling('td') # find corresponding <td>
			capital = td.find('a').string # get string of first <a> in the <td>
			info['capital'] = capital

		if strings[0] == 'Currency':
			td = th_tag.find_next_sibling('td') # find corresponding <td>
			currency = td.find('a').string # get string of first <a> in the <td>
			currency = filter_country_name(currency, country, replacement='').strip()
			info['currency'] = currency

		# check for either President or Prime Minister
		if 'President' in strings:
			td = th_tag.find_next_sibling('td') # find corresponding <td>
			president = td.find('a').string # get string of first <a> in the <td>
			info['president'] = president
		elif 'Prime Minister' in strings:
			td = th_tag.find_next_sibling('td') # find corresponding <td>
			prime_minister = td.find('a').string # get string of first <a> in the <td>
			info['prime minister'] = prime_minister

print()
print(info, '\n')
		




def play_game():
	answer_country = choice(countries) # pick random country

	country_info = scrape_country_info(answer_country)

	guesses_remaining = 6

	print(answer_country)

	while guesses_remaining > 0:

		# display options
		guess_word = 'guesses' if guesses_remaining > 0 else 'guess'
		print(f"{guesses_remaining} {guess_word} remaining. Select a hint option: ")
		options = [
				'[1] Random sentence',
				'[2] Random fact',
				'[3] Flag colour text'
			]
		[print(option) for option in options]

		# get guess from user
		guess = input("Guess the country: ")

		if guess == answer_country:
			print("You win!")
			break



		guesses_remaining -= 1
		


def show_high_scores():
	print('High Scores')

	

def start():

	print('--- Welcome to the World Cup Country Quiz Game ---\n')
	print('Please select an option:')

	options = ['[1] Play quiz game', '[2] Show High Scores']
	[print(option) for option in options] # print out each option on a new line

	menu_choice = input('> ')


	match menu_choice:
		case '1':
			play_game()
		case '2':
			show_high_scores()



if __name__ == '__main__':
	start()