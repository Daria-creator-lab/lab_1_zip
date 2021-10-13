import zipfile
import os
import hashlib
import requests
import re
import csv

# Задание №1
directory_to_extract_to = os.getcwd()     #директория извлечения файлов архива
arch_file = os.path.abspath("archive.zip")  #путь к архиву
print(arch_file)
directory_into = "//Users//dary//PycharmProjects//прикладное_программирование_лаба_1//new_dir"
print(directory_into)
current_zip = zipfile.ZipFile("//Users//dary//PycharmProjects//прикладное_программирование_лаба_1//archive.zip")
current_zip.extractall(directory_into)

# Задание №2.1
sh_files = []
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        if file.endswith('.sh'):
            sh_files.append(root + r'/' + file)

# Задание №2.2
result_hash = []
for file in sh_files:
    file_data = open(file, 'rb').read()
    result_hash.append(hashlib.md5(file_data).hexdigest())

# Задание №3
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла

for file in sh_files:
    target_file_data = open(file, 'rb').read()
    if hashlib.md5(target_file_data).hexdigest() == target_hash:
        target_file = file
        break
print(target_file)
print(target_file_data)

# Задание №4
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

counter = 0
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        # Удаление тегов
        headers = re.sub(r'\<[^>]*\>', "", line)
        # Извлечение списка заголовков
        headers = re.findall('[А-Я][^А-Я]*', headers)
    # Удаление тегов
    temp = re.sub(r'\<[^>]*\>', ';', line)
    temp = re.sub(r'\([()*]*\)', '', temp)
    temp = re.sub(r'^\W+', '', temp)
    temp = re.sub(r'\(.*?\)', '', temp)
    temp = re.sub(r'[*]', '', temp)
    temp = re.sub(r'\xa0', '', temp)
    temp = re.sub(r'_', '-1', temp)
    # Замена последовательности символов ';' на одиночный символ
    temp = re.sub(r';+', ';',  temp)
    # Удаление символа ';' в начале и в конце строки
    temp = re.sub(r';$', '', temp)
    # Разбитие строки на подстроки
    temp_split = re.split(r';', temp)
    # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
    if temp_split != headers:
        country_name = temp_split[0]
    # Извлечение данных из оставшихся столбцов
        col1_val = temp_split[1]
        col2_val = temp_split[2]
        col3_val = temp_split[3]
        col4_val = temp_split[4]
    # Запись извлеченных данных в словарь
        result_dct[country_name] = ([int(col1_val), int(col2_val), int(col3_val), int(col4_val)])
    counter += 1

# Задание №5
# Запись данных из полученного словаря в файл
with open('data.csv','w') as csv_file:
    c = csv.writer(csv_file, delimiter=';')
    c.writerow(headers)
    for key in result_dct.keys():
        c.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
# Задание №6
target_country = input("Введите название страны: ")
if target_country in result_dct:
    print('Заболели; Умерли; Вылечились; Активные случаи')
    print(result_dct[target_country])
else:
    print('Такая страна не найдена')
