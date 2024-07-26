import cv2
import json
import os


def convert_mp4_to_avi(input_path, output_path):
    # Open the MP4 video file
    video_capture = cv2.VideoCapture(input_path)
    
    # Check if the video file opened successfully
    if not video_capture.isOpened():
        print(f"Error opening video file: {input_path}")
        return
    
    # Get the properties of the input video
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create VideoWriter object for the AVI file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    # Read and write frames
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        video_writer.write(frame)
    
    # Release the video capture and writer objects
    video_capture.release()
    video_writer.release()
    print(f"Conversion complete: {output_path}")


def convert_mp4_to_avi_folder(input_folder, output_folder):
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        # Process only MP4 files
        if filename.endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".avi"
            output_path = os.path.join(output_folder, output_filename)
            
            # Convert the MP4 to AVI
            convert_mp4_to_avi(input_path, output_path)

def data_split(json_files, link_paths, dada_path):

    for json_file, link_path in zip(json_files, link_paths):
        with open(json_file, 'r') as f:
            train_f = json.load(f)
            for file in train_f:
                save_p = os.path.join(link_path, file[1])
                src = os.path.join(dada_path, file[0][0], file[0][1])
                os.symlink(src, save_p, target_is_directory=True)

input_folder = "/home/achini/Documents/Crash_videos"
output_folder = "/home/achini/Documents/Crash_videos_converted"
link_paths = ["/home/achini/Documents/test_car_crash"]
json_files = ["/home/achini/Documents/test_file.json"]

# convert_mp4_to_avi_folder(input_folder, output_folder)
# data_split(json_files, link_paths, output_folder)