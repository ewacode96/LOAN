import fitz
import os
import re
import pandas as pd
import numpy as np

path = input("Please insert path: ")
filelist = os.listdir(path)

raty = []
kapital = []
odsetki = []
nadplaty = []

#Szczególy raty
pattern1 = re.compile(r"(Spłata raty\n)([0-9\s,].*)(PLN)([0-9\s,].*)(PLN)([0-9\s,].*)(PLN)")
#Nadpłaty
pattern2 = re.compile(r"(Spłata raty pozaplanowej\n)([0-9\s,].*)(PLN)")

for i in filelist:
    if i.startswith("historia"):
        doc = fitz.open(f'ING\{i}')
        text = ""
        for page in doc:
            text += page.get_text()
        for item in pattern1.finditer(text):
            raty.append(('Rata', float(item.group(2).replace(u'\xa0', '').replace(',', '.'))))
            kapital.append(('Kapital', float(item.group(4).replace(u'\xa0', '').replace(',', '.'))))
            odsetki.append(('Odsetki', float(item.group(6).replace(u'\xa0', '').replace(',', '.'))))
        for item in pattern2.finditer(text):
            nadplaty.append(('Nadplata', float(item.group(2).replace(u'\xa0', '').replace(',', '.'))))

del raty[10]
del odsetki[10]
del kapital[10]

lst = raty + kapital + odsetki + nadplaty
print(lst)
df = pd.DataFrame(lst, columns=['Typ', 'Kwota'])
print(df)

# for typ in df['Typ'].unique():
#     # We'll just calculate the average using numpy for this particular state
#     suma = np.sum(df.where(df['Typ']==typ)['Kwota'])
#     # And we'll print it to the screen
#     print('Suma ' + typ +
#           ' wynosi ' + str(suma))

for group, frame in df.groupby('Typ'):
    # groupby() returns a tuple, where the first value is the
    # value of the key we were trying to group by
    suma = round(np.sum(frame['Kwota']), 2)
    print('Suma ' + group +
          ' wynosi ' + str(suma))

df = df.groupby("Typ").agg({"Kwota":(np.sum, np.average, np.max, np.min)})
print(df)

# avg = np.sum(df['Kapital'])
# print(avg)


# suma_raty = 0
# # del raty[10] #zwielokrotnione
# for x in raty:
#     suma_raty = suma_raty + x
#
# suma_kapital = 0
# # del kapital[10] #zwielokrotnione
# for x in kapital:
#     suma_kapital = suma_kapital + x
#
# suma_odsetki = 0
# # del odsetki[10] #zwielokrotnione
# for x in odsetki:
#     suma_odsetki = suma_odsetki + x
#
# print(f'Historia:\nKapitał: {round(suma_kapital, 2)}')
# print(f'Odsetki: {round(suma_odsetki,2)}')
# print(f'Raty: {round(suma_raty,2)}')
