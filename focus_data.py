import cv2
import numpy as np
import os

def get_focus_area(frame, prev_frame):
    # Convert frames to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the current frame and the previous frame
    diff = cv2.absdiff(gray, prev_gray)

    # Threshold the difference to get the areas of motion
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Find contours of the thresholded areas
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x, y, w, h
    else:
        return 0, 0, frame.shape[1], frame.shape[0]

def apply_saliency(frame):
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    _, saliency_map = saliency.computeSaliency(frame)
    return (saliency_map * 255).astype("uint8")

# def get_focus_area(frame, saliency_map):
#     # Threshold the saliency map to get the areas of interest
#     _, thresh = cv2.threshold(saliency_map, 128, 255, cv2.THRESH_BINARY)

#     # Find contours of the thresholded areas
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if contours:
#         # Find the largest contour
#         largest_contour = max(contours, key=cv2.contourArea)
#         x, y, w, h = cv2.boundingRect(largest_contour)
#         return x, y, w, h
#     else:
#         return 0, 0, frame.shape[1], frame.shape[0]

def generate_focus_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height), False)

    ret, prev_frame = cap.read()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        x, y, w, h = get_focus_area(frame, prev_frame)
        focus_area = frame[y:y+h, x:x+w]
        focus_area_resized = cv2.resize(focus_area, (frame_width, frame_height))
        saliency_map = apply_saliency(focus_area_resized)
        out.write(saliency_map)

        prev_frame = frame

    cap.release()
    out.release()

# def generate_focus_video(input_video_path, output_video_path):
#     cap = cv2.VideoCapture(input_video_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height), False)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         saliency_map = apply_saliency(frame)
#         x, y, w, h = get_focus_area(frame, saliency_map)
#         focus_area = frame[y:y+h, x:x+w]
#         focus_area_resized = cv2.resize(focus_area, (frame_width, frame_height))
#         gray_frame = cv2.cvtColor(focus_area_resized, cv2.COLOR_BGR2GRAY)
#         out.write(gray_frame)

#     cap.release()
#     out.release()

def generate_focus_video_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.avi')):  # Add other video formats if needed
            input_video_path = os.path.join(input_folder, filename)
            output_video_path = os.path.join(output_folder, filename)

            print(f"Processing video: {input_video_path}")
            generate_focus_video(input_video_path, output_video_path)
            print(f"focus data video saved as: {output_video_path}")

# input_folder = "/home/achini/Documents/CarCrash/testing/rgb_videos/1"
# output_folder = "/home/achini/Documents/CarCrash/testing/focus_videos/1"
# generate_focus_video_folder(input_folder, output_folder)

for i in range(2, 21):
    input_folder = f"/home/achini/Documents/CarCrash/testing/rgb_videos/{i}"
    output_folder = f"/home/achini/Documents/CarCrash/testing/focus_videos/{i}"
    generate_focus_video_folder(input_folder, output_folder)