
export const config = {
  runtime: "edge",
};

export default async function handler(request) {
  if (request.method !== "POST") {
    return Response.json(
      { error: "Método não permitido" },
      { status: 405 }
    );
  }

  try {
    const apiKey = process.env.PLANTNET_API_KEY;

    if (!apiKey) {
      return Response.json(
        { error: "Chave do PlantNet não configurada" },
        { status: 500 }
      );
    }

    const data = await request.formData();
    const image = data.get("image");

    if (!image || typeof image === "string") {
      return Response.json(
        { error: "Envie uma imagem da planta" },
        { status: 400 }
      );
    }

    const form = new FormData();
    form.append("images", image, image.name || "planta.jpg");
    form.append("organs", "auto");

    const response = await fetch(
      `https://my-api.plantnet.org/v2/identify/all?api-key=${encodeURIComponent(apiKey)}`,
      {
        method: "POST",
        body: form
      }
    );

    const result = await response.json();

    return Response.json(result, {
      status: response.status
    });

  } catch (error) {
    return Response.json(
      { error: "Erro ao identificar a planta" },
      { status: 500 }
    );
  }
}
