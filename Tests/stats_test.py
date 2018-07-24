from Tests import TestingTools
from Utilities.Stats import Stats
from DataStructures.Keyword import Keyword


def test_constructor(stats_instance):
    test_keywords = [Keyword('Engineer', 0.4, 0.6), Keyword('Python', 0.85, 0.15),
                     Keyword('Software', 0.5, 0.5), Keyword('Developer', 0.55, 0.45)]

    test_keywords.sort(key=lambda x: x.name)
    stats_instance.keywords.sort(key=lambda x: x.name)
    for test_key, actual_key in zip(test_keywords, stats_instance.keywords):
        TestingTools.assert_equal(test_key.pass_probability, actual_key.pass_probability)
        TestingTools.assert_equal(test_key.fail_probability, actual_key.fail_probability)


def run():
    stats_instance = Stats()
    test_constructor(stats_instance)

