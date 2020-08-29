from kivy.clock import mainthread, Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from src.constants import LOADING_STRING, COUNTING_STRING, DONE_STRING, ERROR_STRING
from kivymd.uix.dialog import MDDialog

loading_kv = '''
<Content>:
    orientation: 'vertical'
    on_progress: self.progress_text = self.create_progress_text()
    on_total: self.progress_text = self.create_progress_text()
    on_done: self.progress_text = self.create_progress_text()
    MDLabel:
        text: root.progress_text
        halign: "center"
        font_style: 'Subtitle1'
    MDProgressBar:
        max: root.total
        value: root.progress
'''


class Content(BoxLayout):
    progress = NumericProperty(defaultvalue=0)
    total = NumericProperty(defaultvalue=100)
    progress_text = StringProperty(defaultvalue=COUNTING_STRING)
    image = StringProperty()
    done = BooleanProperty(defaultvalue=False)
    errors = ListProperty(defaultvalue=[])

    def create_progress_text(self):
        if len(self.errors) > 0:
            return ERROR_STRING.format(str(len(self.errors)), self.errors[0])
        elif self.done:
            return DONE_STRING
        elif self.progress > 0:
            return LOADING_STRING.format(str(self.progress), str(self.total))
        else:
            return COUNTING_STRING


class CloseButton(MDRaisedButton):
    pass


class LoadingPopup(MDDialog):
    Builder.load_string(loading_kv)

    def __init__(self, title: str):
        self.content_cls = Content()
        self.type = 'custom'
        self.auto_dismiss = False
        super().__init__(title=title)

    @mainthread
    def update_progress(self, progress: int, total: int):
        self.content_cls.progress = progress
        self.content_cls.total = total

    def close(self, errors: []):
        self.content_cls.errors = errors
        self.content_cls.done = True
        Clock.schedule_once(self.dismiss, 5)






