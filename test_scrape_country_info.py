from app import scrape_country_info

info = scrape_country_info('Argentina')

def test_scrape_country_info_length():
    assert len(info) == 6

def test_country_info_has_capital():
    assert info['capital']

def test_country_info_has_currency():
    assert info['currency']

def test_country_info_has_president():
    assert info['president']

def test_country_info_has_anthem():
    assert info['anthem']

def test_country_info_has_first_paragraph():
    assert info['first paragraph']

def test_country_info_has_second_paragraph():
    assert info['second paragraph']