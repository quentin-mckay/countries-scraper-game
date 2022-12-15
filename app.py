import requests
from bs4 import BeautifulSoup
import re
import os
from random import choice, randint
from countries import countries # list of 32 countries
from colr import color
import json
from csv import reader, DictWriter
from time import time
from pprint import pp
from tabulate import tabulate
import sys

os.system('clear')



def random_color():
	return (randint(0, 256), randint(0, 256), randint(0, 256))

# print(random_color())

text = "Welcome"

def rainbow(string):
	return ''.join([color(letter, fore=random_color()) for letter in string])

def rainbow_print(string):
	print(rainbow(string))
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
	'''Scrapes information and first two paragraphs from the country's Wikipedia page'''
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
	'''Reads flag_colors.json and returns a list of color hex values'''

	with open('flag_colors.json') as file:
		flag_colors_dict = json.load(file)

	return flag_colors_dict[country]





def write_to_high_scores(guesses_remaining, elapsed_time, country):
	with open('high_scores.csv', 'a', newline='') as file:
		headers = ['Guesses', 'Time Taken','Country']
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writerow({
			'Guesses': guesses_remaining,
			'Time Taken': elapsed_time,
			'Country': country
		})


def get_high_scores():
	'''Reads high_scores.csv and returns list of all rows'''
	with open('high_scores.csv', 'r') as file:
		csv_reader = reader(file)
		return list(csv_reader)



def show_high_scores(csv_list):
	'''Sorts list of lists by first column and prints out table'''
	# seperate header so can sort the scores
	headers, scores = csv_list[0], csv_list[1:]

	# sort by first item in list (guesses)
	
	scores = sorted(scores, key=lambda row: row[0])

	result = [headers] + scores

	print()
	print(tabulate(result, headers='firstrow', numalign='left'))
	# print()


# ======================================== PLay Game ============================================
# one little hacky fix here. probably bad practice
# I didn't want to have to pass these into every single call to color_print()
num_flag_colors = 0
flag_colors = []


def play_game():
	'''Plays the quiz game (main menu option [1])'''

	global num_flag_colors, flag_colors

	start_time = time()

	answer_country = choice(countries) # pick random country
	# answer_country = 'France'

	print()
	if is_testing:
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

				color_print("Here's a random sentence:")
				print()
				color_print(sentence + '.')
				print()

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
					print()
					continue

				print()

				facts_remaining -= 1

			# flag color text
			case '3':
				if num_flag_colors == len(flag_colors):
					color_print("Maximum flag colors reached. Please choose another hint type.")
					print()
					continue
				else:
					num_flag_colors += 1
					# guesses_remaining -=1
					# continue

		# print()

		# get guess from user
		guess = input(color_text("Guess the country:", ending=' '))
		print()

		guesses_remaining -= 1

		if guess == answer_country:
			print("Hooray! You win!")
			print()
			print("Your number of guesses, total time taken, and country have been added to the high scores.")
			print()
			print("Don't forget to email student services to redeem your all-expenses paid trip to World Cup 2026 courtesy of Coder Academy.")
			print()

			time_taken = round(time() - start_time, 2)

			num_guesses = starting_guesses - guesses_remaining
			write_to_high_scores(num_guesses, time_taken, answer_country)

			break




	if guesses_remaining == 0:
		color_print(f'Sorry you ran out of guesses. The correct country was {answer_country}.\n')

	again = ''
	while again not in ('y', 'yes', 'n', 'no'):
		again = input("Would you like to play again? (y/n) ").lower()

	if again in ('yes', 'y'):
		return play_game() # return ends execution of the function
	else:
		print("\nThank's for playing! Bye!\n")
	
		






	



def color_text(text, ending=''):
	colored_words_list = []

	if num_flag_colors == 0:
		output = text + ending
	else:
		for index, word in enumerate(text.split()):
		
			i = ((index + 1) % num_flag_colors)
			i = 0 if i < 0 else i # make sure it's not below 0
			hex = flag_colors[i]

			colored_word = color(word, fore=hex)
			colored_words_list.append(colored_word)

		output = ' '.join(colored_words_list) + ending

	return output


def color_print(text):
	if num_flag_colors == 0:
		print(text)
	else:
		print(color_text(text))








def start():


	# num_flag_colors = 3
	# flag_colors = ['ff0000', '00ff00', '0000ff']

	# color_print('hello this is a random sentence of lots of words', num_flag_colors, flag_colors)
	

	rainbow_print('\n--- Welcome to the World Cup Country Quiz Game ---\n')
	print('Please select an option:\n')

	options = [
		'[1] Play Quiz',
		'[2] Show High Scores', 
		'[3] Show Quiz Instructions',
		'[4] Show List of Countries',
		'[q] Quit',
		''
	]
	[print(option) for option in options] # print out each option on a new line

	
	
	# protect against invalid inputs
	possible_choices = ('1', '2', '3', '4', 'q', 'Q')

	menu_choice = ''
	while menu_choice not in possible_choices:
		menu_choice = input('> ')




	match menu_choice:
		case '1':
			play_game()
		case '2':
			scores = get_high_scores()
			show_high_scores(scores)
			start() # restart application
		case '3':
			print('''
Welcome to the world cup country quiz game!

The goal is to guess the country randomly selected from the 32 participanting nations of the 2022 World Cup. 

You have 6 guesses.

Before each guess you can choose from 3 different types of hints.

[1] Random Sentence
A random sentence scraped from the first 2 paragraphs of the country's wikipedia page.
The name of the country has been redacted.

[2] Fact
A fact scraped from the country's Wikipedia page.
The order of the facts given is always the same.
Anthem -> Leader -> Currency -> Capital

[3] Flag color text
Each time chosen, remaining hint text will be colored an additional color of the country's flag.

Good luck!
			''')
			start() # restart application
		case '4':
			print()
			[print(country) for country in sorted(countries)] # print sorted list
			start() # restart application
		case 'q' | 'Q':
			# print("\nBye!\n")
			print()
			quit()




def check_for_testing_flag():
	return '--testing' in sys.argv




if __name__ == '__main__':

	is_testing = check_for_testing_flag()

	try:
		start()
	except KeyboardInterrupt:
		print("\n\nGoodbye!")