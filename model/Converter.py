import ffmpeg
from util import data_path, log_filename


class Converter:
    def __init__(self, loop: int = 1, frame_rate: int = 1, log: bool = False):
        self.loop = loop
        self.frame_rate = frame_rate
        self.log = log

    def to_video(self, image_file, audio_file, out_dir, description):

        audio = ffmpeg.input(audio_file)

        image = ffmpeg.input(
            image_file,
            loop=self.loop,
            framerate=self.frame_rate
        ).filter("pad", **{
            'width': 'ceil(iw / 2) * 2',
            'height': 'ceil(ih / 2) * 2'
        })

        output = ffmpeg.output(
            audio,
            image,
            out_dir,
            shortest=None,
            tune='stillimage',
            crf=18,
            **{'c:a': 'copy',
               'c:v': 'libx264',
               'metadata': f'description="{description}"'
               }).overwrite_output()
        if self.log:
            output.global_args('-report').run(cmd=data_path('ffmpeg.exe'))
        else:
            output.run(cmd=data_path('ffmpeg.exe'))
