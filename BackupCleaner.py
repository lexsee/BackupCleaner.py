from filecmp import dircmp
from os.path import join, getsize
import os
import datetime

def folder_dir():
    '''
        Функция выдаёт адреса рабочего каталога и бэкапа.
    '''
    WORK_DIR = 'c:\\Users\\KondratyevAV\\Desktop\\TEST\\D'
    BACK_DIR = 'c:\\Users\\KondratyevAV\\Desktop\\TEST\\Y'
    return WORK_DIR, BACK_DIR

def find_uncommon(WORK_DIR, BACK_DIR):
    '''
        Функция получает адреса рабочего каталога и бэкапа,
        сравнивает их и возвращает список каталогов
        присутствующих в бэкапе и отсутствующих в рабочем каталоге.
    '''
    dcmp = dircmp(WORK_DIR, BACK_DIR)
    folder_list = [join(BACK_DIR, f) for f in dcmp.right_only]
    # рекурсивно вызываем функцию для подкаталогов общих каталогов
    for sub_dir in dcmp.common_dirs:
        sub_back = find_uncommon(join(WORK_DIR, sub_dir), join(BACK_DIR, sub_dir))
        folder_list.extend(sub_back)
    return folder_list

def folder_size(folder_list):
    '''
        Функция получает список адресов каталогов,
        производит рекурсивные вычисления их размера,
        возвращает словарь вида "адрес каталога : размер каталога"
    '''
    folder_dict = {}
    for roots in folder_list:
        size = getsize(roots)
        folder_dict[roots] = size
        for root, dirs, files in os.walk(roots, topdown=False):
            for f in files:
                fp = os.path.join(root, f)
                # отбрасываем символические ссылки
                if not os.path.islink(fp):
                    size += os.path.getsize(fp)
            folder_dict[roots] = size
    return folder_dict

def folder_print(folder_dict):
    '''
        Функция получает словарь вида "адрес каталога : размер каталога",
        выводит эти данные на экран и формирует лог-файл в формате csv.
    '''
    now = datetime.datetime.now()
    print("\n\t"+now.strftime("%d-%m-%Y %H:%M")+"\n")
    with open (str(now.strftime("%Y-%m-%d-%H-%M")+".csv"), "w") as f:
        for keys, values in folder_dict.items():
            print(f"\t{keys}    {round(values / 1024, 3)} Kb")
            print(f"{keys};{round(values / 1024, 3)} Kb", file=f, sep="\n")

def main():
    '''
        Управляющая функция: определяет порядок вызова и обеспечивает передачу данных
        между служебными функциями.
    '''
    WORK_DIR, BACK_DIR = folder_dir()
    folder_list = find_uncommon(WORK_DIR, BACK_DIR)
    folder_dict = folder_size(folder_list)
    folder_print(folder_dict)

main()

input("\n\n\tНажмите Enter для выхода из программы ")