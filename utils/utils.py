def convert_osu_time_to_ms(osu_time: str) -> int:
    minutes, seconds, milliseconds = osu_time.split(':')

    return (int(minutes) * 60 * 1000) + (int(seconds) * 1000) + int(milliseconds)

def convert_ms_to_osu_time(milliseconds: int) -> int:
    minutes = milliseconds // 60000
    seconds = (milliseconds % 60000) // 1000
    remaining_milliseconds = milliseconds % 1000
    
    return f"{minutes:02}:{seconds:02}:{remaining_milliseconds:03}"