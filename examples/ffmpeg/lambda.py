import os
import sys
import stat
import ffmpeg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

image_name = "watermark.png"
video_name = "hi_chitanda_eru.mp4"
local_path = "./"


# https://github.com/kkroening/ffmpeg-python
def to_video(duration):
    output = 'processed_hi_chitanda_eru.mp4'
    
    # Load input video and image
    input_video = ffmpeg.input(local_path + video_name, loglevel='quiet')
    input_image = ffmpeg.input(local_path + image_name, loglevel='quiet')
    
    # Apply the same filter chain as in the original command
    trimmed_video_0 = input_video.trim(start_frame=0, end_frame=50).setpts('PTS-STARTPTS')
    trimmed_video_1 = input_video.trim(start_frame=100, end_frame=150).setpts('PTS-STARTPTS')
    
    concatenated_video = ffmpeg.concat(trimmed_video_0, trimmed_video_1, v=1, a=0)
    
    flipped_image = input_image.hflip()
    
    overlaid_video = ffmpeg.overlay(concatenated_video, flipped_image, eof_action='repeat')
    
    final_video = overlaid_video.drawbox(50, 50, 120, 120, color='red', thickness=5)
    
    # Output the processed video
    print(ffmpeg.output(final_video, local_path + output, t=duration).run(overwrite_output=True))

    return "Video {} finished!".format(output)

def handler(event, context=None):
    duration = event.get("duration", 5)


    # Process media
    result = to_video(duration)

    return {
        "result": result
    }

if __name__ == "__main__":
    event = {
        "duration": 10
    }

    print(handler(event))