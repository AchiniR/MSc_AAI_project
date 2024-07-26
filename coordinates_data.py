import cv2
import os

def get_centroid(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    return None

def get_coordinates(frame, prev_frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray, prev_gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coordinates = []

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area threshold
            centroid = get_centroid(contour)
            if centroid:
                coordinates.append(centroid)
    return coordinates

def annotate_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    coordinates = {}
    ret, prev_frame = cap.read()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_number > 0:
            coords = get_coordinates(frame, prev_frame)
            coordinates[frame_number] = coords
        prev_frame = frame
        frame_number += 1

    cap.release()
    
    
    # Save coordinates to a text file
    video_filename = os.path.basename(video_path).split('.')[0]  # Extract video name without extension
    coord_file_path = os.path.join(output_dir, f"{video_filename}_coordinate.txt")

    with open(coord_file_path, 'w') as f:
        for frame_number, coords in coordinates.items():
            for coord in coords:
                f.write(f"{frame_number},{coord[0]},{coord[1]}\n")


def process_videos_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video_file in os.listdir(input_folder):
        video_path = os.path.join(input_folder, video_file)
        if os.path.isfile(video_path) and video_file.lower().endswith(('.avi')):
            print(f"Processing video: {video_path}")
            annotate_video(video_path, output_folder)

# input_folder = "/home/achini/Documents/CarCrash/testing/rgb_videos/1"
# output_folder = "/home/achini/Documents/CarCrash/testing/coordinate/1"
# process_videos_in_folder(input_folder, output_folder)

for i in range(1, 21):
    input_folder = f"/home/achini/Documents/CarCrash/testing/rgb_videos/{i}"
    output_folder = f"/home/achini/Documents/CarCrash/coordinate/{i}"
    process_videos_in_folder(input_folder, output_folder)
