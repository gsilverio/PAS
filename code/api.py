import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Para servir arquivos estáticos
from pydantic import BaseModel
from clip_matching import find_best_matching_video

# Diretórios
VIDEO_DIR = "msrvtt_videos"  # Corrigido para servir vídeos da pasta correta
JSON_DIR = "msrvtt_description"

# Criar a API
app = FastAPI()

# Adicionar CORS (para permitir requisições do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acesso de qualquer origem (ajuste se necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (vídeos da pasta msrvtt_videos)
app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")


class SearchRequest(BaseModel):
    description: str


# Carregar descrições dos vídeos na inicialização
descriptions_dict = {}
for json_file in os.listdir(JSON_DIR):
    if json_file.endswith("_descriptions.json"):
        try:
            with open(os.path.join(JSON_DIR, json_file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if "video" in data and "descriptions" in data:
                    video_name = data["video"]
                    descriptions = [desc["description"] for desc in data["descriptions"]]
                    descriptions_dict[video_name] = descriptions
        except Exception as e:
            print(f"❌ Erro ao carregar {json_file}: {e}")


@app.post("/search/")
async def search_videos(request: SearchRequest):
    """
    Busca os vídeos mais semelhantes à descrição fornecida pelo usuário.
    """
    matching_videos = find_best_matching_video(request.description, descriptions_dict)

    response = [
        {
            "video": video,
            "score": round(score, 4),
            "video_url": f"http://127.0.0.1:8000/videos/{video}.mp4",  # Agora servindo da pasta correta
        }
        for video, score in matching_videos[:5]
    ]

    return {"query": request.description, "results": response}


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 API iniciada! Acesse em http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
