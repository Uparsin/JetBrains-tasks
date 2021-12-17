import random

print("H A N G M A N")
choice = input('Type "play" to play the game, "exit" to quit:')
words = ['python', 'java', 'kotlin', 'javascript']

variable_name = random.choice(words)

variable_name_list = list(variable_name)

hyphens = "-"

hidden_name = variable_name.replace(variable_name, hyphens * len(variable_name))
hidden_name_list = list(hidden_name)
hp = 8
guessed_letters = set()

if choice == "play":
    while ("".join(hidden_name_list)) != variable_name:
        if hp == 0:
            break
        print()
        print("".join(hidden_name_list))
        letter = input("Input a letter: ")
        if len(letter) != 1:
            print("You should input a single letter")
            continue
        for j in range(len(variable_name)):
            if letter != hidden_name_list[j] and (letter == variable_name_list[j]):
                if letter == variable_name_list[j]:
                    hidden_name_list[j] = letter
            elif (letter == variable_name_list[j]) and letter == hidden_name_list[j]:
                print("You've already guessed this letter")
                break
            elif letter not in variable_name_list:
                if letter.islower():
                    if letter not in guessed_letters:
                        hp -= 1
                        print("That letter doesn't appear in the word")
                        guessed_letters.add(letter)
                        break
                    else:
                        print("You've already guessed this letter")
                        break
                else:
                    print("Please enter a lowercase English letter")
                    break
    if ("".join(hidden_name_list)) != variable_name:
        print("You lost!")
    else:
        print("""You guessed the word!
You survived!""")
