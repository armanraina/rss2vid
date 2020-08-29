import ffmpeg
from src.util import data_path, get_log_level
from src.model.conversion_exception import ConversionException


def to_video(image_file, audio_file, out_dir, description, loop: int = 1, frame_rate: int = 1):
    try:
        audio = ffmpeg.input(audio_file)

        image = ffmpeg.input(
            image_file,
            loop=loop,
            framerate=frame_rate
        ).filter("pad", **{
            'width': 'ceil(iw / 2) * 2',
            'height': 'ceil(ih / 2) * 2'
        })
        ffmpeg.output(
            audio,
            image,
            out_dir,
            shortest=None,
            tune='stillimage',
            crf=18,
            **{'c:a': 'copy',
               'c:v': 'libx264',
               'metadata': f'description="{description}"'
               }).overwrite_output().global_args(
            '-report',
            '-loglevel',
            str(get_log_level())).run(cmd=data_path('ffmpeg.exe'))
    except ffmpeg.Error as e:
        raise ConversionException(str(e))


