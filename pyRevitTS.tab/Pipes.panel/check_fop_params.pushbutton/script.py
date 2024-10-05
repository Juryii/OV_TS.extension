# -*- coding: utf-8 -*-

__title__ = "check FOP params"  # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 07.09.2024
_____________________________________________________________________
Description:
Проверка параметров в файле общих параметров загруженного в проект.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [28.09.2022] - 1.0 RELEASE
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
import re

# .NET Imports
import clr  # Common Language Runtime. Makes .NET libraries accessible

# Custom Imports
from pyRevitTS.params import compare_parameters

# pyRevit
clr.AddReference("System")  # Reference System.dll for import.
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentheses.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
# noinspection PyUnresolvedReferences
doc = __revit__.ActiveUIDocument.Document  # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.

# noinspection PyUnresolvedReferences
uidoc = __revit__.ActiveUIDocument  # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
# noinspection PyUnresolvedReferences
app = __revit__.Application  # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)  # Absolute path to the folder where script is placed.


# GLOBAL VARIABLES

# - Place global variables here.

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ 🧬 FUNCTIONS
# ==================================================

def extract_gost(text):
    # Регулярное выражение для поиска ГОСТ
    match = re.search(r"ГОСТ\s\d{4,}-\d{2,}", text)

    if match:
        return match.group(0)
    else:
        return None


# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ ⏹️ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder. ts_variables

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================
if __name__ == '__main__':

    # START CODE HERE
    result = compare_parameters(doc, "Идентификация")

    # Вывод результатов
    print("Отсутствующие параметры в файле ФОП:")
    for param in result['missing_params']:
        print(" - {}".format(param['param_name']))

    print("\nПараметры с несовпадающим типом:")
    for param in result['type_mismatch_params']:
        print(" - Параметр '{}': ожидался тип '{}', фактически '{}'".format(
            param['param_name'],
            param['expected_type'],
            param['actual_type']
        ))


    # Notify user that script is complete.
    print('-' * 50)
    print('Hold ALT + Click on the button to open its source folder.')
