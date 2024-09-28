# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

from pyRevitTS.my_utils import translate_param_type
from ts_variables import list_identification


def get_params_of_fop(doc, param_group):
    """
    Получает параметры из файла общих параметров.

    :param doc: Документ Revit, используемый для доступа к приложению.
    :param param_group: Название группы параметров для поиска.
    :return: Список словарей с именем и типом параметра.
    """
    params = []

    # Загружаем файл общих параметров
    app = doc.Application
    shared_param_file = app.OpenSharedParameterFile()

    # Проверяем загружен ли файл ФОП в приложении
    if shared_param_file is None:
        print("Файл общих параметров не найден.")
        return params

    group_found = False
    for group in shared_param_file.Groups:
        if group.Name == param_group:
            group_found = True
            for definition in group.Definitions:
                param = {
                    "param_name": definition.Name,
                    "param_type": definition.ParameterType
                }
                params.append(param)
            return params

    if not group_found:
        print("Группа '{}' не найдена в файле общих параметров.".format(param_group))

    return params


def compare_parameters(doc, param_group):
    """
    Сравнивает параметры из файла общих параметров с параметрами,
    ожидаемыми в проекте, и возвращает список отсутствующих
    параметров и параметры с несовпадающим типом.

    :param doc: Документ Revit, используемый для доступа к приложению.
    :param param_group: Название группы параметров для проверки.
    :return: Словарь, содержащий два списка:
             - 'missing_params': параметры, отсутствующие в проекте.
             - 'type_mismatch_params': параметры с несовпадающим типом,
               где указаны ожидаемый и фактический типы.
    """
    # Получаем параметры из файла общих параметров
    fop_params = get_params_of_fop(doc, param_group)

    # Преобразуем fop_params в словарь для быстрого поиска по имени
    fop_params_dict = {param['param_name']: param for param in fop_params}

    missing_params = []
    type_mismatch_params = []

    # Проверяем параметры из list_identification
    for param in list_identification:
        param_name = param['param_name']
        param_type_in_revit = translate_param_type(param['param_type_inRevit'], to_english=True)

        if param_name not in fop_params_dict:
            # Если параметр отсутствует в файле общих параметров
            missing_params.append(param)
        else:
            # Преобразуем тип параметра из файла общих параметров в строку
            actual_type = str(fop_params_dict[param_name]['param_type'])
            # Приводим оба типа к нижнему регистру и удаляем пробелы для точного сравнения
            if param_type_in_revit.strip().lower() != actual_type.strip().lower():
                type_mismatch_params.append({
                    'param_name': param_name,
                    'expected_type': param_type_in_revit,
                    'actual_type': actual_type
                })

    return {
        'missing_params': missing_params,
        'type_mismatch_params': type_mismatch_params
    }

def add_shared_parameter(doc, param_name, param_group, category, param_type):
    """
    Добавление общего параметра

    Аргументы:
    doc -- __revit__.ActiveUIDocument.Document
    param_name -- наименование параметра, пример "Класс"
    param_group -- группа параметров, прим "Идентификация"
    category -- категория элементов для которых добавляется параметр, пример BuiltInCategory.OST_PipeCurves
    param_type -- тип параметра, пример ParameterType.Text
    """
    app = doc.Application
    # Открываем Transaction (транзакцию)
    transaction = Transaction(doc, "Добавление общего параметра")
    transaction.Start()

    # Загружаем файл общих параметров
    app = doc.Application
    shared_param_file = app.OpenSharedParameterFile()

    if shared_param_file is None:
        print("Файл общих параметров не найден.")
        return

    # Ищем общий параметр по имени
    param_definition = None
    for group in shared_param_file.Groups:
        if group.Name == param_group:
            for definition in group.Definitions:
                if definition.Name == param_name:
                    param_definition = definition
                    break

    if param_definition is None:
        print("Параметр {} не найден в группе {}.".format(param_name, param_group))
        return

    # Создаем привязку параметра к категории
    category_set = app.Create.NewCategorySet()
    category_set.Insert(doc.Settings.Categories.get_Item(category))

    # Создаем привязку параметра к типу экземпляра
    instance_binding = app.Create.NewInstanceBinding(category_set)

    # Добавляем параметр в документ
    binding_map = doc.ParameterBindings
    binding_map.Insert(param_definition, instance_binding, BuiltInParameterGroup.PG_IDENTITY_DATA)

    transaction.Commit()
    print("Параметр {} добавлен к категории {}.".format(param_name, group.Name))

# # Пример использования функции для добавления параметра "Класс" ко всем трубам
# doc = __revit__.ActiveUIDocument.Document

# # Добавляем параметр "Класс" ко всем элементам категории "Трубы"
# add_shared_parameter(doc, "Класс", "МояГруппа", BuiltInCategory.OST_PipeCurves, ParameterType.Text)
