import os

class OsuFileFormatParser:
    def __init__(self, osu_file_path):
        self.osu_file_path: str = osu_file_path
        self.data: dict = {}

        self.parse()

    def parse(self):
        with open(self.osu_file_path, 'r', encoding='utf-8') as f:
            file_content = f.readlines()

        data = {}
        current_section = None
        
        for line in file_content:
            line = line.strip()
            
            if not line:
                continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1] 
                if current_section in ['TimingPoints', 'HitObjects', 'Events']:
                    data[current_section] = []
                else:
                    data[current_section] = {}
                continue
            
            if current_section:
                if current_section in ['TimingPoints', 'HitObjects']:
                    data[current_section].append(line)
                elif current_section in ['Events'] and line[0:2] != "//":
                    data[current_section].append(line)
                else:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data[current_section][key.strip()] = value.strip()
        
        self.data = data
    
    def get_slider_multiplier(self) -> float:
        return float(self.data["Difficulty"]["SliderMultiplier"])

    def get_song_file_path(self) -> str:
        song_filename = self.data["General"]["AudioFilename"]
        path = os.path.normpath(f"{self.osu_file_path}/../{song_filename}")

        return path
    
    def get_timing_points(self) -> list[str]:
        return self.data["TimingPoints"]
    
    def get_hit_objects(self) -> list[str]:
        return self.data["HitObjects"]
    
    def get_bg_path(self) -> str:
        bg_filename = self.data["Events"][0].split("\"")[1]
        path = os.path.normpath(f"{self.osu_file_path}/../{bg_filename}")

        return path
    
    def get_full_data(self) -> dict:
        return self.data
    
    def get_metadata(self) -> dict:
        return self.data["Metadata"]