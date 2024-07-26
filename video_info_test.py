import os
import cv2

def get_video_frame_count(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count

def generate_video_info(input_folder, output_file):
    with open(output_file, 'w') as f:
        for subfolder in sorted(os.listdir(input_folder)):
            subfolder_path = os.path.join(input_folder, subfolder)
            if os.path.isdir(subfolder_path):
                for video_file in sorted(os.listdir(subfolder_path)):
                    if video_file.lower().endswith('.avi'):
                        video_path = os.path.join(subfolder_path, video_file)
                        frame_count = get_video_frame_count(video_path)
                        if frame_count > 0:
                            start_frame = 0
                            end_frame = frame_count - 1
                            f.write(f"{subfolder}/{video_file.split('.')[0]} {start_frame} {end_frame}\n")


input_folder = "/home/achini/Documents/CarCrash/testing/rgb_videos"
output_file = "video_info.txt"
generate_video_info(input_folder, output_file)