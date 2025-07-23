# app.py

import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import io

st.set_page_config(page_title="Color Palette Generator", layout="centered")

st.title("🎨 Color Palette Generator from Image")
st.markdown("Upload an image and extract its dominant colors with HEX codes.")

uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

def get_dominant_colors(image, n_colors=5):
    image = image.resize((200, 200))  # Resize for faster processing
    img_array = np.array(image)
    img_array = img_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
    kmeans.fit(img_array)

    colors = np.rint(kmeans.cluster_centers_).astype(int)
    hex_colors = ['#%02x%02x%02x' % tuple(color) for color in colors]

    return colors, hex_colors

def display_palette(colors, hex_colors):
    fig, ax = plt.subplots(figsize=(8, 2))
    for i, color in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=np.array(color) / 255))
        ax.text(i + 0.5, -0.2, hex_colors[i], ha='center', fontsize=12)

    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(fig)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📸 Uploaded Image", use_container_width=True)

    with st.spinner("Extracting colors..."):
        colors, hex_colors = get_dominant_colors(image)

    st.subheader("🎨 Dominant Colors")
    display_palette(colors, hex_colors)
