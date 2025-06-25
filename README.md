One can check the well-formedness of the Canonical Form of MWEs. Tis example shows how this can be done:

```
from ucfsyntax  import is_wellformed

examples = ['someone +kicks the bucket', someone DO:+takes 0a L:decision', someone DO:+takes 0a L;walk']

for example in examples:
    if is_wellformed(exampe):
        print(f'OK: {example}')
    else:
        print(f'NO: {example}')
```   

