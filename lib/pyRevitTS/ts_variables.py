# coding=utf-8
from Autodesk.Revit.DB import BuiltInCategory, ParameterType

list_identification = [
    {
        "param_name": "Идентификатор",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },
    {
        "param_name": "Идентификатор арматуры",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Арматура трубопроводов"]
    },
    {
        "param_name": "Идентификатор мест крепления трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Идентификатор типа фланца",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Идентификатор трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Идентификатор фланцевого соединения",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Класс давления фланцев",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Код крепления трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Код транспортируемой среды",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },
    {
        "param_name": "Материальный класс трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Материал",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "МНПЗ_Рабочий набор",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },
    {
        "param_name": "Номинальный диаметр",
        "param_type": "Общие",
        "param_type_inRevit": "Целое",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
        # почему не требуется для Арматуры трубопроводов ?
    },
    {
        "param_name": "Обозначение участка трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Порядковый номер",
        "param_type": "Общие",
        "param_type_inRevit": "Целое",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },
    {
        "param_name": "Порядковый номер мест креплений трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Целое",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Порядковый номер трубопровода",
        "param_type": "Общие",
        "param_type_inRevit": "Целое",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Порядковый номер фланцевого соединения трубопроводов",
        "param_type": "Общие",
        "param_type_inRevit": "Целое",
        "param_categories": ["Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Суффикс",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },
    {
        "param_name": "Тип арматуры",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Арматура трубопроводов"]
    },
    {
        "param_name": "Тип изоляции",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Тип обогрева",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов"]
    },
    {
        "param_name": "Установка",
        "param_type": "Общие",
        "param_type_inRevit": "Текст",
        "param_categories": ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
    },

]
"""
list_identification список обязательных параметров для идентификации элементов

elements {
    "param_name": Имя параметра,
    "param_type": Тип данных, значение "Общие"
    "param_type_inRevit": Тип данных в Revit, значения: "текст" или "Целое"
    "param_categories": список категорий для добавления параметров
    значения в списке категорий: ["Трубы", "Соединительные детали трубопроводов", "Арматура трубопроводов"]
}

"""

parameter_type_mapping = {
    "Текст": ParameterType.Text,
    "Целое": ParameterType.Integer,
    # Добавьте другие типы параметров
}

categories_mapping = {
    "Трубы": BuiltInCategory.OST_PipeCurves,
    "Соединительные детали трубопроводов": BuiltInCategory.OST_PipeFitting,
    "Арматура трубопроводов": BuiltInCategory.OST_PipeAccessory,
    # Добавьте другие соответствия
}
