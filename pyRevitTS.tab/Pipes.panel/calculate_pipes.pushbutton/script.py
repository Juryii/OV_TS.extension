# -*- coding: utf-8 -*-

__title__ = "Calculate pipes"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 07.09.2024
_____________________________________________________________________
Description:
Расчет длинны все труб.
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
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# Custom Imports
from pyRevitTS.my_utils import *                                        # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

# GLOBAL VARIABLES

# - Place global variables here.

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ 🧬 FUNCTIONS
# ==================================================
def group_pipes(pipes):
    grouped_pipes = {}
    
    for pipe in pipes:
        diameter = str(int(get_param_value("Диаметр", pipe)["param_value"]))
        
        length = round(float(get_param_value("Длина", pipe)["param_value"]), 3)
        # length = round(length, 3)
        group_name = "DN" + diameter
        
        if group_name not in grouped_pipes:
            # Инициализируем новый список, если ключа нет
            grouped_pipes[group_name] = []
        
        # Добавляем значение длины в список
        grouped_pipes[group_name].append(length)
    
    return grouped_pipes

def calc_pipe_length(pipe_dict):
    pipe_lengths = {}
    
    for key in pipe_dict.keys():
        total_length = 0
        for length in pipe_dict[key]:
            total_length += length  # Суммируем длины труб
        
        pipe_lengths[key] = total_length  # Записываем общую длину для диаметра
    
    return pipe_lengths

# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ ⏹️ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================
if __name__ == '__main__':

    # START CODE HERE
    pipes = get_pipes()
    new_pipes = group_pipes(pipes)
    print(new_pipes)
    pipe_lengths = calc_pipe_length(new_pipes)
    print(pipe_lengths)
    # pipe_d = get_param_value("Размер", pipes[0])
    # print(pipe_d["param_value"])
    # print(pipe_d["param_type"])

    # pipe_l = get_param_value("Длина", pipes[0])



    

    # pipe_dn = get_param_value("Внешний диаметр", pipes[0])
    # pipe_project = get_param_value("Код проекта", pipes[0])

    
    # for pipe in pipes:
    #     print(pipe.Name)
    #     print(pipe.Parameters)
    # params = pipes[0].Parameters

    # for param in params:
    #     param_name = param.Definition.Name
    #     if param.HasValue:
    #         param_value = param.AsValueString()  # или AsString(), AsDouble(), в зависимости от типа данных
    #     else:
    #         param_value = "No value"
    #     print("Параметр {0} - значение: {1}".format(param_name, param_value))

    
    # print("hello world")
    # get_pipes()


    # Use Transaction for Changes.
    # t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.
    # AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    # t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE

    # t.Commit()  # <- Transaction End


    # Notify user that script is complete.
    print('-' * 50)
    print('Hold ALT + Click on the button to open its source folder.')