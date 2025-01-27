def convert_osu_time_to_ms(osu_time) -> int:
    minutes, seconds, milliseconds = osu_time.split(':')

    return (int(minutes) * 60 * 1000) + (int(seconds) * 1000) + int(milliseconds)