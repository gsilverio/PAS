from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

# Inicializar o modelo BLIP e o processador
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_descriptions_from_frames(frame_dir):
    descriptions = []
    
    # Obter todos os arquivos de imagem do diretório de frames
    for filename in os.listdir(frame_dir):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            img_path = os.path.join(frame_dir, filename)
            img = Image.open(img_path).convert("RGB")

            # Preparar a imagem para o modelo BLIP
            inputs = processor(images=img, return_tensors="pt")

            # Gerar a descrição a partir do modelo BLIP
            out = model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)

            descriptions.append({"frame": filename, "description": description})
            print(f"Descrição gerada para o frame {filename}: {description}")
    
    return descriptions
