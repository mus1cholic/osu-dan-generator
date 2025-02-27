import re
from PIL import Image, ImageDraw, ImageFont

class BackgroundGenerator:
    def __init__(self, diff_name, set_title, symbol, beatmaps):
        self.diff_name = diff_name
        self.set_title = set_title
        self.symbol = symbol
        self.beatmaps = beatmaps

        self.bg_files = []

    def add_background(self, bg_path):
        self.bg_files.append(bg_path)

    def stitch_symbol(self, combined_bgs, total_width, max_height):
        draw = ImageDraw.Draw(combined_bgs)

        font_size = int(total_width * 0.35)
        font = ImageFont.truetype("res/fonts/DejaVuSans.ttf", font_size)
        
        symbol_bbox = draw.textbbox((0, 0), self.symbol, font=font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        symbol_x = (total_width - symbol_width) // 2
        symbol_y = (max_height - symbol_height) // 2

        draw.text((symbol_x, symbol_y), self.symbol, fill="brown", font=font)

    def generate(self):
        bgs: list[Image.Image] = []
        cropped_bgs: list[Image.Image] = []

        for path in self.bg_files:
            bg = Image.open(path)
            bgs.append(bg)

        num_bgs = len(bgs)

        final_width = 1920 // num_bgs
        final_height = 1080

        for bg in bgs:
            width, height = bg.width, bg.height
            strip_width = width * 0.25
            left = (width - strip_width) // 2
            right = left + strip_width
            
            crop_box = (int(left), 0, int(right), height)
            cropped = bg.crop(crop_box)

            resized_strip = cropped.resize((final_width, final_height), Image.Resampling.LANCZOS)
            cropped_bgs.append(resized_strip)

        stitched_width = 1920
        stitched_height = 1080

        combined_bgs = Image.new("RGB", (stitched_width, stitched_height))

        x_offset = 0
        for cropped_bg in cropped_bgs:
            combined_bgs.paste(cropped_bg, (x_offset, 0))
            x_offset += cropped_bg.width

        self.stitch_symbol(combined_bgs, stitched_width, stitched_height)

        combined_bgs.save(f"generated/{self.set_title}/bg_{self.diff_name}.png")
        
    def stitch_metadata(self, bg_filepath, metadata, bpm, idx):
        bg = Image.open(bg_filepath)
        
        new_bg = Image.new("RGB", (bg.width, bg.height))
        new_bg.paste(bg, (0, 0))
        
        if bg.height < 720:
            new_width = bg.width * 720 // bg.height
            new_height = 720
            new_bg = new_bg.resize(size=(new_width, new_height), resample=Image.Resampling.LANCZOS)
        else:
            new_width = bg.width
            new_height = bg.height
        
        draw = ImageDraw.Draw(new_bg)
        version = metadata['Version']
        match = re.match(r'(.*\d+x) \(\d+bpm\)', version)
        if match:
            version = match.group(1)
        text = f"{metadata['Artist']} - {metadata['Title']}\n({metadata['Creator']}) [{version}]\n{bpm} BPM"

        font_size = int(new_height * 0.04)
        font = ImageFont.truetype("res/fonts/DejaVuSans.ttf", font_size)
        
        symbol_bbox = draw.multiline_textbbox((new_width // 2, new_height * 7 // 8), text, align="center", font=font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        symbol_x = (new_width - symbol_width) // 2
        symbol_y = (new_height - symbol_height) * 7 // 8

        draw.multiline_text((symbol_x, symbol_y), text, fill="white", stroke_width=font_size // 8, stroke_fill="black", align="center", font=font)
        
        bg_count = len(self.bg_files)
        
        new_bg.save(f"generated/{self.set_title}/sb_{self.diff_name}/BG{idx + 1}.jpg", quality=90)
        
        return 480 / new_height