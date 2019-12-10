string=b""+str(input("Donner la chaine unicode  a afficher en arabe \n"))
string=string.encode("utf-8")
t=string.decode("windows-1256")
print(t)