from app import get_flag_colors

# test get_flag_colors() returns correct hex codes
def test_flag_colors_item():
    assert get_flag_colors('Germany') ==  ["000000", "DD0000", "FFCC00"]

def test_flag_colors_item():
    assert get_flag_colors('Canada') ==  ["D80621", "FFFFFF"]