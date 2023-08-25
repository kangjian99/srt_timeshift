import re

def shift_time(time_str, delay_milliseconds):
    hours, minutes, secs, msecs = map(int, re.split('[:,]', time_str))
    
    total_seconds = hours * 3600 + minutes * 60 + secs
    total_msecs = msecs + delay_milliseconds
    
    # rounding or debiting operation is required if the number of milliseconds exceeds 1000 or is less than 0
    secs_from_msecs, total_msecs = divmod(total_msecs, 1000)
    total_seconds += secs_from_msecs
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    return f"{hours:02}:{minutes:02}:{secs:02},{total_msecs:03}"

def adjust_srt_timing(srt_content, delay_milliseconds):
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
    
    def replacer(match):
        return f"{shift_time(match.group(1), delay_milliseconds)} --> {shift_time(match.group(2), delay_milliseconds)}"
    
    return pattern.sub(replacer, srt_content)

def adjust_srt_file(filename, delay_milliseconds, output_filename):
    with open(filename, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    adjusted_content = adjust_srt_timing(srt_content, delay_milliseconds)
    
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(adjusted_content)

# main
filename = 'path_to_your_srt_file.srt' # change to your own srt file
delay_milliseconds = 5500  # how many milliseconds shift is required，like delay 5500ms, minus is ok
output_filename = 'adjusted_subtitle.srt' # output file
adjust_srt_file(filename, delay_milliseconds, output_filename)
