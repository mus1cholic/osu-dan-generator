import bisect
import copy

from functools import cmp_to_key

from utils.constants import NOTE_SHIFT_RESISTANCE

class OsuFileGenerator:
    def __init__(self, diff_name, set_title, set_id, circle_size, approach_rate, overall_difficulty, hp):
        self.diff_name = diff_name
        self.set_title = set_title
        self.set_id = set_id

        self.file_contents_json = {
            "General": {
                "AudioFilename": f"{diff_name}.mp3",
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
                "Title": self.set_title,
                "TitleUnicode": self.set_title,
                "Artist": "Various Artists",
                "ArtistUnicode": "Various Artists",
                "Creator": "lolol234",
                "Version": diff_name,
                "Source": "",
                "Tags": "Osu Standard Dan",
                "BeatmapID": "-1",
                "BeatmapSetID": self.set_id
            },
            "Difficulty": {
                "HPDrainRate": hp,
                "CircleSize": circle_size,
                "OverallDifficulty": overall_difficulty,
                "ApproachRate": approach_rate,
                "SliderMultiplier": "2.0",
                "SliderTickRate": "1"
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
        fade_in_duration = start_time - fade_in_start_time
        
        # uninherited is red line, inherited is green line
        uninherited_timings_points_arr: list[str] = []
        inherited_timings_points_arr: list[str] = []

        for time in timing_points_arr:
            time_split = time.split(",")

            if int(time_split[6]) == 1:
                uninherited_timings_points_arr.append(time)
            else:
                inherited_timings_points_arr.append(time)

        # this weird and complicated logic has to be done because the osu editor occasionally moves
        # objects and timings by a few ms each. that's why AImod also exists. very annoying workaround,
        # but must be done

        uninherited_timings = [int(float(time.split(",")[0])) for time in uninherited_timings_points_arr]
        uninherited_timings_possible_start_right_index = bisect.bisect_right(uninherited_timings, start_time)
        uninherited_timings_possible_start_left_index = uninherited_timings_possible_start_right_index - 1

        if uninherited_timings_possible_start_right_index == len(uninherited_timings):
            uninherited_timings_possible_start_right_index -= 1
        elif uninherited_timings_possible_start_left_index < 0:
            uninherited_timings_possible_start_left_index += 1

        if abs(uninherited_timings[uninherited_timings_possible_start_left_index] - start_time) \
            < abs(uninherited_timings[uninherited_timings_possible_start_right_index] - start_time) \
            or uninherited_timings[uninherited_timings_possible_start_right_index] > start_time + NOTE_SHIFT_RESISTANCE:
            uninherited_timings_range_start_index = uninherited_timings_possible_start_left_index
        else:
            uninherited_timings_range_start_index = uninherited_timings_possible_start_right_index

        uninherited_timings_possible_end_right_index = bisect.bisect_right(uninherited_timings, end_time)
        uninherited_timings_possible_end_left_index = uninherited_timings_possible_end_right_index - 1

        if uninherited_timings_possible_end_right_index == len(uninherited_timings):
            uninherited_timings_possible_end_right_index -= 1
        elif uninherited_timings_possible_end_left_index < 0:
            uninherited_timings_possible_end_left_index += 1

        if abs(uninherited_timings[uninherited_timings_possible_end_left_index] - end_time) \
            < abs(uninherited_timings[uninherited_timings_possible_end_right_index] - end_time) \
            or uninherited_timings[uninherited_timings_possible_end_right_index] > end_time + NOTE_SHIFT_RESISTANCE:
            uninherited_timings_range_end_index = uninherited_timings_possible_end_left_index
        else:
            uninherited_timings_range_end_index = uninherited_timings_possible_end_right_index


        inherited_timings = [int(float(time.split(",")[0])) for time in inherited_timings_points_arr]
        inherited_timings_possible_start_right_index = bisect.bisect_right(inherited_timings, start_time)
        inherited_timings_possible_start_left_index = inherited_timings_possible_start_right_index - 1

        if inherited_timings_possible_start_right_index == len(inherited_timings):
            inherited_timings_possible_start_right_index -= 1
        elif inherited_timings_possible_start_left_index < 0:
            inherited_timings_possible_start_left_index += 1

        if abs(inherited_timings[inherited_timings_possible_start_left_index] - start_time) \
            < abs(inherited_timings[inherited_timings_possible_start_right_index] - start_time) \
            or inherited_timings[inherited_timings_possible_start_right_index] > start_time + NOTE_SHIFT_RESISTANCE:
            inherited_timings_range_start_index = inherited_timings_possible_start_left_index
        else:
            inherited_timings_range_start_index = inherited_timings_possible_start_right_index\
            
        inherited_timings_possible_end_right_index = bisect.bisect_right(inherited_timings, end_time)
        inherited_timings_possible_end_left_index = inherited_timings_possible_end_right_index - 1        

        if inherited_timings_possible_end_right_index == len(inherited_timings):
            inherited_timings_possible_end_right_index -= 1
        elif inherited_timings_possible_end_left_index < 0:
            inherited_timings_possible_end_left_index += 1

        if abs(inherited_timings[inherited_timings_possible_end_left_index] - end_time) \
            < abs(inherited_timings[inherited_timings_possible_end_right_index] - end_time) \
            or inherited_timings[inherited_timings_possible_end_right_index] > end_time + NOTE_SHIFT_RESISTANCE:
            inherited_timings_range_end_index = inherited_timings_possible_end_left_index
        else:
            inherited_timings_range_end_index = inherited_timings_possible_end_right_index        

        # if in the original map, there is an instance such that green < red <= start, we remove the green line.
        # otherwise, we move that green line to the time of the first note
        if inherited_timings[inherited_timings_range_start_index] < uninherited_timings[uninherited_timings_range_start_index] \
            and uninherited_timings[uninherited_timings_range_start_index] <= start_time:
            inherited_timings_range_start_index += 1

        timings: list[str] = []
        
        for i in range(uninherited_timings_range_start_index, uninherited_timings_range_end_index + 1):
            cur = uninherited_timings_points_arr[i].split(",")
            cur_time = int(float(cur[0]))

            if i == uninherited_timings_range_start_index and cur_time < start_time:
                cur_time = offset + fade_in_duration
            else:
                cur_time = (offset + fade_in_duration) + (cur_time - start_time)

            cur[0] = str(cur_time)
            timings.append(",".join(cur))

        for i in range(inherited_timings_range_start_index, inherited_timings_range_end_index + 1):
            cur = inherited_timings_points_arr[i].split(",")
            cur_time = int(float(cur[0]))

            if i == inherited_timings_range_start_index and cur_time < start_time:
                cur_time = offset + fade_in_duration
            else:
                cur_time = (offset + fade_in_duration) + (cur_time - start_time)

            cur[0] = str(cur_time)
            timings.append(",".join(cur))

        def custom_cmp(timing1: str, timing2: str):
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

        for i, timing in enumerate(timings):
            cur_timing_point = timing.split(",")
            if int(cur_timing_point[6]) == 0:
                # apply adjusted slider multiplier
                cur_timing_point[1] = str(float(cur_timing_point[1]) * (1.0 / slider_velocity_adjust))
            elif i < len(timings) - 1:
                # add a green line at the timestamp of any red line that adjusts to slider velocity
                # except if there is already a green line at the same timestamp
                next_timing = timings[i + 1].split(",")

                if int(next_timing[6]) != 0 or int(next_timing[0]) != int(cur_timing_point[0]):
                    insert_new_timing = copy.deepcopy(cur_timing_point)
                    insert_new_timing[1] = str(float("-100") * (1.0 / slider_velocity_adjust))
                    insert_new_timing[6] = "0"

                    insert_new_timing = ",".join(insert_new_timing)
                    self.file_contents_json["TimingPoints"].append(insert_new_timing)

            cur_timing_point = ",".join(cur_timing_point)
            self.file_contents_json["TimingPoints"].append(cur_timing_point)

        # unkiai the final timing point to make sure there is no kiai during breaks
        last_timing_point = self.file_contents_json["TimingPoints"][-1].split(",")
        last_timing_point[7] = str(int(last_timing_point[7]) & 1110)

        last_timing_point = ",".join(last_timing_point)
        self.file_contents_json["TimingPoints"][-1] = last_timing_point

    def add_hit_objects(self, hit_objects_arr: list[str], start_time: int, end_time: int, fade_in_start_time: int, offset: int):
        fade_in_duration = start_time - fade_in_start_time
        
        hitobjects = [int(hitobject.split(",")[2]) for hitobject in hit_objects_arr]
        hitobjects_possible_start_right_index = bisect.bisect_right(hitobjects, start_time)
        hitobjects_possible_start_left_index = hitobjects_possible_start_right_index - 1

        if hitobjects_possible_start_right_index == len(hitobjects):
            hitobjects_possible_start_right_index -= 1
        elif hitobjects_possible_start_left_index < 0:
            hitobjects_possible_start_left_index += 1

        if abs(hitobjects[hitobjects_possible_start_left_index] - start_time) \
            < abs(hitobjects[hitobjects_possible_start_right_index] - start_time):
            hitobjects_range_start_index = hitobjects_possible_start_left_index
        else:
            hitobjects_range_start_index = hitobjects_possible_start_right_index

        hitobjects_possible_end_right_index = bisect.bisect_right(hitobjects, end_time)
        hitobjects_possible_end_left_index = hitobjects_possible_end_right_index - 1

        if hitobjects_possible_end_right_index == len(hitobjects):
            hitobjects_possible_end_right_index -= 1
        elif hitobjects_possible_end_left_index < 0:
            hitobjects_possible_end_left_index += 1

        if abs(hitobjects[hitobjects_possible_end_left_index] - end_time) \
            < abs(hitobjects[hitobjects_possible_end_right_index] - end_time) \
            or hitobjects[hitobjects_possible_end_right_index] > end_time + NOTE_SHIFT_RESISTANCE:
            hitobjects_range_end_index = hitobjects_possible_end_left_index
        else:
            hitobjects_range_end_index = hitobjects_possible_end_right_index

        for i in range(hitobjects_range_start_index, hitobjects_range_end_index + 1):
            cur_hitobject_split = hit_objects_arr[i].split(",")
            if int(cur_hitobject_split[3]) & (1 << 3):
                # spinner object
                spinner_duration = int(cur_hitobject_split[5]) - int(cur_hitobject_split[2])

                cur_hitobject_split[2] = str((offset + fade_in_duration) + (int(cur_hitobject_split[2]) - start_time))
                cur_hitobject_split[5] = str(int(cur_hitobject_split[2]) + spinner_duration)
            else:
                # slider or hitcircle object
                cur_hitobject_split[2] = str((offset + fade_in_duration) + (int(cur_hitobject_split[2]) - start_time))

                # make sure every new map starts with a new combo
                if i == hitobjects_range_start_index:
                    cur_hitobject_split[3] = str(int(cur_hitobject_split[3]) | (1 << 2))

            cur_hitobject = ",".join(cur_hitobject_split)
            self.file_contents_json["HitObjects"].append(cur_hitobject)

    def get_timing_point_length(self):
        return len(self.file_contents_json["TimingPoints"])

    def get_bpm(self, timing_point_idx):
        timing_point = self.file_contents_json["TimingPoints"][timing_point_idx]
        fields = timing_point.split(',')
        bpm = round(60000 / float(fields[1]))
        return bpm
        
    def add_sb_events(self, fade_in_start_time: int, true_start_time: int, fade_out_end_time: int, true_end_time: int, cur_offset: int, idx: int, scaling_factor: float):
        real_offset = cur_offset - fade_in_start_time
        
        events = self.file_contents_json["Events"]
        events.append(f"Sprite,Foreground,Centre,\"sb_{self.diff_name}\\BG{idx + 1}.jpg\",320,240")
        events.append(f" S,0,{fade_in_start_time + real_offset},,{round(scaling_factor, 5)}")
        events.append(f" F,0,{fade_in_start_time + real_offset},{true_start_time + real_offset},0,1")
        events.append(f" F,0,{true_end_time + real_offset},{fade_out_end_time + real_offset},1,0")

    def export(self):
        with open(f"generated/{self.set_title}/{self.diff_name}.osu", 'w', encoding='utf-8') as osu_file:
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