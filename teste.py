
if __name__ == '__main__':
    arquivo = open("teste.txt", "r")
    toWrite = open("pol_n.txt", "a")
    for line in arquivo:
        splited =  line.replace("\n","").split(" ")

        string = ""
        for i in splited:
            string += "x^" + i + " + "
        string += "1"
        toWrite.write(string +"\n")
        print string
