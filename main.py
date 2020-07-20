from util import resource_path
import kivy.resources
from ui.KivyPlyerGui import RSS2VidApp

kivy.resources.resource_add_path(resource_path('ui'))

RSS2VidApp().run()
