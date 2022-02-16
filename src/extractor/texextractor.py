#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding: utf-8

import re


def inner_extract(text, obracket, cbracket):
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

    for i in range(count):
        pos = text.find(cbracket, pos+1)
        if pos < 0:
            raise Exception('incorrect formated string!')
    endpos = text.find(cbracket, pos+1)
    return (startpos, endpos)


def extract(paperFileName):
    data = open(paperFileName).read()
    pos = data.find("\\author")
    shortauthors = ""
    longauthors = ""
    shorttitle = ""
    longtitle = ""
    abstract = ""
    keywords = ""

    if pos > -1:
        data = data[pos + len("\\author"):]
        startpos, endpos = inner_extract(data, '[', ']')
        if startpos >= 0 and endpos >= 0:
            shortauthors = data[startpos+1:endpos]

        startpos, endpos = inner_extract(data, '{', '}')
        if startpos >= 0 and endpos >= 0:
            longauthors = data[startpos+1:endpos]

    data = open(paperFileName).read()
    pos = data.find(r"\title")

    if pos > -1:
        data = data[pos + len(r"\title"):].strip()

        startpos, endpos = inner_extract(data, '[', ']')
        if startpos >= 0 and endpos >= 0:
            shorttitle = clear_title(data[startpos+1:endpos], True)

        startpos, endpos = inner_extract(data, '{', '}')
        if startpos >= 0 and endpos >= 0:
            longtitle = clear_title(data[startpos+1:endpos])
    else:
        print(paperFileName)

    data = open(paperFileName).read()
    pos = data.find("\\begin{abstract}")
    if pos > -1:
        data = data[pos + len("\\begin{abstract}"):]
        endpos = data.find("\\end{abstract}")
        abstract = data[0:endpos].strip()

    data = open(paperFileName).read()
    pos = data.find("\\begin{keywords}")
    if pos > -1:
        data = data[pos + len("\\begin{keywords}"):]
        endpos = data.find("\\end{keywords}")
        keywords = data[0:endpos].strip()

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
