import re


write = open("./NewHadithOnly.txt", "w+", encoding='windows-1256')
read = open("./originalCANER.txt", "r+", encoding='windows-1256')
read = read.read()

"""
تعليق	O
مصطفى	PERSON
البغا	PERSON
30	Number
"""
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
  