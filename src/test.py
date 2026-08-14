frase = " Frase animada aqui "

import time, sys

for i in list(frase):
    print(i, end='')
    sys.stdout.flush()
    time.sleep(0.1)