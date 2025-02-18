import cv2
import os

# Função para extrair frames de um vídeo
def extract_frames(video_path, output_dir, interval=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Frames por segundo
    count = 0
    success = True
    frame_num = 0

    while success:
        success, frame = cap.read()
        if frame_num % int(frame_rate * interval) == 0:
            frame_filename = os.path.join(output_dir, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            count += 1
        frame_num += 1

    cap.release()
