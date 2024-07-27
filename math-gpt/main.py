import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import os

# Configure your OpenAI API key
# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# Function to render the response with LaTeX
def render_response(response):

    # Having response replace [\ and \] with $$ and  \( and \) with $ to render LaTeX
    response = (
        response.replace(r"\[", "$$")
        .replace(r"\]", "$$")
        .replace(r"\(", "$")
        .replace(r"\)", "$")
    )

    st.write(response)

    # lines = response.split("\n")
    # for line in lines:
    #     # if line.startswith("[") and line.endswith("]"):
    #     #     try:
    #     #         st.latex(r"{}".format(line[1:-1]))
    #     #     except Exception as e:
    #     #         st.error(f"Error rendering LaTeX: {e}")
    #     # else:
    #     #     st.markdown(line)
    #     st.text(line)


# Function to call GPT-4
def obtener_respuesta(prompt, base64_image):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente experto en resolver problemas matemáticos.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
    )
    return response.choices[0].message.content


# Configure the Streamlit interface
st.title("MathGPT - Resolución de Problemas Matemáticos")

# Upload the image
uploaded_image = st.file_uploader(
    "Sube una imagen con el problema matemático", type=["png", "jpg", "jpeg"]
)

# Enter the prompt
prompt = st.text_area("Describe el problema matemático o agrega información adicional:")

# Send button
if st.button("Obtener respuesta"):
    if uploaded_image is not None and prompt:
        # Load the image
        image = Image.open(uploaded_image)
        st.image(image, caption="Imagen subida", use_column_width=True)

        # Convert the image to bytes to pass it to the prompt
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_data = image_bytes.getvalue()
        # Encode the image to base64
        base64_image = base64.b64encode(image_data).decode("utf-8")

        # Create the prompt including the image
        final_prompt = f"Resuelve el siguiente problema matemático basado en esta imagen y la información proporcionada: {prompt}"

        # Get the response from GPT-4
        respuesta = obtener_respuesta(final_prompt, base64_image)

        # Show the response
        render_response(respuesta)
    else:
        st.error("Por favor, sube una imagen y proporciona un prompt.")
