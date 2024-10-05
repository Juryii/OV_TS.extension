# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, StorageType, UnitTypeId

# noinspection PyUnresolvedReferences
doc = __revit__.ActiveUIDocument.Document


def get_pipes():
    pipes = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements()
    return pipes


def get_param_value(param_name, element):
    """
    Получение значение параметра у элемента
    """
    params = [param.Definition.Name for param in element.Parameters]

    if param_name not in params:
        # print("Параметр '{}' отсутствует у данного элемента".format(param_name))
        return None
    else:
        for param in element.Parameters:
            if param.Definition.Name == param_name:
                if param.HasValue:
                    if param.StorageType == StorageType.String:
                        param_value = param.AsString()
                        param_type = "String"
                    elif param.StorageType == StorageType.Integer:
                        param_value = param.AsInteger()
                        param_type = "Integer"
                        if param_value == 0:
                            param_value = "Ложь"
                        elif param_value == 1:
                            param_value = "Истина"
                        else:
                            param_value = "Неизвестное значение"
                    elif param.StorageType == StorageType.Double:
                        param_value = param.AsDouble()
                        # Получаем единицы измерения через другие методы
                        unit_type_id = UnitTypeId.Feet  # Замените на правильное значение
                        # unit_type_id = get_unit_type_for_param(param) 
                        param_value_mm = convert_to_mm(param_value, unit_type_id)
                        param_value = round(param_value_mm, 3)
                        param_type = "Double"
                    elif param.StorageType == StorageType.ElementId:
                        param_value = param.AsElementId().IntegerValue
                        param_type = "ElementId"
                    else:
                        param_value = "Неизвестный тип значения"
                        param_type = None
                    # print("Параметр '{}' имеет значение {} Тип {}".format(param_name, param_value, param_type))
                    return {"param_value": param_value, "param_type": param_type}
                else:
                    # print("Параметр '{}' не имеет значения".format(param_name))
                    param_value = None
                    param_type = None
                    return {"param_value": param_value, "param_type": param_type}


def convert_to_mm(value, unit_type_id):
    if unit_type_id == UnitTypeId.Feet:
        return value * 304.8
    elif unit_type_id == UnitTypeId.Inches:
        return value * 25.4
    elif unit_type_id == UnitTypeId.Meters:
        return value * 1000
    elif unit_type_id == UnitTypeId.Millimeters:
        return value
    else:
        raise ValueError("Неизвестный тип единиц измерения: {}".format(unit_type_id))


def get_param_definition(param_name, param_group):
    """
    Получает определение общего параметра из файла общих параметров по имени и группе.

    Параметры:
    :param param_name: Имя общего параметра, который нужно найти. (str)
    :param param_group: Имя группы, в которой ищется параметр. (str)

    :return:
        Определение параметра (Definition) если найден, иначе None.
    """
    app = doc.Application  # Получаем приложение Revit
    # Загружаем файл общих параметров (Shared Parameter File)
    shared_param_file = app.OpenSharedParameterFile()

    # Если файл общих параметров не найден, выводим сообщение и выходим из функции
    if shared_param_file is None:
        print("Файл общих параметров не найден.")
        return None  # Возвращаем None, если файл не найден

    # Ищем общий параметр по имени в файле общих параметров
    param_definition = None  # Инициализируем переменную для хранения определения параметра
    for group in shared_param_file.Groups:  # Проходим по всем группам в файле общих параметров
        # Проверяем, совпадает ли имя группы с указанным
        if group.Name == param_group:
            # Ищем параметр по имени внутри группы
            for definition in group.Definitions:  # Проходим по всем определениям в группе
                if definition.Name == param_name:  # Проверяем, совпадает ли имя параметра
                    param_definition = definition  # Сохраняем определение параметра
                    break  # Выходим из цикла, если параметр найден

    # Если параметр не найден в указанной группе, выводим сообщение
    if param_definition is None:
        print("Параметр {} не найден в группе {}.".format(param_name, param_group))
        return None  # Возвращаем None, если параметр не найден

    return param_definition  # Возвращаем найденное определение параметра
