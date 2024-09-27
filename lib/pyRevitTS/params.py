# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

# noinspection PyUnresolvedReferences
doc = __revit__.ActiveUIDocument.Document


def add_shared_parameter(doc, param_name, param_group, category, param_type):
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
