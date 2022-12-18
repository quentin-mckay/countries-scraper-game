from app import filter_country_name

#test filter_country_name() correctly replaces name of country in string
def test_filter_country_name():
    assert filter_country_name('Japanese Yen', 'Japan', '_') == '_ Yen'

def test_filter_country_name():
    assert filter_country_name('The United States', 'United_States', '_') == 'The _ _'


# @pytest.mark.parametrize('test_string', [
#     '',
#     'Japanese Yen',
#     'The capital of Spain is Madrid',
#     'The United States has 50 states.'
# ])