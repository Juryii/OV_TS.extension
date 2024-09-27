# -*- coding: utf-8 -*-

__title__ = "check params"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 07.09.2024
_____________________________________________________________________
Description:
Проверка параметров у элементов модели.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [24.04.2022] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Yura Polyanskii"""                                           # Button Description shown in Revit UI

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
# Regular + Autodesk
import os  # Regular Imports
import re

# .NET Imports
import clr  # Common Language Runtime. Makes .NET libraries accessible
from Autodesk.Revit.DB import *  # Import everything from DB (Very good for beginners)

# Custom Imports
from pyRevitTS.my_utils import *  # lib import
from pyRevitTS.params import add_shared_parameter

# pyRevit
clr.AddReference("System")                  # Reference System.dll for import.
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentheses.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
# noinspection PyUnresolvedReferences
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.

# noinspection PyUnresolvedReferences
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
# noinspection PyUnresolvedReferences
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

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
    pipes = get_pipes()
    # pipe_d = get_param_value("Размер", pipes[0])
    # print(pipe_d["param_value"])
    # print(pipe_d["param_type"])
    # pipe_name = pipes[0].Name
    # print(extract_gost(pipe_name))
    # # pipe_l = get_param_value("Длина", pipes[0])
    add_shared_parameter(doc, "Класс", "Идентификация", BuiltInCategory.OST_PipeCurves, ParameterType.Text)
    param_val = get_param_value("Класс", pipes[0])
    print(param_val)
    
    # pipe_dn = get_param_value("Внешний диаметр", pipes[0])
    # pipe_project = get_param_value("Код проекта", pipes[0])

    # Use Transaction for Changes.
    # t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.
    # AVOID  placing Transaction inside your loops! It will drastically reduce performance of your script.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    # t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE

    # t.Commit()  # <- Transaction End


    # Notify user that script is complete.
    print('-' * 50)
    print('Hold ALT + Click on the button to open its source folder.')