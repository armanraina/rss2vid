from kivymd.uix.picker import MDDatePicker
from plyer import filechooser
from datetime import datetime

from ProgressUpdater import ProgressUpdater
from Request import Request
from Downloader import Downloader
from Converter import Converter
from RequestProcessor import RequestProcessor
from FeedProvider import FeedProvider
from EpisodeProcessor import EpisodeProcessor
from FeedSearcher import FeedSearcher
import constants
import threading
from kivy.clock import mainthread
from kivy.properties import StringProperty, ObjectProperty, OptionProperty, BooleanProperty

from kivy.uix.boxlayout import BoxLayout
from ui.LoadingPopup import LoadingPopup


class Controller(BoxLayout):
    image_error = BooleanProperty(defaultvalue=False)
    url_error = BooleanProperty(defaultvalue=False)
    output_error = BooleanProperty(defaultvalue=False)
    date_error = BooleanProperty(defaultvalue=False)
    processing = BooleanProperty(defaultvalue=False)

    image = StringProperty(defaultvalue='')
    url = StringProperty(defaultvalue='')
    output_dir = StringProperty(defaultvalue='')

    video_format = OptionProperty(defaultvalue=constants.MKV_EXT,
                                  options=[constants.MKV_EXT, constants.MP4_EXT, constants.AVI_EXT])

    start_date = ObjectProperty(defaultvalue=datetime.now())
    loading_popup = ObjectProperty()

    def choose_image(self):
        files = filechooser.open_file(
            filters=[("Image files", "*.jpg; *.jpeg; *.png")])
        if files:
            self.image = files[0]

    def choose_dir(self):
        folders = filechooser.choose_dir()
        if folders:
            self.output_dir = folders[0]

    def set_start_date(self, date: datetime):
        if date:
            self.start_date = date

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.set_start_date)
        date_dialog.open()

    def process_button_handler(self):
        request = Request(self.url,
                          self.start_date,
                          self.output_dir,
                          constants.MP3_EXT,
                          self.video_format,
                          self.image)

        downloader = Downloader(request.chunk_size)
        converter = Converter()
        feed_searcher = FeedSearcher()
        feed_provider = FeedProvider(feed_searcher, request.rss_url)
        episode_processor = EpisodeProcessor(converter, downloader)
        self.loading_popup = LoadingPopup(image=request.image, title=request.rss_url)
        self.loading_popup.open()
        progress_updater = ProgressUpdater(self.loading_popup.update_progress)
        request_processor = RequestProcessor(feed_provider, episode_processor, progress_updater)
        background_thread = threading.Thread(target=self.handle_background_thread,
                                             args=tuple([request_processor, request]))
        background_thread.start()

    @mainthread
    def dismiss_popup(self):
        self.loading_popup.close()

    def handle_background_thread(self, request_processor: RequestProcessor, request: Request):
        request_processor.process(request)
        self.dismiss_popup()
