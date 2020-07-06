from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from constants import LOADING_STRING, COUNTING_STRING, DONE_STRING
from kivymd.uix.dialog import MDDialog


class Content(BoxLayout):
    progress = NumericProperty(defaultvalue=0)
    total = NumericProperty(defaultvalue=100)
    progress_text = StringProperty(defaultvalue=COUNTING_STRING)
    image = StringProperty()
    done = BooleanProperty(defaultvalue=False)

    def create_progress_text(self):
        if self.done:
            return DONE_STRING
        if self.progress > 0:
            return LOADING_STRING.format(str(self.progress), str(self.total))
        else:
            return COUNTING_STRING


class CloseButton(MDRaisedButton):
    pass


class LoadingPopup(MDDialog):
    Builder.load_file('loading.kv')

    def __init__(self, image: str, title: str):
        self.content_cls = Content(image=image)
        self.image = image
        self.type = 'custom'
        self.buttons = [CloseButton(on_press=self.dismiss)]
        self.auto_dismiss = False
        super().__init__(title=title)

    @mainthread
    def update_progress(self, progress: int, total: int):
        self.content_cls.progress = progress
        self.content_cls.total = total

    def close(self):
        self.content_cls.done = True






