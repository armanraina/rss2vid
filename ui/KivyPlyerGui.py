import os

import kivy
from kivymd.app import MDApp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton

from ArgumentCacheManager import ArgumentCacheManager
from ui.Controller import Controller
from util import create_local_datetime
import os
kivy.require('1.9.0')


class RSS2VidApp(MDApp):

    def build(self):
        directory = os.getcwd()
        argument_cache_manager = ArgumentCacheManager(directory=directory)
        config = argument_cache_manager.get_config()

        return Controller(image=config['DEFAULT']['IMAGE'],
                          url=config['DEFAULT']['RSS_URL'],
                          output_dir=config['DEFAULT']['BASE_DIR'],
                          video_format=config['DEFAULT']['EXT_OUTPUT_VIDEO'],
                          start_date=create_local_datetime(config['DEFAULT']['START_DATE']))


if __name__ == '__main__':

    RSS2VidApp().run()

