import re


write = open("./NewHadithOnly.txt", "w+", encoding='windows-1256')
read = open("./HadithOnly.txt", "r+", encoding='windows-1256')
read = read.readLines()

for line in read:
    print(line)