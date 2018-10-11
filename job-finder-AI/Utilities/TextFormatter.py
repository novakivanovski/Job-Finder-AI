import re
from nltk.tokenize import WhitespaceTokenizer


def multi_print(*args):
    for arg in args:
        print(arg)


def format_job_url(job_url):
    url_text = 'Link: ' + str(job_url)
    return reformat_text(url_text)


def format_job_keywords(job_keywords):
    keywords_text = 'Job keywords: ' + str(job_keywords)
    return reformat_text(keywords_text)


def format_job_score(job_score):
    score_text = 'Job score: ' + str(job_score)
    return score_text


def format_job_description(job_description):
    description_text = 'Job description: ' + job_description
    return reformat_text(description_text) + '\n'


def format_job_title(job_title):
    title_text = 'Job Title: ' + job_title
    return format_header(title_text)


def reformat_text(text, max_line_length=100):
    line_length = 0
    text_output = ''
    text = replace_multiple_whitespace(text)
    text_without_newlines = remove_newlines(text)
    text_list = WhitespaceTokenizer().tokenize(text_without_newlines)
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


def format_header(text):
    text = reformat_text(text)
    sep = '\n' + '=' * 25
    header = sep + '\n' + text + sep
    return header

