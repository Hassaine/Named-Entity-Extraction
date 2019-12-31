import re


write = open("./NewHadithOnly.txt", "w+", encoding='windows-1256')
read = open("./originalCANER.txt", "r+", encoding='windows-1256').readlines()


def getHadith(lines):
    read = lines
    i=1
    l=0
    listLines= []
    end = False
    while l < len(read):
        while i< 6803 and l<len(read):
            match = re.search(r"\b"+str(i)+"\tNumber",read[l])
            if(match):
                l+=1
                one = re.search(r"تعليق\tO", read[l])
                while not one:
                    l+=1
                    listLines.append(read[l])
                    one = re.search(r"تعليق\tO", read[l])
                if(one):
                    l+=1
                    two = re.search(r"مصطفى\tPERSON", read[l])
                    if(two):
                        l+=1
                        three = re.search(r"البغا\tPERSON", read[l])
                        if(three):
                            l+=1
                            end = re.search(r""+str(i)+"\tNumber", read[l])
                if(end):
                    for line in listLines:
                        write.write(line)
                    write.write("***")
                    print("*** "+str(i))
                    i+=1
            else:
                l+=1



getHadith(read)


