from xls2tex import compress


examples = [['iemand', '|', 'iets', 'is', 'ziek']]

for example in examples:
    result = compress(example)
    print(f'{example} -->\n{result}')