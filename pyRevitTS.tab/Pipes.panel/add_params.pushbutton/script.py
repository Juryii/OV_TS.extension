# -*- coding: utf-8 -*-
__title__ = "add params"  # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 05.10.2024
_____________________________________________________________________
Description:
Добавление параметров для классов элементов
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [05.10.2024] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Yuri Polyanskii"""  # Button Description shown in Revit UI

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
# Regular + Autodesk
import os  # Regular Imports

# .NET Imports
import clr  # Common Language Runtime. Makes .NET libraries accessible

from pyRevitTS.params import add_shared_parameter, check_parameter_in_categories, \
    get_ru_category_names

clr.AddReference("System")  # Reference System.dll for import.

# noinspection PyUnresolvedReferences
doc = __revit__.ActiveUIDocument.Document  # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
# noinspection PyUnresolvedReferences
uidoc = __revit__.ActiveUIDocument  # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
# noinspection PyUnresolvedReferences
app = __revit__.Application  # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)  # Absolute path to the folder where script is placed.

from pyRevitTS.ts_variables import list_identification, categories_mapping
from Autodesk.Revit.DB import TransactionGroup

if __name__ == '__main__':
    # Создаем групповую транзакцию для добавления параметров
    transaction_group = TransactionGroup(doc, "Добавление параметров")
    transaction_group.Start()  # Запускаем групповую транзакцию

    try:
        # Проходим по каждому параметру из списка идентификации
        for param in list_identification:
            # Получаем имя параметра и соответствующие категории
            param_name = param['param_name']
            param_categories = param['param_categories']

            # Получаем встроенные категории, используя отображение (mapping)
            built_in_categories = [categories_mapping.get(category) for category in param['param_categories']]

            # Проверяем наличие параметра в категориях
            categories_with_param, categories_without_param = check_parameter_in_categories(doc, param_name,
                                                                                            built_in_categories)

            # Если параметр отсутствует в каких-либо категориях
            if categories_without_param:
                # Получаем русские названия категорий, в которых отсутствует параметр
                ru_names = get_ru_category_names(category_dict=categories_mapping,
                                                 list_built_in_category=categories_without_param)
                # Выводим информацию о категориях, где параметр отсутствует
                print("Параметр '{}' отсутствует в следующих категориях: {}.".format(param_name, ', '.join(ru_names)))

                # Добавляем параметр в категории, где его нет
                result = add_shared_parameter(doc, param_name=param_name, param_group="Идентификация",
                                              param_categories=categories_without_param)

                # Проверяем результат добавления параметра и выводим соответствующее сообщение
                if result:
                    print("Параметр '{}' был успешно добавлен.".format(param_name))
                else:
                    print("Не удалось добавить параметр '{}'.".format(param_name))

            # Если параметр уже существует в каких-либо категориях
            if categories_with_param:
                # Получаем русские названия категорий, где параметр существует
                ru_names = get_ru_category_names(category_dict=categories_mapping,
                                                 list_built_in_category=categories_with_param)
                # Выводим информацию о категориях, где параметр существует
                print("Параметр '{}' существует в следующих категориях: {}.".format(param_name, ', '.join(ru_names)))

        # Применяем групповую транзакцию, если все прошло успешно
        transaction_group.Assimilate()

    except Exception as e:
        # Откатываем транзакцию в случае возникновения ошибки
        transaction_group.RollBack()
        # Выводим сообщение об ошибке
        print("Ошибка: {}".format(str(e)))

    print('-' * 50)
    print('Hold ALT + Click on the button to open its source folder.')
