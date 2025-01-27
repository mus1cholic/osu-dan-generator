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
                if current_section in ['TimingPoints', 'HitObjects']:
                    data[current_section] = []
                else:
                    data[current_section] = {}
                continue
            
            if current_section:
                if current_section in ['TimingPoints', 'HitObjects']:
                    data[current_section].append(line)
                else:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data[current_section][key.strip()] = value.strip()
        
        self.data = data

    def get_song_file_path(self) -> str:
        song_filename = self.data["General"]["AudioFilename"]

        return f"{self.osu_file_path}/../{song_filename}"