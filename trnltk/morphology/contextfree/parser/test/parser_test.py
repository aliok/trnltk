import unittest
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from trnltk.morphology.model import formatter

class ParserTest(unittest.TestCase):
    def assert_parse_correct_for_verb(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatches([a for a in args]))


    def assert_parse_correct(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultMatchesIgnoreVerbPresA3Sg([a for a in args]))


    def assert_parse_exists(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultExists([a for a in args]))

    def assert_parse_doesnt_exist(self, word_to_parse, *args):
        assert_that(self.parse_result(word_to_parse), IsParseResultDoesntExist([a for a in args]))


    def parse_result(self, word):
        return [formatter.format_morpheme_container_for_tests(r) for r in (self.parser.parse(word))]


class IsParseResultMatches(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))


class IsParseResultMatchesIgnoreVerbPresA3Sg(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        items = filter(lambda item: u'+Zero+Pres+' not in item, items)
        return all(er in items for er in self.expected_results) and all(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))


class IsParseResultExists(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        return any(er in items for er in self.expected_results) and any(item in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))

class IsParseResultDoesntExist(BaseMatcher):
    def __init__(self, expected_results):
        self.expected_results = expected_results

    def _matches(self, items):
        return all(er not in items for er in self.expected_results) and all(item not in self.expected_results for item in items)

    def describe_to(self, description):
        description.append_text(u'     ' + str(self.expected_results))