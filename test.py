from curses.ascii import isalpha


name = 'poly-nes-76'

words = list(name)
newWords = []

for w in words:
    if w.isalpha():
        newWords.append(w)
    else:
        pass

newName = "".join(newWords)

print(newName)