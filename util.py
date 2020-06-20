import ffmpeg


def create_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def create_video_stream(image_stream, audio_stream, out_stream):
    audio = ffmpeg.input(audio_stream)
    image = ffmpeg.input(image_stream, loop=1, framerate=1)
    out = ffmpeg.output(
        audio, image, out_stream,
        shortest=None, preset='veryslow', crf=0,
        **{'c:a': 'copy', 'c:v': 'libx264'})
    out.run()




