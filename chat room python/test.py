def hello():
    print("hello world this is just a test")

isRunning = True


def MyStrip(word):
    newWord = ""
    for letter in word:  
        if(letter) == " ":
            continue
        newWord = newWord + letter
    return newWord

while isRunning:
    command = input(" >> ")
    command = MyStrip(command)
    if(command.lower() == "do"):
        hello()
    elif command.lower()=="exit":
        isRunning = False


