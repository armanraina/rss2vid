import ffmpeg
from src.util import data_path, get_log_level
from src.infr.conversion_exception import ConversionException
import itertools


def to_video(image_file,
             audio_file,
             out_dir,
             description,
             loop: int = 1,
             frame_rate: int = 1,
             speed: str = 'ultrafast',
             encoding: str = 'libx264',
             quality: int = 23):
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
        output = ffmpeg.output(
            audio,
            image,
            out_dir,
            shortest=None,
            crf=quality,
            preset=speed,
            **{'c:a': 'copy',
               'c:v': encoding,
               'metadata': f'description="{description}"'
               }).overwrite_output().global_args(
            '-report',
            '-loglevel',
            str(get_log_level()))
        output.run(cmd=data_path('ffmpeg.exe'))
    except ffmpeg.Error as e:
        raise ConversionException(str(e))


def to_video_viz(image_file,
                 audio_file,
                 out_dir,
                 description,
                 loop: int = 1,
                 frame_rate: int = 1,
                 speed: str = 'ultrafast',
                 encoding: str = 'libx264',
                 quality: int = 23,
                 size=(1920, 1080)):
    try:
        audio = ffmpeg.input(audio_file)

        viz = audio.filter(
            "showwaves", size=f'{size[0]}x{size[1]}',
            colors='white', mode='line'
            
        )

        image = ffmpeg.input(
            image_file
        ).filter("scale",
                 width=size[0],
                 height=size[1]
        ).overlay(viz)

        output = ffmpeg.output(
            audio,
            image,
            out_dir,
            shortest=None,
            crf=quality,
            preset=speed,
            **{'c:a': 'copy',
               'c:v': encoding,
               'metadata': f'description="{description}"'
               }).overwrite_output().global_args(
            '-report',
            '-loglevel',
            str(get_log_level()))
        output.run(cmd=data_path('ffmpeg.exe'))
    except ffmpeg.Error as e:
        raise ConversionException(str(e))


if __name__ == '__main__':
    import os
    import time
    image_file = data_path(os.path.join('samples', 'mic.jpg'))
    audio_file = data_path(os.path.join('samples', 'life_for_rent.mp3'))
    out_dir = data_path('samples/life_for_rent.mkv')
    description = 'life_for_rent song'
    runs = 1
    encodings = ['libx264']
    speeds = ['ultrafast']
    exts = ['mp4']
    qualities = [23]
    options = itertools.product(range(runs), encodings, speeds, exts, qualities)
    timing = {}
    for run, encoding, speed, ext, quality in options:
        key = f'{encoding}_{speed}_{run}_{quality}_{ext}'
        tic = time.perf_counter()
        out_dir = data_path('samples/life_for_rent_{0}.{1}').format(key, ext)
        to_video_viz(image_file, audio_file, out_dir, description, encoding=encoding, speed=speed, quality=quality)
        toc = time.perf_counter()
        timing[key] = toc-tic
    print(str(timing))
