#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8

__version__ = '0.0.1'
__author__ = 'Benedikt Zoennchen'

import re


def __extract_within_brackets(text, obracket, cbracket):
    pos = text.find(obracket)
    startpos = pos
    count = 0
    while pos >= 0:
        cpos = text.find(cbracket, pos+1)
        opos = text.find(obracket, pos+1)
        if opos >= 0 and cpos > opos:
            count += 1
            pos = opos
        else:
            break

    for _ in range(count):
        pos = text.find(cbracket, pos+1)
        if pos < 0:
            raise Exception('incorrect formated string!')
    endpos = text.find(cbracket, pos+1)
    return (startpos, endpos)


def extract_bracket(text, lead, obracket, cbracket):
    pos = text.find(lead)
    extraction = ""
    if pos > -1:
        text = text[pos + len(lead):]
        startpos, endpos = __extract_within_brackets(text, obracket, cbracket)
        if startpos >= 0 and endpos >= 0:
            extraction = text[startpos+1:endpos]
    return extraction


def extract_optional(text, lead):
    return extract_bracket(text, lead, '[', ']')


def extract_non_optional(text, lead):
    return extract_bracket(text, lead, '{', '}')


def extract_shortauthors(text):
    return extract_optional(text, "\\author")


def extract_authors(text):
    return extract_non_optional(text, "\\author")


def extract_shorttitle(text):
    return extract_optional(text, "\\title")


def extract_title(text):
    return extract_non_optional(text, "\\title")


def extract_env(text, env):
    env_content = ""
    pos = text.find("\\begin{" + env + "}")
    if pos > -1:
        text = text[pos + len("\\begin{" + env + "}"):]
        endpos = text.find("\\end{"+env+"}")
        env_content = text[0:endpos].strip()
    return env_content


def extract(paper_file_name):
    text = open(paper_file_name).read()
    shortauthors = extract_shortauthors(text)
    longauthors = extract_authors(text)
    shorttitle = extract_shorttitle(text)
    longtitle = extract_title(text)
    abstract = extract_env(text, "abstract")
    keywords = extract_env(text, "keywords")
    return shortauthors, longauthors, shorttitle, longtitle, abstract, keywords


def remove_comments(tex_text):
    out = ''
    print(tex_text.splitlines())
    for line in tex_text.splitlines():
        new_line = line
        pos = line.find("%")
        if pos > -1:
            new_line = line[:pos]
        out += new_line + '\n'
    return out.strip()


def clear_title(title, is_short_title=False):
    title = title.replace("%", "")
    title = title.replace(r"\\", "")
    title = title.replace("\n", "")
    title = title.replace("\break", "")
    title = title.replace("\centering", "")
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"\[.*?\] *", "", title)
    title = re.sub(
        r"\\(textnormal|vspace|small|large){.*?}", "", title)
    title = re.sub(r"\\(systemname){.*?} :", "", title)
    if is_short_title:
        title = re.sub(r"---.*$", "", title)
    title = re.sub(r"\\large.*$", "", title)
    title = title.strip()
    return title


def texify(text):
    tex_replacement_map = {'é': "\\'e", 'ó': "\\'{o}", 'ć': "\\'{c}", 'Ä': '\\"A', 'Ö': '\\"O', 'Ü': '\\"U',
                           'ß': '{\\ss}', 'ä': '\\"a', 'ö': '\\"o', 'ü': '\\"u', 'ñ': '\\~{n}', 'ń': "\\'n",
                           '„': '\\glqq', '“': '\\grqq', '”': "''", '’': "'{}", ' - ': ' --- '}
    for char in tex_replacement_map:
        text = text.replace(char, tex_replacement_map[char])
    return text
