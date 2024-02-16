import sys
import json
from functions import search_json, display_contacts, editing_contact

phonebook: dict = {}


def load_phonebook() -> None:
    """Загрузка телефонной книги из файла для дальнейшей работы с данными."""
    try:
        with open("phonebook.txt", "r") as file:
            global phonebook
            phonebook = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        pass


def save_phonebook() -> None:
    """Сохранение изменений данных и запись в файл."""
    try:
        with open("phonebook.txt", "w") as file:
            json.dump(phonebook, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def display_phonebook() -> None:
    """Отображение списка записей в книге постранично с меню действий."""
    contacts: dict = phonebook["contacts"]
    display_contacts(contacts, 3)


def add_contact() -> None:
    """Добавление новой записи. Сохранение и загрузка обновленного файла."""
    try:
        print('Новая запись в книге.')
        contact: dict = {
            "last_name": input('Введите фамилию:').capitalize(),
            "first_name": input('Введите Имя: ').capitalize(),
            "middle_name": input('Введите Отчество: ').capitalize(),
            "company": input('Введите организацию: '),
            "work_phone": input('Рабочий номер: '),
            "personal_phone": input('Личный номер: ')
        }
        # Добавление новой записи к данным и сохранение файла
        phonebook['contacts'][len(phonebook['contacts']) + 1] = contact
        save_phonebook()
        load_phonebook()
        print("Запись успешно добавлена.")
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def edit_contact() -> None:
    """Редактирование записи. Сохранение и загрузка обновленного файла."""
    try:
        data: dict = phonebook["contacts"]
        records_for_edit: list = search_contacts()
        if len(records_for_edit) == 1:
            record_id = records_for_edit[0]
            if record_id in phonebook["contacts"].keys():
                phonebook["contacts"][record_id] = editing_contact(data, record_id)
                save_phonebook()
                load_phonebook()
                print("Запись успешно изменена.")
            else:
                print("Введены неверные данные.")
        else:
            record_id = input('Укажите номер записи, которую хотите редактировать : ')
            if record_id in phonebook["contacts"].keys():
                phonebook["contacts"][record_id] = editing_contact(data, record_id)
                save_phonebook()
                load_phonebook()
                print("Запись успешно изменена.")
            else:
                print("Введены неверные данные.")
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def search_contacts() -> list:
    """
    Поиск записей в телефонной книге и их отображение в консоли.
    :return: Список номеров найденных записей
    """
    try:
        search_value: str = input('Укажите данные для поиска записи (ФИО, организация или номер телефона) : ')
        find_records: dict = search_json(phonebook, search_value)
        list_id: list = []
        if find_records:
            print("Результаты поиска:")
            for key in find_records: # Отображение результатов поиска
                record_id = str(key).lstrip('/').split('/')[1]
                values = find_records[key]
                print(f"{record_id}. {values['last_name']} {values['first_name']} {values['middle_name']},"
                      f" {values['company']}, Рабочий: {values['work_phone']}, Личный: {values['personal_phone']}")
                list_id.append(record_id)
        else:
            search_value = search_value.capitalize() # Вторая попытка поиска строки с большой буквы
            find_records: dict = search_json(phonebook, search_value)
            if find_records:
                print("Результаты поиска:")
                for key in find_records:
                    record_id = str(key).lstrip('/').split('/')[1]
                    values = find_records[key]
                    print(f"{record_id}. {values['last_name']} {values['first_name']} {values['middle_name']},"
                          f" {values['company']}, Рабочий: {values['work_phone']}, Личный: {values['personal_phone']}")
                    list_id.append(record_id)
            else:
                print("Объекты с таким значением не найдены.")
        return list_id
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


load_phonebook() # загрузка данных из файла


def start_program() -> None:
    """Запуск программы и основное меню."""
    try:
        print('\nМеню:')
        print('1. Просмотреть книгу')
        print('2. Добавить новую запись')
        print('3. Редактировать запись')
        print('4. Поиск')
        print('5. Выход')
        choice: str = input('Введите нужный пункт меню: ')
        if choice == '1':
            display_phonebook()
        elif choice == '2':
            add_contact()
        elif choice == '3':
            edit_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            save_phonebook()
            print('До свидания!')
            sys.exit()
        else:
            print('Введены неверные данные.')
            start_program()
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


while True:
    start_program()
