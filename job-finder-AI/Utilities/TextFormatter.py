import re
from nltk import word_tokenize


def reformat_newlines(text, max_line_length=100):
    line_length = 0
    text_output = ''
    text = replace_multiple_whitespace(text)
    text_without_newlines = remove_newlines(text)
    text_list = word_tokenize(text_without_newlines)
    for i, word in enumerate(text_list):
        text_output += word + ' '
        line_length += len(word)
        if line_length > max_line_length:
            text_output += '\n'
            line_length = 0
    return text_output


def replace_multiple_whitespace(text):
    text = replace_multiple_newlines(text)
    text = replace_multiple_spaces(text)
    text_output = replace_multiple_tabs(text)
    return text_output


def replace_multiple_newlines(text):
    pattern = '\n+'
    text_output = re.sub(pattern, '\n', text)
    return text_output


def replace_multiple_spaces(text):
    pattern = ' +'
    text_output = re.sub(pattern, ' ', text)
    return text_output


def replace_multiple_tabs(text):
    pattern = '\t+'
    text_output = re.sub(pattern, '\t', text)
    return text_output


def remove_multiple_spaces(text):
    pattern = ' +'
    text_output = re.sub(pattern, ' ', text)
    return text_output


def remove_newlines(text):
    pattern = '\n+'
    return re.sub(pattern, '', text)


def remove_tabs(text):
    pattern = '\t+'
    text_output = re.sub(pattern, '', text)
    return text_output


def remove_spaces(text):
    pattern = ' +'
    text_output = re.sub(pattern, '', text)
    return text_output


