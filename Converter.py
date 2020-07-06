import ffmpeg


class Converter:
    def __init__(self, loop: int = 1, frame_rate: int = 1):
        self.loop = loop
        self.frame_rate = frame_rate

    def to_video(self, image_file, audio_file, out_dir, description):
        print(audio_file)
        print(image_file)
        print(out_dir)

        audio = ffmpeg.input(audio_file)

        image = ffmpeg.input(
            image_file,
            loop=self.loop,
            framerate=self.frame_rate
        ).filter("pad", **{
            'width': 'ceil(iw / 2) * 2',
            'height': 'ceil(ih / 2) * 2'
        })

        ffmpeg.output(
            audio,
            image,
            out_dir,
            shortest=None,
            preset='veryslow',
            crf=18,
            **{'c:a': 'copy',
               'c:v': 'libx264',
               'metadata': f'description="{description}"'
               }).overwrite_output().global_args('-progress', 'pipe:1').run()