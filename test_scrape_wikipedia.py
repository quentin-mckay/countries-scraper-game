from app import scrape_country_info

# test country scraping returns dictionary with all pieces of data

info = scrape_country_info('Argentina')

def test_scrape_country_info_length():
    assert len(info) == 6

def test_country_info_has_capital():
    assert info['capital']

def test_country_info_has_capital():
    assert info['currency']

def test_country_info_has_capital():
    assert info['president']

def test_country_info_has_capital():
    assert info['anthem']

def test_country_info_has_capital():
    assert info['first paragraph']



info = scrape_country_info('Canada')

def test_scrape_country_info_length():
    assert len(info) == 6

def test_country_info_has_capital():
    assert info['capital']

def test_country_info_has_capital():
    assert info['currency']

def test_country_info_has_capital():
    assert info['president']

def test_country_info_has_capital():
    assert info['anthem']

def test_country_info_has_capital():
    assert info['first paragraph']



# @pytest.fixture(params=['Argentina', 'Canada'])
# def scrape_country_info(request):
#     info = scrape_country_info(request.param)
#     return info