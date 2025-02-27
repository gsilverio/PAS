import os
import json
from extract_frames import extract_frames
from generate_descriptions import generate_descriptions_from_frames
from save_descriptions import save_descriptions_to_json

# Definição dos diretórios
video_dir = 'C:/Users/guilh/OneDrive/Área de Trabalho/PAS - CODE/msrvtt_videos'
output_base_dir = 'C:/temp'
output_json_dir = 'C:/Users/guilh/OneDrive/Área de Trabalho/PAS - CODE/msrvtt_description'

# Criar diretórios de saída se não existirem
os.makedirs(output_base_dir, exist_ok=True)
os.makedirs(output_json_dir, exist_ok=True)

def process_all_videos(video_dir, output_base_dir, output_json_dir):
    for video_name in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_name)
        
        if os.path.isfile(video_path) and video_name.endswith(('.mp4', '.avi', '.mov')):
            print(f"Processando vídeo: {video_name}")

            # Criar diretório para armazenar frames desse vídeo
            output_dir = os.path.join(output_base_dir, video_name.split('.')[0])
            os.makedirs(output_dir, exist_ok=True)

            # Passo 1: Extrair frames
            extract_frames(video_path, output_dir)

            # Passo 2: Gerar descrições dos frames
            descriptions = generate_descriptions_from_frames(output_dir)

            # Passo 3: Salvar as descrições em JSON
            output_file = os.path.join(output_json_dir, f"{video_name.split('.')[0]}_descriptions.json")
            save_descriptions_to_json(descriptions, video_name.split('.')[0], output_file)

            print(f"✅ Processamento concluído para {video_name}")

if __name__ == "__main__":
    process_all_videos(video_dir, output_base_dir, output_json_dir)
    print("\n🎬 Processamento finalizado! Arquivos de descrição gerados.")
