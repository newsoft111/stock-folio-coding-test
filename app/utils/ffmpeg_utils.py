import subprocess
import json
from typing import Dict, List

def run_ffmpeg_command(command: List[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg command failed: {e.stderr}")

def get_video_info(file_path: str) -> Dict:
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ]
    
    output = run_ffmpeg_command(command)
    info = json.loads(output)
    
    video_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'video'), None)
    
    return {
        'duration': float(info['format']['duration']),
        'format': info['format']['format_name'],
        'width': int(video_stream['width']) if video_stream else None,
        'height': int(video_stream['height']) if video_stream else None,
    }

def create_trim_command(input_path: str, output_path: str, start_time: float, end_time: float) -> List[str]:
    return [
        'ffmpeg',
        '-i', input_path,
        '-ss', str(start_time),
        '-to', str(end_time),
        '-c', 'copy',
        output_path
    ]

def create_concat_command(input_paths: List[str], output_path: str) -> List[str]:
    input_args = []
    for path in input_paths:
        input_args.extend(['-i', path])
    
    filter_complex = f"concat=n={len(input_paths)}:v=1:a=1 [outv] [outa]"
    
    return [
        'ffmpeg',
        *input_args,
        '-filter_complex', filter_complex,
        '-map', '[outv]',
        '-map', '[outa]',
        output_path
    ]