import json
import os
import shutil

from classes.OsuFileFormatParser import OsuFileFormatParser
from classes.OsuFileGenerator import OsuFileGenerator
from classes.SongStitcher import SongStitcher

def create_dan(maps_info):
    song_stitcher = SongStitcher()
    osu_file_generator = OsuFileGenerator()

    for map in maps_info:
        osu_file_path = map["osu_file_path"]
        start_time_unformatted = map["start_time"]
        end_time_unformatted = map["end_time"]

        file_parser = OsuFileFormatParser(osu_file_path)
        
        # stitch songs
        audio_file_path = file_parser.get_song_file_path()
        song_stitcher.stitch(audio_file_path, start_time_unformatted, end_time_unformatted)

        # add timing points and hit objects
        timing_points = file_parser.get_timing_points()
        hit_objects = file_parser.get_hit_objects()

        true_start_time = song_stitcher.get_true_start_time()
        fade_in_start_time = song_stitcher.get_fade_in_start_time()
        true_end_time = song_stitcher.get_true_end_time()
        fade_out_end_time = song_stitcher.get_fade_out_end_time
        cur_offset = song_stitcher.get_offset()

        osu_file_generator.add_timing_points(timing_points, true_start_time, true_end_time, fade_in_start_time, cur_offset)
        osu_file_generator.add_hit_objects(hit_objects, true_start_time, true_end_time, fade_in_start_time, cur_offset)

    if os.path.exists("testdan"):
        shutil.rmtree("testdan")
        
    os.makedirs("testdan")
    song_stitcher.export()
    osu_file_generator.export()

def main():
    with open("maps_info.json") as f:
        maps_info = json.load(f)

    create_dan(maps_info)

if __name__ == "__main__":
    main()