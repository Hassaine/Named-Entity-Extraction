import re
lines=open("CANERCorpuss.txt","r",encoding="windows-1256").readlines()
cpt=0
for line in lines:
    print(line)
    tokens=re.compile(r"\s+").split(line)
    print(tokens)
    if not re.match(r"O$",tokens[1]):
        cpt+=1


print(cpt)
