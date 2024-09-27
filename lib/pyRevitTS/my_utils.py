# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, StorageType, UnitUtils, UnitTypeId, DisplayUnit

doc   = __revit__.ActiveUIDocument.Document 


def get_pipes():
    pipes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements()
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
                    return {"param_value": param_value, "param_type" : param_type}
                else:
                    # print("Параметр '{}' не имеет значения".format(param_name))
                    param_value = None
                    param_type = None
                    return {"param_value": param_value, "param_type" : param_type}

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


