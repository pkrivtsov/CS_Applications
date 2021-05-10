import re
import csv

regex = r"^\s*(?P<key>[\w\s\(\)\[\]]*):\s*(?P<value>[\w\.\-\,\~\;\\\(\) \/\+\:]*)$"
main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

for i in range(1, 4):
    with open(f'example/info_{i}.txt', encoding='cp1251') as r_file:
        my_dict = dict(re.findall(regex, r_file.read(), re.MULTILINE))
    main_data.append([my_dict.get(j) for j in main_data[0]])
with open('example/main_data.csv', 'w') as w_file:
    writer = csv.writer(w_file)
    writer.writerows(main_data)  # [[1,2,3,4], [1,2,3,4]]
