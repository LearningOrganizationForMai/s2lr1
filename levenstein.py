import logging
import time
from docx import Document
from fuzzywuzzy import fuzz
import Levenshtein

logging.basicConfig(
    level=logging.INFO,
    filename="lev.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s"
)

def read(filename):
    doc = Document(filename)
    text = []
    for i in doc.paragraphs:
        text.append(i.text)
    result = '\n'.join(text)
    return result

text1 = read('first.docx')
text2 = read('second.docx')

def lev(first, second):
    len1, len2 = len(first), len(second)
    if len1 > len2:
        first, second = second, first
        len1, len2 = len2, len1

    cur_row = range(len1 + 1)
    for i in range(1, len2 + 1):
        prew_row, cur_row = cur_row, [i] + [0] * len1
        for j in range(1, len1 + 1):
            add, delete, change = prew_row[j] + 1, cur_row[j - 1] + 1, prew_row[j - 1]
            if first[j - 1] != second[i - 1]:
                change += 1
            cur_row[j] = min(add, delete, change)

    return cur_row[len1]

start = time.time()

result = lev(text1, text2)
print(f"Расстояние Левенштейна моим кодом: {result}")

end = time.time()
logging.info(f'Расчет расстояния Левенштейна через мой код занял {end - start} с')


start = time.time()

result = fuzz.ratio(text1, text2)
print(f"Расстояние Левенштейна, использую fuzzywuzzy {result}")

end = time.time()
logging.info(f'Расчет расстояния Левенштейна через библиотеку fuzzywuzzy занял {end - start} с')



start = time.time()

result = Levenshtein.distance(text1, text2)
print(f"Расстояние Левенштейна, использую Levenshtein {result}")

end = time.time()
logging.info(f'Расчет расстояния Левенштейна через библиотеку Levenshtein занял {end - start} с')


