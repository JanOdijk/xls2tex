from ucfsyntax  import is_wellformed

examples = ['someone +kicks the bucket', 'someone DO:+takes 0a L:decision', 'someone DO:+takes 0a L;walk']

for example in examples:
    if is_wellformed(example):
        print(f'OK: {example}')
    else:
        print(f'NO: {example}')