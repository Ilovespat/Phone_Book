import math


def search_json(data: dict, search_value: str, path: str = "") -> dict:
    """
    Поиск по файлу.

    :param data: Данные файла, по которому производится поиск
    :param search_value: Значение, которое ищем
    :param path: Путь в файле до объекта, который совпал с поиском
    :return: dict - словарь с результатами поиска
    """
    try:
        results: dict = {}  # Словарь для хранения результатов поиска
        # Проверяем, является ли data словарем
        if isinstance(data, dict):
            # Перебираем все ключи и значения в словаре
            for key, value in data.items():
                # Формируем новый путь к текущему элементу, добавляя ключ к существующему пути
                new_path = path + "/" + str(key)
                # Проверяем, является ли значение словарем или списком
                if isinstance(value, dict) or isinstance(value, list):
                    # Если значение является словарем или списком, то рекурсивно вызываем текущую функцию для этого значения
                    results.update(search_json(value, search_value, new_path))
                # Проверяем, совпадает ли значение с искомым
                elif str(value) == search_value:
                    # Если значение совпадает, то добавляем весь объект JSON в список results
                    results[new_path] = data
        # Проверяем, является ли data списком (в зависимости от структуры файла JSON)
        elif isinstance(data, list):
            # Перебираем все элементы списка
            for i, item in enumerate(data):
                # Формируем новый путь к текущему элементу, добавляя индекс элемента к существующему пути
                new_path = path + "[" + str(i) + "]"
                # Проверяем, является ли элемент словарем или списком
                if isinstance(item, dict) or isinstance(item, list):
                    # Если элемент является словарем или списком, то рекурсивно вызываем текущую функцию для этого элемента
                    results.update(search_json(item, search_value, new_path))
                # Проверяем, совпадает ли элемент с искомым значением
                elif str(item) == search_value:
                    # Если элемент совпадает с искомым значением, то добавляем весь объект JSON в список results
                    results[new_path] = data
        return results
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def display_contacts(data: dict, page_size: int = 3) -> None:
    """
    Выводит список контактов постранично.

    :type page_size: int
    :param data: Данные файла, которые выводятся
    :param page_size: Количество записей на странице, по умолчанию 3
    """
    try:
        page_index: int = 1  # Номер текущей страницы
        start_index: int = 0  # Индекс, с которого начинается отображение на странице
        quantity_of_pages: int = math.ceil(len(data) / page_size)  # Расчет количества страниц
        keys: list = list(data.keys())  # Список ключей из данных файла, для создания среза
        # Цикл для вывода страниц
        while start_index < len(keys):
            # Получаем объекты для текущей страницы - словарь из среза списка ключей с нужными для отображения индексами
            page_data: dict = {key: data[key] for key in keys[start_index:start_index + page_size]}
            print(f'Страница {page_index} из {quantity_of_pages}:')
            # Выводим объекты на консоль
            for key in page_data:
                values = page_data[key]
                # Формирование вывода для консоли
                displayable: str = (f"{key}. {values['last_name']} {values['first_name']} {values['middle_name']}, "
                                    f"{values['company']}, Рабочий: {values['work_phone']}, Личный: {values['personal_phone']}")
                print(displayable)
            if page_index < quantity_of_pages:  # Печать разных меню в зависимости от текущей страницы
                text = (f'{'-' * len(displayable)}\nНажмите \'Enter\' для просмотра следующей страницы, '
                        f'\'R\' для редактирования записи или \'Q\' для возврата в меню: ')
                user_input = input(text)
                if user_input.lower() == 'r' or user_input.lower() == 'к':
                    edit_contact_from_display(data)
                    break
                elif user_input.lower() == 'q' or user_input.lower() == 'й':
                    break
            else:
                text = (f'{'-' * len(displayable)}\nЭто последняя страница. Нажмите \'R\' для редактирования записи,'
                        f' \'Q\' или \'Enter\' для возврата в меню.')
                user_input = input(text)
                if user_input.lower() == 'r' or user_input.lower() == 'к':
                    edit_contact_from_display()
                    break
                elif user_input.lower() == 'q' or user_input.lower() == 'й':
                    break
            page_index += 1
            start_index += page_size
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def edit_contact_from_display(data: dict) -> None:
    """
    Редактирование контакта при вызове из отображения списка контактов.
    Принимает данные из файла и редактирует выбранную пользователем запись.

    :param data: Данные, с которыми работает функция
    """
    try:
        record_id: str = input('Укажите номер записи, которую хотите редактировать : ')
        if record_id in data.keys(): # Проверка ввода пользователя
            if editing_contact(data, record_id):
                print("Запись успешно изменена.")
        else:
            print("Введены неверные данные.")
    except Exception as e:
        print(f'Ошибка:{e}')
        pass


def editing_contact(data: dict, record_id: str) -> dict:
    """
    Редактирование записи в телефонной книге.
    :param data: Данные, с которыми работает функция
    :param id: Номер записи для редактирования
    :return: Запись с измененными данными
    """
    try:
        contact: dict = data[record_id]
        print('Поля для редактирования:')
        print('1. Фамилия')
        print('2. Имя')
        print('3. Отчество')
        print('4. Организация')
        print('5. Рабочий номер')
        print('6. Личный номер')
        edit_record: str = input('Укажите, что будете редактировать: ')
        if edit_record == '1':
            contact["last_name"] = input('Введите фамилию:').capitalize()
        elif edit_record == '2':
            contact["first_name"] = input('Введите Имя: ').capitalize()
        elif edit_record == '3':
            contact["middle_name"] = input('Введите Отчество: ').capitalize()
        elif edit_record == '4':
            contact["company"] = input('Введите организацию: ')
        elif edit_record == '5':
            contact["work_phone"] = input('Рабочий номер: ')
        elif edit_record == '6':
            contact["personal_phone"] = input('Личный номер: ')
        else:
            print('Введены некорректные данные.')
        displayable: str = (f"{record_id}. {contact['last_name']} {contact['first_name']} {contact['middle_name']}, {contact['company']}"
                  f", Рабочий: {contact['work_phone']}, Личный: {contact['personal_phone']}")
        print(f'Новые данные:\n')
        print(displayable)
        print(f'{'-' * len(displayable)}\n')
        return contact
    except Exception as e:
        print(f'Ошибка:{e}')
        pass
