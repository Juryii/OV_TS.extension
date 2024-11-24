# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from pyrevit import forms
import wpf, os, clr

# .NET Imports
clr.AddReference("System")
clr.AddReference("PresentationFramework")
from System.Windows import Application, Window
from System.Windows.Controls import UserControl

from System.Windows.Media.Animation import DoubleAnimation
from System import TimeSpan
from System.Windows import Duration
from System.Windows.UIElement import OpacityProperty


PATH_SCRIPT = os.path.dirname(__file__)


# Первая страница как UserControl
class MainPage(UserControl):
    def __init__(self, parent_window):
        wpf.LoadComponent(self, os.path.join(PATH_SCRIPT, 'main_page.xaml'))
        self.parent_window = parent_window

        # Привязка обработчиков событий
        self.testButton.Click += self.test_button_click

    def test_button_click(self, sender, args):
        """Переключение на вторую страницу"""
        self.parent_window.navigate_to_page("second")


# Вторая страница как UserControl
class SecondPage(UserControl):
    def __init__(self, parent_window):
        wpf.LoadComponent(self, os.path.join(PATH_SCRIPT, 'second_page.xaml'))
        self.parent_window = parent_window

        # Привязка обработчиков событий
        self.homeButton.Click += self.home_button_click

    def home_button_click(self, sender, args):
        """Возврат на главную страницу"""
        self.parent_window.navigate_to_page("main")


# Главное окно приложения
class MainWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, os.path.join(PATH_SCRIPT, 'main_window.xaml'))

        # Инициализация страниц
        self.pages = {
            "main": MainPage(self),
            "second": SecondPage(self)
        }

        # Установка начальной страницы
        self.navigate_to_page("main")

        # Показать окно
        self.ShowDialog()

    def navigate_to_page(self, page_name):
        if page_name in self.pages:
            # Создаем анимацию fade out
            fade_out = DoubleAnimation(1, 0, Duration(TimeSpan.FromSeconds(0.2)))

            # После завершения fade out меняем страницу и делаем fade in
            def on_completed(s, e):
                self.contentControl.Content = self.pages[page_name]
                fade_in = DoubleAnimation(0, 1, Duration(TimeSpan.FromSeconds(0.2)))
                self.contentControl.BeginAnimation(OpacityProperty, fade_in)

            fade_out.Completed += on_completed
            self.contentControl.BeginAnimation(OpacityProperty, fade_out)


if __name__ == '__main__':
    main_window = MainWindow()