import kivy
from kivymd.app import MDApp

from model.ArgumentCacheManager import ArgumentCacheManager
from ui.Controller import Controller
from util import create_local_datetime, data_path
kivy.require('1.9.0')


class RSS2VidApp(MDApp):

    def build(self):
        self.icon = data_path('icon.png')
        argument_cache_manager = ArgumentCacheManager()
        config = argument_cache_manager.get_config()

        return Controller(argument_cache_manager,
                          image=config['DEFAULT']['IMAGE'],
                          url=config['DEFAULT']['RSS_URL'],
                          output_dir=config['DEFAULT']['BASE_DIR'],
                          video_format=config['DEFAULT']['EXT_OUTPUT_VIDEO'],
                          start_date=create_local_datetime(config['DEFAULT']['START_DATE']))


if __name__ == '__main__':
    RSS2VidApp().run()

