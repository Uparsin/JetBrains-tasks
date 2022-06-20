import requests

from bs4 import BeautifulSoup

import itertools


def translate(src, lang, translatable, limit=1):
    direction = f'{src}-{lang.lower()}'
    url = f'https://context.reverso.net/translation/{direction}/{translatable}'

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(response.text, "html.parser")

    translation_line = f'{lang} Translations:'

    translations_filtered = [r.get_text().strip().lower() for r in soup.find_all(
          'span', class_='display-term')]
    translations_line = "\n".join(translations_filtered)

    trg_class_name = "trg ltr"

    if lang == "Hebrew":
        trg_class_name = "trg rtl"
    elif lang == "Arabic":
        trg_class_name = "trg rtl arabic"

    example_line = f'{lang} Examples:'

    src_filtered = (r.text.strip() for r in soup.find_all(
          'div', class_='src ltr'))
    trg_filtered = (r.text.strip() for r in soup.find_all(
          'div', class_=trg_class_name))
    zip_lists = zip(list(itertools.islice(src_filtered, limit)),
                    list(itertools.islice(trg_filtered, limit)))
    join_list = [source + "\n" + target for source, target in zip_lists]
    examples_line = "".join(join_list)

    if bool(examples_line) is False:
        return "Sorry, unable to find "

    translations = f"{translation_line}\n{translations_line}"
    examples = f"{example_line}\n{examples_line}"
    to_file = f"""{translations}

{examples}"""

    return to_file
