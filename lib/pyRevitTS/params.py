# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

from pyRevitTS.my_utils import get_param_definition
from ts_variables import list_identification, parameter_type_mapping


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


def compare_parameters(doc, param_group, list_params=list_identification):
    """
    Сравнивает параметры из файла общих параметров с параметрами,
    ожидаемыми в проекте, и возвращает список отсутствующих
    параметров и параметры с несовпадающим типом.

    :param doc: Документ Revit, используемый для доступа к приложению.
    :param param_group: Название группы параметров для проверки.
    :param list_params: Список параметров, который нужно сравнить с параметрами в ФОП,
                        по умолчанию берется из list_identification.
    :return: Словарь, содержащий два списка:
             - 'missing_params': параметры, отсутствующие в проекте.
             - 'type_mismatch_params': параметры с несовпадающим типом,
               где указаны ожидаемый и фактический типы.
    """
    # Получаем параметры из файла общих параметров
    fop_parameters = get_params_of_fop(doc, param_group)

    # Преобразуем fop_parameters в словарь для быстрого поиска по имени
    fop_params_dict = {param['param_name']: param for param in fop_parameters}

    missing_params = []  # Список отсутствующих параметров в ФОП
    type_mismatch_params = []  # Список неверно указанных типов параметров в ФОП

    # Проверяем параметры из list_identification
    for param in list_params:
        param_name = param['param_name']
        # Получаем тип параметра из list_identification с типом ParameterType
        param_type_in_revit = parameter_type_mapping.get(param['param_type_inRevit'])

        # Используем get для проверки наличия параметра
        fop_param = fop_params_dict.get(param_name)
        if fop_param is None:
            # Если параметр отсутствует в файле общих параметров
            missing_params.append(param)
        else:
            # Получаем тип параметра из файла общих параметров с типом ParameterType
            actual_type = fop_param.get('param_type')

            # Проверяем соответствие типа параметра из list_identification в ФОП
            if param_type_in_revit != actual_type:
                type_mismatch_params.append({
                    'param_name': param_name,
                    'expected_type': param_type_in_revit,
                    'actual_type': actual_type
                })

    return {
        'missing_params': missing_params,
        'type_mismatch_params': type_mismatch_params
    }


def add_shared_parameter(doc, param_name, param_group, param_categories):
    """
    Добавление общего параметра к указанным категориям.

    :param doc: Текущий документ Revit (__revit__.ActiveUIDocument.Document).
    :param param_name: Наименование параметра, пример "Класс".
    :param param_group: Группа параметров, пример "Идентификация".
    :param param_categories: Список встроенных категорий, к которым добавляется параметр (список элементов BuiltInCategory).
    :return: None
    """
    app = doc.Application
    transaction = Transaction(doc, "Добавление общего параметра")

    try:
        transaction.Start()

        param_definition = get_param_definition(param_name, param_group)
        category_set = app.Create.NewCategorySet()

        # Добавляем все категории в набор категорий
        for built_in_category in param_categories:
            category = doc.Settings.Categories.get_Item(built_in_category)
            category_set.Insert(category)

        instance_binding = app.Create.NewInstanceBinding(category_set)
        binding_map = doc.ParameterBindings
        binding_map.Insert(param_definition, instance_binding, BuiltInParameterGroup.PG_IDENTITY_DATA)

        transaction.Commit()
        print("Параметр '{}' добавлен к категориям.".format(param_name))
        return True

    except Exception as e:
        transaction.RollBack()
        print("Ошибка при добавлении параметра '{}': {}".format(param_name, str(e)))
        return False


# Функция для проверки параметра в списке категорий

def is_parameter_in_category(doc, built_in_category, param_name):
    # Получаем объект Category из BuiltInCategory
    category = doc.Settings.Categories.get_Item(built_in_category)

    # Проверяем, есть ли параметр с заданным именем у категории
    binding_map = doc.ParameterBindings
    it = binding_map.ForwardIterator()
    it.Reset()

    while it.MoveNext():
        definition = it.Key
        binding = it.Current
        if binding.Categories.Contains(category) and definition.Name == param_name:
            return True

    return False


def check_parameter_in_categories(doc, param_name, built_in_categories):
    """
    Проверяет наличие параметра с заданным именем в списке категорий и выводит результаты.

    Параметры:
    :param doc: Текущий документ Revit. (Document)
    :param param_name: Имя параметра, который нужно проверить. (str)
    :param built_in_categories: Список категорий, в которых необходимо проверить наличие параметра. (list of BuiltInCategory)

    :return:
        tuple: (categories_with_param, categories_without_param)
               categories_with_param: Список категорий, в которых параметр существует.
               categories_without_param: Список категорий, в которых параметр отсутствует.
    """
    categories_with_param = []  # Список категорий, в которых параметр существует
    categories_without_param = []  # Список категорий, в которых параметр отсутствует
    for built_in_category in built_in_categories:

        if is_parameter_in_category(doc, built_in_category, param_name):
            categories_with_param.append(built_in_category)

        else:
            categories_without_param.append(built_in_category)

    return categories_with_param, categories_without_param


def get_ru_category_names(category_dict, list_built_in_category):
    # Инвертируем словарь для быстрого поиска
    inverted_dict = {val: key for key, val in category_dict.items()}

    # Используем списковое включение для создания списка имен категорий
    param_categories = [inverted_dict[built_in_category] for built_in_category in list_built_in_category if
                        built_in_category in inverted_dict]

    return param_categories

# # Пример использования функции для добавления параметра "Класс" ко всем трубам
# doc = __revit__.ActiveUIDocument.Document

# # Добавляем параметр "Класс" ко всем элементам категории "Трубы"
# add_shared_parameter(doc, "Класс", "МояГруппа", [BuiltInCategory.OST_PipeCurves, BuiltInCategory.OST_PipeFitting])
