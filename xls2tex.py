from collections import defaultdict
from dataclasses import dataclass
from latexdoc import docbegin, docend
import os
import re
from sastadev.xlsx import getxlsxdata
from variablewords import variablewords, translitvariablewords
from typing import List, Tuple
# from mwe_query.analyseducame import containsillegalsymbols, containsillegalwords
from ucfsyntax import is_wellformed

illegalsymbols = """@#$%&()_{};"\\/123456789"""
illegalsymbolserror = "Illegal symbols"
glosserror = "Glosserror"
illformedness_error = "Not well-formed"

space = ' '
oiamarking = 'oia:'
ciamarking = 'cia:'

r2l = {'ar', 'fa'}

id_sectioncol = 1
id_ordercol = 2
id_namecol = 3
languagecol = 4
id_segmentcol = 5
cfcol = 7
transliterationcol = 8
glosscol = 9
literaltranslationcol = 10
translationcol = 11
statuscol = 12
contributorcol = 13
sourcecol = 14

endxlist = r'\end{xlist}'
endexe = r"""\end{exe}

"""


outex, inex, inxlist = 0, 1, 2
okstate, inbrackets = 0, 1

outfolder = 'texout'

@dataclass
class ExampleMWE:
    id: str
    cf: str
    transliteration: str
    gloss: str
    literaltranslation: str
    translation: str
    language: str
    source: str


def containsillegalsymbols(canform: str) -> Tuple[bool, str]:
    illegalchars = ''
    result = False
    for ch in canform:
        if ch in illegalsymbols:
            illegalchars += ch
            result = True
    return result, illegalchars

def mksection(title: str) -> str:
    result = \
    rf"""\section*{{{title}}}

\begin{{exe}}
"""
    return result



def isiav(word) -> bool:
    result = word.lower().startswith(oiamarking) or word.lower().startswith(ciamarking)
    return result


def marktext(rawinstr: str, variablewords: List[str]) -> str:
    newwords = []
    instr = re.sub(r'\|', r' | ', rawinstr)
    words = instr.split()
    state = okstate
    for word in words:
        if word.startswith('<'):
            state = inbrackets
        marking = state != inbrackets and word not in variablewords and not isiav(word) and not \
            word.lower().startswith(r'\lex') and not word.startswith('0') and word not in r'\|<>'
        if marking:
            newword = rf"\lex{{{word}}}"
        else:
            newword = word
        newwords.append(newword)
        if word.endswith('>'):
            state = okstate
    compressedwords = compress(newwords)
    result = space.join(compressedwords)
    return result

def compress(words: List[str]) -> List[str]:
    newwords = []
    newword = ''
    for i, word in enumerate(words):
        if i < len(words) - 1:
            nextword = words[i+1]
        else:
            nextword = ''
        if i > 0:
            prevword = words[i-1]
        else:
            prevword = ''
        if word == '|':
            newword += word
        elif prevword == '|':
            newword += word
            newwords.append(newword)
        elif nextword == '|':
            newword = word
        else:
            newwords.append(word)
    return newwords


def checkforerrors(data):
    errors = defaultdict(list)
    glosserrors = defaultdict(list)
    for i, row in enumerate(data):
        status = row[statuscol]
        contributor = row[contributorcol]
        if status.lower() == 'ok':
            rowcount = i + 2
            cf = row[cfcol]
            if not is_wellformed(cf):
                errors[contributor].append((illformedness_error, rowcount, '', cf))
            wrong, wrongsymbols = containsillegalsymbols(cf)
            if wrong:
                errors[contributor].append((illegalsymbolserror, rowcount, wrongsymbols, cf))

            gloss = row[glosscol]
            lcf = len(cf.split())
            lgloss = len(gloss.split())
            if lcf != lgloss:
                errors[contributor].append((glosserror, rowcount, cf, gloss, lcf, lgloss))
    return errors

def ex2tex(ex: ExampleMWE, twolinetranslation=True, lexmarking=True) -> str:
    lg = ex.language
    lglc = lg.lower()
    # do something for right-to-left languages
    id = ex.id
    hastransliteration = ex.transliteration != ""
    hasliteraltranslation = ex.literaltranslation != ''
    sourcetext = rf'\hspace*{{\fill}}({ex.source})' if ex.source != "" else ""

    if hasliteraltranslation:
        if twolinetranslation:
            sep = r"\\"
        else:
            sep = " | "
        literaltranslation = rf"lit. `{ex.literaltranslation}'{sep}"
    else:
        literaltranslation = ""
    if hastransliteration:
        glcommand = r'\glll'
        markedcf = marktext(ex.cf, variablewords[lglc]) if lglc in variablewords else ex.cf
        cf = rf'{markedcf}\\'
        transliteration = marktext(ex.transliteration, translitvariablewords[lglc]) if lglc in translitvariablewords \
            else \
            ex.transliteration
    else:
        glcommand = r'\gll'
        cf = marktext(ex.cf, variablewords[lglc]) if lglc in variablewords else ex.cf
        transliteration = ''
    result = \
rf"""\ex \label{{{lg}:{id}}}
\settowidth \jamwidth{{({lg})}} 
{glcommand} {cf}{transliteration}\\
{ex.gloss}\\  \jambox{{({lg})}}
\glt {literaltranslation}
`{ex.translation}' \\
{sourcetext}
%\z
"""
    return result

def genlatex(header, table) -> str:
    previd_section = ''
    previd_order = ''
    previd_name = ''
    state = outex
    resultlist = []
    for row in table:
        status = row[statuscol]
        if status.lower() not in ['ok']:
            continue
        id_section = row[id_sectioncol]
        id_order = row[id_ordercol]
        id_name = row[id_namecol]
        id_segment = row[id_segmentcol]
        id = f'{id_name}-{id_segment}'
        language = row[languagecol]
        cf = row[cfcol]
        transliteration = row[transliterationcol]
        gloss = row[glosscol]
        literaltranslation = row[literaltranslationcol]
        translation = row[translationcol]
        contributor = row[contributorcol]
        source = f'{language}-{id}: {row[sourcecol]}' if row[sourcecol] != "" else f'{language}-{id}'
        mwe = ExampleMWE(id=id, cf=cf, transliteration=transliteration, gloss=gloss,
                         literaltranslation=literaltranslation, translation=translation, language=language,
                         source=source)
        if previd_section != id_section:
            if previd_section != "":
                resultlist.append(endexe)
            newsection = mksection(id_section)
            resultlist.append(newsection)
            previd_section = id_section
        mwetex = ex2tex(mwe)
        resultlist.append(mwetex)
    resultb = docbegin
    resultm = '\n'.join(resultlist)
    resulte = docend
    result = resultb + resultm + resulte
    return result


def reporterrors(errors):
    for contributor in errors:
        print(f'contributor: {contributor}')
        for tpl in errors[contributor]:
            if len(tpl) == 4:
                errormsg, rowid, wrongsymbols, cf = tpl
                if errormsg in [illegalsymbols,illformedness_error]:
                    print(f'---{rowid}: {errormsg}: {wrongsymbols} in {cf}')
            elif len(tpl) == 6:
                errormsg, rowid, cf , gloss, lcf, lgloss = tpl
                if errormsg == glosserror:
                    print(f'---{rowid}: {errormsg}: {lcf}<>{lgloss} in <{cf}> with gloss <{gloss}>')

def mkdoc():
    infilename = 'CF Examples WG 2 task 2.4.xlsx'
    infullname = os.path.join('data', infilename)
    header, table = getxlsxdata(infullname, sheetname='Data')
    errors = checkforerrors(table)
    reporterrors(errors)
    latextext = genlatex(header, table)
    base, ext = os.path.splitext(infilename)
    outfullname = os.path.join(outfolder, f'{base}.tex')
    with open(outfullname, 'w', encoding='utf8') as outfile:
        print(latextext, file=outfile)


def tryme():
    example1 = ExampleMWE(id='example1', cf=r'Chris hat Alex \lex{den} \lex{Kopf} \lex{gewaschen}.',
                          transliteration="", gloss="Chris has Alex the head washed",
                          literaltranslation="Chris washed Alex' head.",
                          translation ="Chris gave Alex a telling-off.",
                          language = "de",
                          source ="Hoehle 2018: 9; our gloss and translation"
                          )


    latex1 = ex2tex(example1)
    print(latex1)

if __name__ == '__main__':
    # tryme()
    mkdoc()