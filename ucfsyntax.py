import re

def plus(unit: str, sep=r'\s*') -> str:
    result = fr'({unit}({sep}{unit})*)'
    return result

basic_outer_annotation = r'(L|M|OIA|CIA|DO|BE|BC|ST|CBE|CBC|CST|GV|GT|LBT|PMP)'
outer_annotation = rf'({basic_outer_annotation}:)'
escapesym = r'\\'
escape = fr'({escapesym}[<0:\\])'
interpunction = r'[?!,]'
bword = fr"((\w|{escape}|[-'\u2019])+|{interpunction})"
word = fr'{bword}{interpunction}?'
vbl_word = word
alt_word = rf'({vbl_word}\s*\|\s*{vbl_word})'
word_annotation = r'([\*\+=!0\^]|dd:|dr:|com:|\+\*|\*\+|\+!|!\+|\=\*|\*\=|=!|!=)'
annotated_word = rf'({outer_annotation}?{word_annotation}?{word})'
sequence_annotation = r'[LM]'
sequence_end = r'\]'
sequence_start = fr'{sequence_annotation}:\['
basic_annotated_word_sequence = rf'({sequence_start}\s*{plus(annotated_word)}\s*{sequence_end})'
angled_sequence = rf'(((<\s*{plus(word)}\s*>)|(<:\s*{plus(word)}\s*:>)))'
annotated_word_sequence = rf'({basic_annotated_word_sequence}|{angled_sequence}|{annotated_word}|{alt_word})'
ucfmwe = fr'^\s*{plus(annotated_word_sequence)}\s*$'

theregex = ucfmwe

theregex_re = re.compile(theregex)

okmwelist = ['L:[in veiligheid]',
        ' L:[in veiligheid] ',
        ' L:[ in veiligheid ] ',
        '<zij>',
        ' < zij > ',
        ' < zij > gaan',
             'gaan <zij>',
        'iemand zal iemand L:[in veiligheid] stellen']
okmwelist += ['iets zal iets willen zeggen',
        'iemand zal 0de L:beschikking CIA:over iets CBE:krijgen',
        'iemand zal het CIA:met iemand kunnen vinden',
        'laat staan',
        'dd:die vlieger 0zal ^niet opgaan',
        'iemand zal iemand tot kalmte brengen',
        'iemand zal buiten spel staan  ',
        'iemand zal iemand buiten spel zetten',
        '<zij> zullen naar elkaar toegroeien',
        'iemand zal iemand L:[in veiligheid] CBC:stellen',
        'iemand|iets zal eruit vliegen',
        'iets|iemand zal zijn prijs hebben',
        'iets | iemand zal zijn prijs hebben',
              '=!liep',
              '!=liep',
              '*=liep',
              '=*liep',
              '*+liep',
              '+*liep',
              'com:met',
              'dd:het',
              'dr:er',
              ' DO:+loopt',
              'L:[onder *druk]' ,
              'L:[onder L:druk]',
              'L:[onder *druk] staan',
              'iemand ',
              'iemand zal ',
              'iemand zal 0de ',
              'iemand zal 0de L:beschikking ',
              ' iemand',
              'met zijn <: vieren :> ',
              '\\0de',
              '\\0de poging',
              'k\\:a'

              ]

okmwes = [(mwe, True) for mwe in okmwelist]

wrongmwelist = [' 0de C:beschikking',
                '0de C:beschikking',
                'CIA;over',
                 'L: over'
               ] + \
               ['iemand zal 0de C:beschikking CIA:over iets CBE:krijgen',
                ' L:beschikking CIA;over ',
                  '0de L:beschikking CIA;over',
                  'iemand zal 0de L:beschikking CIA;over',
                 'iemand zal 0de L:beschikking CIA;over iets CBE:krijgen'  
               ]

wrongmwes = [(mwe, False) for mwe in wrongmwelist]

allmwes = okmwes + wrongmwes

def is_wellformed(mwe: str) -> bool:
    thematch = theregex_re.match(mwe)
    result = thematch is not None
    return result

def tryme():
    verbose = 5
    errorfound = False
    # allmwes = [  (' L:beschikking CIA;over ', False),
    #              ('0de L:beschikking CIA;over', False) # this one already causes looping
    #           ]
#    allmwes = [('<0de', True)]
    for mwe, ok in allmwes:
        thematch = theregex_re.match(mwe)
        correct = (thematch is None and not ok) or (thematch is not None and ok)
        wellformed = 'indeed' if thematch is not None else 'not'
        message = f'expression is {wellformed} well-formed'
        if not correct:
            print(f'NO: <{mwe}>: {message}')
            errorfound = True
        else:
            if verbose > 3:
                print(f'OK: <{mwe}>: {message}')
    # if errorfound:
    #   raiseError()



if __name__ == '__main__' :
    tryme()