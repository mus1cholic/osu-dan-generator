import json
import os
import shutil

from classes.BackgroundGenerator import BackgroundGenerator
from classes.OsuFileFormatParser import OsuFileFormatParser
from classes.OsuFileGenerator import OsuFileGenerator
from classes.SongStitcher import SongStitcher

def create_dan(mapset_info_filename, mapset_info_title, mapset_info_setid):
    with open(mapset_info_filename, encoding='utf-8') as f:
        mapset_data = json.load(f)

    if os.path.exists(f"generated/{mapset_info_title}"):
        shutil.rmtree(f"generated/{mapset_info_title}")
    os.makedirs(f"generated/{mapset_info_title}")

    for diff in mapset_data:
        diff_name = diff["diff_name"]
        symbol = diff["symbol"]
        circle_size = diff["circle_size"]
        approach_rate = diff["approach_rate"]
        overall_difficulty = diff["overall_difficulty"]
        hp = diff["hp"]
        beatmaps = diff["beatmaps"]

        background_generator = BackgroundGenerator(diff_name, mapset_info_title, symbol, beatmaps)
        song_stitcher = SongStitcher(diff_name, mapset_info_title)
        osu_file_generator = OsuFileGenerator(diff_name, mapset_info_title, mapset_info_setid, circle_size, approach_rate, overall_difficulty, hp)

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

def create_dan_sets(dan_mapset):
    if os.path.exists("generated"):
        shutil.rmtree("generated")
    os.makedirs("generated")

    for mapset in dan_mapset["mapsets"]:
        mapset_info_filename = mapset["filename"]
        mapset_info_title = mapset["title"]
        mapset_info_setid = mapset["beatmap_set_id"]

        create_dan(mapset_info_filename, mapset_info_title, mapset_info_setid)
        
def main():
    with open("dan_mapset.json", encoding='utf-8') as f:
        dan_mapset = json.load(f)

    create_dan_sets(dan_mapset)

if __name__ == "__main__":
    main()