import json
import os
import shutil

from classes.BackgroundGenerator import BackgroundGenerator
from classes.OsuFileFormatParser import OsuFileFormatParser
from classes.OsuFileGenerator import OsuFileGenerator
from classes.SongStitcher import SongStitcher

def create_dan(mapset):
    diff_name = mapset["diff_name"]
    symbol = mapset["symbol"]
    circle_size = mapset["circle_size"]
    approach_rate = mapset["approach_rate"]
    overall_difficulty = mapset["overall_difficulty"]
    hp = mapset["hp"]
    beatmaps = mapset["beatmaps"]

    background_generator = BackgroundGenerator(diff_name, symbol, beatmaps)
    song_stitcher = SongStitcher(diff_name)
    osu_file_generator = OsuFileGenerator(diff_name, circle_size, approach_rate, overall_difficulty, hp)

    for map in beatmaps:
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
        slider_multiplier = file_parser.get_slider_multiplier()

        true_start_time = song_stitcher.get_true_start_time()
        fade_in_start_time = song_stitcher.get_fade_in_start_time()
        true_end_time = song_stitcher.get_true_end_time()
        fade_out_end_time = song_stitcher.get_fade_out_end_time
        cur_offset = song_stitcher.get_offset()

        osu_file_generator.add_timing_points(timing_points, slider_multiplier, true_start_time, true_end_time, fade_in_start_time, cur_offset)
        osu_file_generator.add_hit_objects(hit_objects, true_start_time, true_end_time, fade_in_start_time, cur_offset)

        # add backgrounds
        bg_filepath = file_parser.get_bg_path()
        background_generator.add_background(bg_filepath)

    background_generator.generate()
    song_stitcher.export()
    osu_file_generator.export()

def create_dan_set(mapset_info):
    if os.path.exists("testdan"):
        shutil.rmtree("testdan")
    os.makedirs("testdan")

    for mapset in mapset_info:
        create_dan(mapset)
        
def main():
    with open("mapset_info.json", encoding='utf-8') as f:
        mapset_info = json.load(f)

    create_dan_set(mapset_info)

if __name__ == "__main__":
    main()