from nose.tools import *

import get_data

def test_cleandata_removes_square_brackets():
    before = """ethnicity = [[Latins]]"""
    after = get_data.clean_data(before).strip()
    goal = """ethnicity = Latins"""
    assert_equals(after, goal)

def test_cleandata_removes_html_tags():
    before = """agency = Roman schools<ref>{{cite encyclopedia}}</ref>"""
    after = get_data.clean_data(before).strip()
    goal = """agency = Roman schools"""
    assert_equals(after, goal)

def test_parsetags_unwraps_urls():
    before = """{{URL|scraperwiki.com}}"""
    after = get_data.parse_tags(before).strip()
    goal = """scraperwiki.com"""
    assert_equals(after, goal)

def test_parsetags_extracts_the_first_bit_from_square_brackets():
    before = """ethnicity = [[Medieval Europe|Medieval]]"""
    after = get_data.parse_tags(before).strip()
    goal = """ethnicity = Medieval Europe"""
    assert_equals(after, goal)
