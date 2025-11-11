import os
from sastadev.readcsv import readcsv
from collections import defaultdict

infilename = 'variablewords.txt'
infilename = 'Variable Words - Sheet1.tsv'
infullname = os.path.join('data', infilename)

def getvblwords(infullname):
    variablewords = defaultdict(list)
    translitvariablewords = defaultdict(list)
    idata = readcsv(infullname)
    for i, row in idata:
        if len(row) <= 1:
            print(f'variablewords: Wrong row: <{row}>')
        if len(row) >= 2:
            language = row[0].lower()
            vblword = row[1]
            variablewords[language].append(vblword)
        if len(row) == 3:
            tvblword = row[2]
            translitvariablewords[language].append(tvblword)
    return variablewords, translitvariablewords

variablewords, translitvariablewords = getvblwords(infullname)


junk = 0  # for debugging purposes