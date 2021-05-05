x = [i.rstrip() for i in open("test.txt").readlines()]
y = [i.rstrip() for i in open("wordlist.txt").readlines()]



for i in x:
    if i in y :
        pass
    else:
        print(i.rstrip(), "not found")
