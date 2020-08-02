from util import resource_path, data_path

from kivy.config import Config
Config.set('kivy', 'log_dir', data_path(''))

import kivy.resources
kivy.resources.resource_add_path(resource_path('ui'))

from ui.KivyPlyerGui import RSS2VidApp
RSS2VidApp().run()

