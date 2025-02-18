import os

# Caminho do vídeo
video_path = 'path_to_your_video.mp4'
output_dir = 'extracted_frames'

# Extraindo os frames do vídeo
extract_frames(video_path, output_dir, interval=1)

# Gerar o embedding do texto (descrição fornecida pelo usuário)
description = "Homem andando a cavalo"
text_embedding = get_text_embedding(description)

# Comparando os frames com o texto
frame_files = os.listdir(output_dir)
similarities = []

for frame_file in frame_files:
    frame_path = os.path.join(output_dir, frame_file)
    image_embedding = get_image_embedding(frame_path)

    # Calculando a similaridade entre o texto e a imagem
    similarity = torch.cosine_similarity(text_embedding, image_embedding)
    similarities.append((frame_file, similarity.item()))

# Ordenar os resultados pela maior similaridade
similarities.sort(key=lambda x: x[1], reverse=True)

# Exibir os frames mais similares
for frame_file, similarity in similarities[:5]:
    print(f"Frame: {frame_file}, Similaridade: {similarity}")
