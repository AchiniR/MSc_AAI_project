import cv2
import os

def generate_saliency_map_video(input_video_path, output_video_path):
    # Load the video
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize video writer
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height), False)

    # Initialize saliency object
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Generate saliency map
        success, saliency_map = saliency.computeSaliency(frame)
        saliency_map = (saliency_map * 255).astype("uint8")

        # Write the frame to the output video
        out.write(saliency_map)

    cap.release()
    out.release()


def generate_saliency_map_video_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.avi')):  # Add other video formats if needed
            input_video_path = os.path.join(input_folder, filename)
            output_video_path = os.path.join(output_folder, filename)

            print(f"Processing video: {input_video_path}")
            generate_saliency_map_video(input_video_path, output_video_path)
            print(f"Saliency map video saved as: {output_video_path}")


# input_folder = "/home/achini/Documents/CarCrash/testing/rgb_videos/1"
# output_folder = "/home/achini/Documents/CarCrash/testing/salmap_videos/1"
# generate_saliency_map_video_folder(input_folder, output_folder)

for i in range(2, 21):
    input_folder = f"/home/achini/Documents/CarCrash/testing/rgb_videos/{i}"
    output_folder = f"/home/achini/Documents/CarCrash/testing/salmap_videos/{i}"
    generate_saliency_map_video_folder(input_folder, output_folder)