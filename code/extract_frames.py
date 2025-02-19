import cv2
import os

def extract_frames(video_path, output_dir, frame_interval=30):
    """
    Extrai frames de um vídeo e os salva na pasta especificada.

    :param video_path: Caminho do vídeo de entrada.
    :param output_dir: Diretório onde os frames serão salvos.
    :param frame_interval: Número de frames a pular entre cada extração.
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Erro ao abrir o vídeo: {video_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0
    saved_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break  # Sai do loop quando o vídeo termina

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"🖼️ Frame salvo: {frame_filename}")
            saved_count += 1

        frame_count += 1

    cap.release()
