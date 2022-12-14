import requests
from bs4 import BeautifulSoup
import re
import os
from random import choice, randint
from countries import countries # list of 32 countries
from colr import color
import json
from csv import DictReader, DictWriter
from time import time
from pprint import pp

os.system('clear')

start_time = time()


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


def clean_text(text, country):
	text = filter_country_name(text, country, replacement='_')
	text = remove_footnotes_and_parens(text)
	return text

# print(info_paragraph)
# print(remove_footnotes_and_parens((info_paragraph)))
# print(info_paragraph.split('.')[0]) 
# print(choice(info_paragraph.split('.')))
		

def scrape_country_info(country):
	info = {}

	response = requests.get(f'https://en.wikipedia.org/wiki/{country}')
	soup = BeautifulSoup(response.text, 'html.parser')

	# ===== get info paragraph =====
	p_tags = soup.select('.mw-parser-output > p') # hook in and get list of <p>'s

	paragraph = p_tags[1].get_text() # get text from 1st <p>
	info['first paragraph'] = clean_text(paragraph, country)

	paragraph = p_tags[2].get_text() # get text from 1st <p>
	info['second paragraph'] = clean_text(paragraph, country)



	# ============================== Fill info dictionary ========================================
	# ===== get anthem =====
	anthem = ''
	try:
		td_tag = soup.select('.anthem')[0]
		strings_list = list(td_tag.stripped_strings)
		last_few = strings_list[-3:] # anthem is always in one of the last few spots
		anthem = [s for s in last_few if len(s) > 5][-1] # find the one that's not a punctuation

		# print()
		# print(list(strings_list))
	except IndexError: # for some reason Denmark is different to every other country
		# print('no anthem')
		pass


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

	return info












def get_flag_colors(country):
	with open('flag_colors.json') as file:
		flag_colors_dict = json.load(file)

	return flag_colors_dict[country]





def write_to_high_scores(guesses_remaining, country, elapsed_time):
	with open('high_scores.csv', 'a', newline='') as file:
		headers = ['Guesses', 'Country', 'Elapsed Time']
		writer = DictWriter(file, fieldnames=headers)
		writer.writerow({
			'Guesses': guesses_remaining,
			'Country': country,
			'Elapsed Time': elapsed_time
		})




# ======================================== PLay Game ============================================
# one little hacky fix here. probably bad practice
# I didn't want to have to pass these into every single call color_print()
num_flag_colors = 0
flag_colors = []


def play_game():
	global num_flag_colors, flag_colors

	answer_country = choice(countries) # pick random country
	# answer_country = 'France'

	print()
	print(answer_country, '\n')

	info = scrape_country_info(answer_country)
	# print(country_info)

	flag_colors = get_flag_colors(answer_country)
	# print(flag_colors)
	num_flag_colors = 0


	starting_guesses = 6
	guesses_remaining = starting_guesses
	facts_remaining = 4


	# main hints loop
	while guesses_remaining > 0:

		# display options
		guess_word = 'guess' if guesses_remaining == 1 else 'guesses'
		color_print(f"{guesses_remaining} {guess_word} remaining. Select a hint option: ")
		print()

		options = [
				'[1] Random sentence',
				'[2] Fact',
				'[3] Flag color text',
				''
			]
		[color_print(option) for option in options]


		# hint_option = ''
		# while hint_option not in ('1', '2', '3'):
		hint_option = input('> ')
		print()


		match hint_option:
			# Random Sentence
			case '1':
				combined = info['first paragraph'] + info['second paragraph']
				sentences = combined.split('.')
				# print(sentences)

				sentence = ''
				while len(sentence) < 5: # filter out occasional oddities
					sentence = choice(sentences)
					sentence = sentence.strip()

				color_print("Here's a random sentence: \n")
				color_print(sentence + '.')

			# Fact
			case '2':
				# anthem
				if facts_remaining == 4:
					anthem = clean_text(info['anthem'], answer_country)
					color_print(f"The national anthem of the country is {anthem}.")
				# leader
				elif facts_remaining == 3:
					if info.get('president'):
						color_print(f"The country's president is {info['president']}.")
					elif info.get('prime minister'):
						color_print(f"The country's prime minister is {info['prime minister']}.")
				# currency
				elif facts_remaining == 2:
					color_print(f"The country's currency is {info['currency']}.")
				# capital
				elif facts_remaining == 1:
					color_print(f"The country's capital is {info['capital']}.")
				elif facts_remaining == 0:
					color_print('Sorry, there are no new facts. Please choose another hint type.\n')
					continue

				facts_remaining -= 1
			case '3':
				if num_flag_colors == len(flag_colors):
					color_print("Maximum flag colors reached. Please choose another hint type.")
					print()
					continue
				else:
					num_flag_colors += 1
					guesses_remaining -=1
					continue

		print()

		# get guess from user
		guess = input("Guess the country: ")
		print()

		if guess == answer_country:
			color_print("You win!")
			print()

			elapsed_time = round(time() - start_time, 2)

			write_to_high_scores(guesses_remaining, answer_country, elapsed_time)

			break



		guesses_remaining -= 1

	if guesses_remaining == 0:
		color_print(f'Sorry you ran out of guesses. The correct country was {answer_country}.\n')

	again = ''
	while again not in ('y', 'yes', 'n', 'no'):
		again = input("Would you like to play again? (y/n) ").lower()

	if again in ('yes', 'y'):
		return play_game() # return ends execution of the function
	else:
		color_print("\nThank's for playing! Bye!\n")
	
		







def show_high_scores():
	print('High Scores')

	







def color_print(text):
	num_colors = num_flag_colors
	colors_list = flag_colors

	# print(num_colors)
	# print(colors_list)

	if num_colors == 0:
		print(text)
	else:
		colored_words_list = []

		for index, word in enumerate(text.split()):
		
			i = ((index + 1) % num_colors)
			i = 0 if i < 0 else i # make sure it's not below 0
			hex = colors_list[i]

			colored_word = color(word, fore=hex)
			colored_words_list.append(colored_word)

		output = ' '.join(colored_words_list)
		print(output)








def start():


	# num_flag_colors = 3
	# flag_colors = ['ff0000', '00ff00', '0000ff']

	# color_print('hello this is a random sentence of lots of words', num_flag_colors, flag_colors)
	

	print('\n--- Welcome to the World Cup Country Quiz Game ---\n')
	print('Please select an option:\n')

	options = [
		'[1] Play Quiz',
		'[2] Show High Scores', 
		# '[3] Show Quiz Instructions',
		'[4] Show List of Countries',
		'[q] Quit',
		''
	]
	[print(option) for option in options] # print out each option on a new line

	menu_choice = input('> ')


	match menu_choice:
		case '1':
			play_game()
		case '2':
			show_high_scores()
		case '4':
			pp(sorted(countries))
			start() # restart application
		case 'q' | 'Q':
			print("\nBye!\n")
			quit()



if __name__ == '__main__':
	start()