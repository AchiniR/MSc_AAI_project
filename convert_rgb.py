import cv2
import os

def convert_to_rgb_video(input_path, output_path):
    # Open the input video file
    video_capture = cv2.VideoCapture(input_path)
    
    # Check if the video file opened successfully
    if not video_capture.isOpened():
        print(f"Error opening video file: {input_path}")
        return
    
    # Get the properties of the input video
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create VideoWriter object for the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like 'MJPG', 'MP4V', etc.
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    # Read and convert each frame to RGB
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Convert the frame from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write the RGB frame to the output video
        video_writer.write(rgb_frame)
    
    # Release the video capture and writer objects
    video_capture.release()
    video_writer.release()
    print(f"Conversion to RGB video complete: {output_path}")

def generate_rgb_video_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.avi')):  # Add other video formats if needed
            input_video_path = os.path.join(input_folder, filename)
            output_video_path = os.path.join(output_folder, filename)

            convert_to_rgb(input_video_path, output_video_path)



for i in range(25, 45):
    input_folder = f"/home/achini/Documents/CarCrash/avi_videos/{i}"
    output_folder = f"/home/achini/Documents/CarCrash/training/rgb_videos/{i}"
    generate_rgb_video_folder(input_folder, output_folder)