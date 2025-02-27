import { useState } from "react";
import { useForm } from "react-hook-form";
import "./styles.css";

const API_URL = "http://127.0.0.1:8000/search/";

export default function SearchComponent() {
  const { register, handleSubmit, reset } = useForm();
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (data) => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: data.description }),
      });

      const result = await response.json();
      if (result.results.length > 0) {
        setVideos(result.results);
      } else {
        setVideos([]);
        setError("Nenhum vídeo encontrado para essa descrição.");
      }
    } catch (err) {
      console.error("Erro na requisição:", err);
      setError("Erro ao buscar vídeos.");
    } finally {
      setLoading(false);
      reset();
    }
  };

  return (
    <div className="main-container">
      {/* Parte esquerda com o título estilizado */}
      <div className="left-section">
        <h1 className="title">📽 Video Retrival System</h1>
      </div>

      {/* Parte direita com a busca e os vídeos */}
      <div className="right-section">
        <h4>🔎 Busca de Vídeos</h4>
        <form onSubmit={handleSubmit(onSubmit)} className="search-form">
          <input
            {...register("description", { required: true })}
            type="text"
            placeholder="Digite a descrição..."
            className="input"
          />
          <button type="submit" className="button">
            Buscar
          </button>
        </form>

        {loading && <p className="loading">🔍 Buscando vídeos...</p>}
        {error && <p className="error">{error}</p>}

        <div className="video-grid">
          {videos.map((video, index) => (
            <div key={video.video} className="video-card">
              <span className="ranking">{index + 1}º</span>
              <p className="video-title">Titulo: {video.video}</p>
              <p className="similarity">
                🎯 Similaridade: {Math.round(video.score * 100)}%
              </p>
              <video controls className="video-player">
                <source src={video.video_url} type="video/mp4" />
                Seu navegador não suporta vídeos.
              </video>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
