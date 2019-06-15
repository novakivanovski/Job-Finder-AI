from Tests import TestingTools
from Utilities.Stats import Stats
from DataStructures.Keyword import Keyword


def sort_by_name(values):
    values.sort(key=lambda x: x.name)


@TestingTools.timer
def run():
    TestingTools.reset_db()
    stats = Stats()
    keywords = stats.get_keywords()
    sort_by_name(keywords)
    expected_keywords = [Keyword('engineer', 1, 2, 40, 80), Keyword('software', 20, 4, 40, 80)]
    sort_by_name(expected_keywords)
    for actual, expected in zip(keywords, expected_keywords):
        TestingTools.assert_equal(actual.pass_count, expected.pass_count)
        TestingTools.assert_equal(actual.fail_count,  expected.fail_count)




