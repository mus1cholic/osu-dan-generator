import bisect

from functools import cmp_to_key

class OsuFileGenerator:
    def __init__(self, diff_name, circle_size, approach_rate, overall_difficulty, hp):
        self.diff_name = diff_name

        self.file_contents_json = {
            "General": {
                "AudioFilename": f"final_{diff_name}.mp3",
                "AudioLeadIn": "0",
                "PreviewTime": "2000",
                "Countdown": "0",
                "SampleSet": "Soft",
                "StackLeniency": "0.7",
                "Mode": "0",
                "LetterboxInBreaks": "0",
                "WidescreenStoryboard": "0"
            },
            "Editor": {
                "Bookmarks": "",
                "DistanceSpacing": "0.8",
                "BeatDivisor": "4",
                "GridSize": "8",
                "TimelineZoom": "1"
            },
            "Metadata": {
                "Title": "Tapping Dan",
                "TitleUnicode": "Tapping Dan",
                "Artist": "Various Artists",
                "ArtistUnicode": "Various Artists",
                "Creator": "lolol234",
                "Version": diff_name,
                "Source": "",
                "Tags": "Osu Standard Dan",
                "BeatmapID": "-1",
                "BeatmapSetID": "-1"
            },
            "Difficulty": {
                "HPDrainRate": hp,
                "CircleSize": circle_size,
                "OverallDifficulty": overall_difficulty,
                "ApproachRate": approach_rate,
                "SliderMultiplier": "2.0",
                "SliderTickRate": "2"
            },
            "Events": [
                f"0,0,\"bg_{diff_name}.png\",0,0"
            ],
            "TimingPoints": [],
            "Colours": {
                "Combo1": "177,100,255",
                "Combo2": "179,179,255",
                "Combo3": "0,210,210",
                "Combo4": "228,228,228"
            },
            "HitObjects": []
        }

    def add_timing_points(self, timing_points_arr: list[str], slider_multiplier: float, start_time: int, end_time: int, fade_in_start_time: int, offset: int):
        fade_in_start_time = start_time - fade_in_start_time
        
        uninherited_timings_points_arr = []
        inherited_timings_points_arr = []

        # TODO: slight bug, there is a red line that is added 05:29:686 that corresponds to lugal en ki, but i dont need it

        for time in timing_points_arr:
            time_split = time.split(",")

            if int(time_split[6]) == 1:
                uninherited_timings_points_arr.append(time)
            else:
                inherited_timings_points_arr.append(time)

        uninherited_timings = [int(time.split(",")[0]) for time in uninherited_timings_points_arr]
        uninherited_timings_range_start_index = bisect.bisect_right(uninherited_timings, start_time) - 1
        uninherited_timings_range_end_index = bisect.bisect_right(uninherited_timings, end_time) - 1

        if uninherited_timings_range_start_index == -1:
            uninherited_timings_range_start_index = 0
        if uninherited_timings_range_end_index == -1:
            uninherited_timings_range_end_index = 0

        inherited_timings = [int(time.split(",")[0]) for time in inherited_timings_points_arr]
        inherited_timings_range_start_index = bisect.bisect_right(inherited_timings, start_time) - 1
        inherited_timings_range_end_index = bisect.bisect_right(inherited_timings, end_time) - 1

        if inherited_timings_range_start_index == -1:
            inherited_timings_range_start_index = 0
        if inherited_timings_range_end_index == -1:
            inherited_timings_range_end_index = 0

        timings = []
        for i in range(uninherited_timings_range_start_index, uninherited_timings_range_end_index + 1):
            cur = uninherited_timings_points_arr[i].split(",")
            cur_time = int(cur[0])

            if i == uninherited_timings_range_start_index and int(cur[0]) < start_time:
                cur_time = offset + fade_in_start_time
            else:
                cur_time = (offset + fade_in_start_time) + (cur_time - start_time)

            cur[0] = str(cur_time)
            timings.append(",".join(cur))
        for i in range(inherited_timings_range_start_index, inherited_timings_range_end_index + 1):
            cur = inherited_timings_points_arr[i].split(",")
            cur_time = int(cur[0])

            if i == inherited_timings_range_start_index and int(cur[0]) < start_time:
                cur_time = offset + fade_in_start_time
            else:
                cur_time = (offset + fade_in_start_time) + (cur_time - start_time)

            cur[0] = str(cur_time)
            timings.append(",".join(cur))

        def custom_cmp(timing1, timing2):
            # put red lines before green lines
            timing1_split = timing1.split(",")
            timing2_split = timing2.split(",")

            if int(timing1_split[0]) < int(timing2_split[0]):
                return -1
            elif int(timing1_split[0]) > int(timing2_split[0]):
                return 1
            else:
                return -1 if int(timing1_split[6]) == 1 else 1

        timings.sort(key=cmp_to_key(custom_cmp))

        slider_velocity_adjust = slider_multiplier / 2.0

        for timing in timings:
            cur_timing_point_split = timing.split(",")
            if int(cur_timing_point_split[6]) != 1:
                # apply adjusted slider multiplier
                cur_timing_point_split[1] = str(float(cur_timing_point_split[1]) * (1.0 / slider_velocity_adjust))
            cur_timing_point = ",".join(cur_timing_point_split)

            self.file_contents_json["TimingPoints"].append(cur_timing_point)

    def add_hit_objects(self, hit_objects_arr: list[str], start_time: int, end_time: int, fade_in_start_time: int, offset: int):
        fade_in_start_time = start_time - fade_in_start_time
        
        hitobjects = [int(hitobject.split(",")[2]) for hitobject in hit_objects_arr]

        hitobjects_range_start_index = bisect.bisect_left(hitobjects, start_time)
        hitobjects_range_end_index = bisect.bisect_left(hitobjects, end_time)

        if hitobjects_range_start_index == -1:
            hitobjects_range_start_index = 0
        if hitobjects_range_end_index == len(hitobjects):
            hitobjects_range_end_index -= 1

        for i in range(hitobjects_range_start_index, hitobjects_range_end_index + 1):
            cur_hitobject_split = hit_objects_arr[i].split(",")
            if int(cur_hitobject_split[3]) & (1 << 3):
                # spinner object
                spinner_duration = int(cur_hitobject_split[5]) - int(cur_hitobject_split[2])

                # cur_hitobject_split[2] = str(int(cur_hitobject_split[2]) + offset - test + fade_in_start_time)
                cur_hitobject_split[2] = str((offset + fade_in_start_time) + (int(cur_hitobject_split[2]) - start_time))
                cur_hitobject_split[5] = str(int(cur_hitobject_split[2]) + spinner_duration)
            else:
                # slider or hitcircle object
                # cur_hitobject_split[2] = str(int(cur_hitobject_split[2]) + offset - test + fade_in_start_time)
                cur_hitobject_split[2] = str((offset + fade_in_start_time) + (int(cur_hitobject_split[2]) - start_time))

            cur_hitobject = ",".join(cur_hitobject_split)

            self.file_contents_json["HitObjects"].append(cur_hitobject)

    def export(self):
        with open(f"testdan/final_{self.diff_name}.osu", 'w', encoding='utf-8') as osu_file:
            osu_file.write('osu file format v14\n\n')

            for section, content in self.file_contents_json.items():
                osu_file.write(f'[{section}]\n')
                
                if isinstance(content, dict):
                    for key, value in content.items():
                        osu_file.write(f'{key}: {value}\n')
                elif isinstance(content, list):
                    for line in content:
                        osu_file.write(f'{line}\n')
                
                osu_file.write('\n')