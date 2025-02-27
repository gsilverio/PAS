import torch
from transformers import CLIPProcessor, CLIPModel

# Carregar o modelo CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Definição do threshold mínimo de similaridade
SIMILARITY_THRESHOLD = 0.5

def find_best_matching_video(user_query, descriptions_dict):
    """
    Compara a descrição do usuário com as descrições dos vídeos usando CLIP.
    
    :param user_query: Texto da consulta do usuário.
    :param descriptions_dict: Dicionário {video_nome: [lista de descrições]}
    :return: Lista de vídeos ordenados por similaridade (acima do threshold).
    """
    # Criar embeddings para a consulta do usuário
    inputs = processor(text=[user_query], return_tensors="pt", padding=True)
    with torch.no_grad():
        user_embedding = model.get_text_features(**inputs)
        user_embedding = torch.nn.functional.normalize(user_embedding, p=2, dim=-1)  # Normaliza os embeddings

    video_scores = {}

    for video_name, descriptions in descriptions_dict.items():
        # Criar embeddings para todas as descrições do vídeo
        inputs = processor(text=descriptions, return_tensors="pt", padding=True)
        with torch.no_grad():
            description_embeddings = model.get_text_features(**inputs)
            description_embeddings = torch.nn.functional.normalize(description_embeddings, p=2, dim=-1)

        # Calcular similaridade de cosseno
        similarity = torch.nn.functional.cosine_similarity(user_embedding, description_embeddings)
        max_similarity = similarity.max().item()  # Maior similaridade entre todas as descrições do vídeo

        # Apenas adiciona vídeos acima do threshold
        if max_similarity >= SIMILARITY_THRESHOLD:
            video_scores[video_name] = max_similarity

    # Ordenar os vídeos por similaridade (do maior para o menor)
    sorted_videos = sorted(video_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_videos
