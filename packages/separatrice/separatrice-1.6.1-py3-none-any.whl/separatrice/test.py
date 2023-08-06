from separatrice import *
from evalution import *

text = "Добрый вечер, вчера я пришел с университета и обнаружил, что потерял пропуск, скажите, как мне восстановить пропуск?"
s = Separatrice()
clauses = s.into_clauses(text)
for i,clause in enumerate(clauses):
    print(i,clause)