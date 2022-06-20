import sys

import translate_func

lang_dict = {1: "Arabic",
             2: "German",
             3: "English",
             4: "Spanish",
             5: "French",
             6: "Hebrew",
             7: "Japanese",
             8: "Dutch",
             9: "Polish",
             10: "Portuguese",
             11: "Romanian",
             12: "Russian",
             13: "Turkish"}

args = sys.argv

if args[1].capitalize() not in lang_dict.values():
    print(f"Sorry, the program doesn't support {args[1]}")
    sys.exit()
elif args[2].capitalize() not in lang_dict.values() and args[2] != "all":
    print(f"Sorry, the program doesn't support {args[2]}")
    sys.exit()

lang_src = args[1].lower()

del_num = 3
for num, lang in lang_dict.items():
    if lang.lower() == lang_src:
        del_num = num

del lang_dict[del_num]

file = open(f"{args[3]}.txt", "w", encoding="UTF-8")

try:
    if args[2] != "all":
        lang_trg = args[2].capitalize()
        translation = translate_func.translate(
            lang_src, lang_trg, args[3], limit=5)
        if translation == "Sorry, unable to find ":
            print(translation + args[3])
        else:
            file.write(translation)
            print(translation)
    else:
        full_file = []

        for num in range(1, 14):
            try:
                lang_trg = lang_dict[num]
                translation = translate_func.translate(
                    lang_src, lang_trg, args[3])
                if translation == "Sorry, unable to find ":
                    print(translation + args[3])
                    sys.exit()
                else:
                    full_file.append(translation)
            except KeyError:
                continue

        file.write("\n\n\n".join(full_file))
        print("\n\n\n".join(full_file))

    file.close()

except ConnectionError:
    print("Something wrong with your internet connection")
