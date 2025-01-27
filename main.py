import json

from classes.OsuFileFormatParser import OsuFileFormatParser
from classes.SongStitcher import SongStitcher

def stitch_maps(maps_info):
    song_stitcher = SongStitcher()

    for map in maps_info:
        osu_file_path = map["osu_file_path"]
        start_time = map["start_time"]
        end_time = map["end_time"]

        file_parser = OsuFileFormatParser(osu_file_path)
        
        audio_file_path = file_parser.get_song_file_path()

        song_stitcher.stitch(audio_file_path, start_time, end_time)

    song_stitcher.export()

def main():
    with open("maps_info.json") as f:
        maps_info = json.load(f)

    stitch_maps(maps_info)

if __name__ == "__main__":
    main()