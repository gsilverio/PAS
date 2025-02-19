import json
import os

def save_descriptions_to_json(descriptions, video_name, output_path):
    """
    Salva as descrições geradas em um arquivo JSON.

    :param descriptions: Dicionário com descrições dos frames.
    :param video_name: Nome do vídeo original.
    :param output_path: Caminho onde o JSON será salvo.
    """
    data = {
        "video": video_name,
        "descriptions": descriptions
    }

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"✅ Descrições salvas em {output_path}")
