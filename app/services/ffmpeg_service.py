import subprocess
import json
from app.core.errors import handle_video_processing_error

class FFmpegService:
    def get_video_info(self, file_path: str) -> dict:
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path],
                capture_output=True,
                text=True
            )
            info = json.loads(result.stdout)
            
            video_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'video'), None)
            
            return {
                'duration': float(info['format']['duration']),
                'format': info['format']['format_name'],
                'width': int(video_stream['width']) if video_stream else None,
                'height': int(video_stream['height']) if video_stream else None,
            }
        except Exception as e:
            handle_video_processing_error(f"Error getting video info: {str(e)}")

    def trim_video(self, input_path: str, output_path: str, start_time: float, end_time: float):
        try:
            subprocess.run([
                'ffmpeg',
                '-ss', str(start_time),
                '-i', input_path,
                '-to', str(end_time - start_time), #이렇게 안하면 음성만 남고 영상이 사라짐 (상대적 시간사용)
                '-c', 'copy',
                output_path
            ], check=True)

            
        except subprocess.CalledProcessError as e:
            handle_video_processing_error(f"Error trimming video: {str(e)}")

    def concat_videos(self, input_paths: list[str], output_path: str):
        try:
            input_args = []
            for path in input_paths:
                input_args.extend(['-i', path])
            
            filter_complex = f"concat=n={len(input_paths)}:v=1:a=1 [outv] [outa]"
            
            command = [
                'ffmpeg',
                *input_args,
                '-filter_complex', filter_complex,
                '-map', '[outv]',
                '-map', '[outa]',
                output_path
            ]
            
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            handle_video_processing_error(f"Error concatenating videos: {str(e)}")