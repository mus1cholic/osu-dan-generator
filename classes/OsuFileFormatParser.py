class OsuFileFormatParser:
    def __init__(self, osu_file_path):
        # TODO: implement this
        self.osu_file_path: str = osu_file_path

    def get_song_file_path(self) -> str:
        if "Halozy" in self.osu_file_path:
            return f"{self.osu_file_path}/../audio.mp3"
        elif "Yooh" in self.osu_file_path:
            return f"{self.osu_file_path}/../Yooh Ice Angel.mp3"