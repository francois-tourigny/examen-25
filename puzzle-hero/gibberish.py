f = open("q7.txt", "r")
data = f.read()

for i in range(len(data)):
    print(data[i], end='')
    if i%200 == 0:
        print()
