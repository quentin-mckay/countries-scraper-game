from app import get_flag_colors

def test_flag_colors_length():
    assert get_flag_colors('Germany') ==  ["000000", "DD0000", "FFCC00"]

def test_flag_colors_length():
    assert get_flag_colors('Canada') ==  ["D80621", "FFFFFF"]