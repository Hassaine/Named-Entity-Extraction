import re


writes = open("./splitmustapha.txt", "w+", encoding='windows-1256')
read = open("./HadithOnly_50_bak.txt", "r+", encoding='windows-1256')
read = read.read()

"""
تعليق	O
مصطفى	PERSON
البغا	PERSON
30	Number
"""
def bad(write):
    x= 1
    for i in range(1,6803):
        match = re.search(r"\n("+str(i)+"\tNumber\n(حدثنا\tO\n(.|\n)*?)(تعليق\tO\nمصطفى\tPERSON\nالبغا\tPERSON\n"+str(i)+"\tNumber)|[0-9]+\tNumber\n[0-9]+\tNumber)\n", read)
        if (match):
            write.write(match.group(2))
            write.write("***")
            print(match.group(2))
            print(i)
            print("number"+str(x))
            x+=1
    pass
def mark_ta3lik(lines, file):
    for line in lines:
        if re.search("تعليق\tO",line):
            file.write("***\n")
        file.write(line)
    pass


read = open("./HadithOnly_50_bak.txt", "r+", encoding='windows-1256')

read = open("./HadithOnly.txt", "r+", encoding='windows-1256')
w = open("./temp.txt", "w+", encoding='windows-1256')


lines = read.readlines()
temp =[]
l=0
first = False
for i in range(1,6418):
    while l <len(lines):
        match = re.search(r"\b"+str(i)+"\tNumber", lines[l])
        if(match and not first):
            first = True
        if(first):
            temp.append(lines[l])
        if(match and first):
            for line in temp:
                w.write(line)
            w.write("***\n")
            first = True
            break
        l+=1