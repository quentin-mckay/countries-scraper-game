# Countries Scraper Game

A terminal quiz game written in Python which challenges the player to guess a country in 6 tries or less based on various types of hints scraped from the country's Wikipedia page and/or flag colors scraped from [FlagColorCodes.com](https://www.flagcolorcodes.com/).

High scores are recorded to a CSV file and can displayed in a pretty-printed table.

[Click to view project GitHub repository](https://github.com/quentin-mckay/countries-scraper-game)

The code follows the styling conventions outlined in [PEP 8](https://peps.python.org/pep-0008/)


## Installation and Usage


1. Run `chmod +ux run_app.sh` to make the bash script executable

2. Run `./run_app.sh` to launch the application

Two command line options are available:
1. `--show-country` will display the correct answer at the beginning of each game. Useful for testing and debugging.

2. `--no-intro` will skip the intro animation. Useful wehn testing the application so you don't have to sit through the unnecessary (albeit short) animation.

Example usage with both flags: `./run_app --show-country --no-intro`

Note: The application uses the `match case` statement so requires Python version 3.10 or later.

## Features

### Web-Scraping Wikipedia

The quiz selects a random country from the 32 nations in the 2022 world cup and then uses the [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) library to scrape information from that country's Wikipedia page.

Each piece of data was it's own challenge, with the scraping method needing to be tweaked so as to accomodate varying oddities in both the HTML structure and particular country's available information.

### High Scores CSV File

Each time the user guesses correctly, their attempt is written to a csv file of "High Scores". Three pieces of data are written (number of guesses attempted, overall time taken (seconds) to complete the game, and the correctly guessed country)

The user can also display the high scores by selecting the option from the main menu. The csv file is read, sorted by number of guesses, and pretty-printed using the [Tabulate](https://pypi.org/project/tabulate/) library for better readability.

![high scores](./images/high-scores.jpg)

### Flag Color Text

Each time "[3] Flag Color Text" is selected as a hint option, the words in the remaing hints are colored an additional color of the country's flag using the package [Colr](https://pypi.org/project/Colr/).  

![color sentence](./images/color-sentence.jpg)

### Flag Color Web-Scraping to JSON

A separate script was written to scrape the flag color hex codes for all 32 countries from [FlagColorCodes.com](https://www.flagcolorcodes.com/). 

The data was written into a JSON file and then read by the main application.

### Main Menu and Quiz Game Loop

The main menu provides multiple options with varying functionality and gives the user the option to quit.

![main menu](./images/main-menu.jpg)








## Implementation Plan

The implementation plan was carried out using Trello.

[Click to view the Trello Board](https://trello.com/b/vWXNzHCk/countries-scraping-game)

![scraping](./images/trello-scraping-date.jpg)

![checklist](./images/trello-checklist.jpg)

![progress 1](./images/trello-progress-1.jpg)

![progress 2](./images/trello-progress-2.jpg)

![progress 3](./images/trello-progress-3.jpg)