from pydub import AudioSegment

from utils.utils import convert_osu_time_to_ms

class SongStitcher:
    
    def __init__(self):
        self.combined_audio = AudioSegment.silent(duration=0)

    def stitch(self, song_path, start_time, end_time):
        audio = AudioSegment.from_file(song_path)
        start_time = convert_osu_time_to_ms(start_time)
        end_time = convert_osu_time_to_ms(end_time)

        segment = audio[start_time:end_time]

        self.combined_audio = self.combined_audio + segment

    def export(self):
        self.combined_audio.export("final.mp3", format="mp3")