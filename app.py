import os
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.get("/")
def inicio():
    return "TerraSense conectado!"

@app.post("/identificar")
def identificar():
    chave = os.environ.get("PLANTNET_API_KEY")

    if not chave:
        return jsonify({"erro": "Chave API não configurada"}), 500

    imagem = request.get_data()

    if not imagem:
        return jsonify({"erro": "Nenhuma imagem recebida"}), 400

    tipo = request.headers.get(
        "Content-Type", "image/jpeg"
    ).split(";")[0]

    if tipo not in ["image/jpeg", "image/png"]:
        return jsonify({"erro": "Formato de imagem inválido"}), 415

    extensao = "png" if tipo == "image/png" else "jpg"

    try:
        resposta = requests.post(
            "https://my-api.plantnet.org/v2/identify/all",
            params={"api-key": chave, "lang": "pt"},
            files={
                "images": (
                    f"planta.{extensao}",
                    imagem,
                    tipo
                )
            },
            data={"organs": "auto"},
            timeout=60
        )

        return Response(
            resposta.content,
            status=resposta.status_code,
            content_type="application/json"
        )

    except requests.RequestException:
        return jsonify({"erro": "Falha ao conectar com Pl@ntNet"}), 502
