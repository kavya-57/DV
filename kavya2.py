import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import pdfplumber

# --- Page Config ---
st.set_page_config(page_title="Text Visualizer", layout="wide")

# --- Title ---
st.title("📊 Text Visualizer from PDF or Manual Input")
st.write("Upload a PDF or paste text to generate Word Cloud, Pie Chart, and Bar Chart.")

# --- Sidebar Input ---
st.sidebar.header("📁 Upload or Paste Text")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
manual_text = st.sidebar.text_area("Or paste your text here", height=150)

# --- Extract Text ---
text_data = ""

if uploaded_file:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_data += page_text + " "
        if text_data.strip():
            st.sidebar.success("✅ PDF text extracted successfully!")
        else:
            st.sidebar.warning("⚠️ No extractable text found in the PDF.")
    except Exception as e:
        st.sidebar.error(f"❌ Error reading PDF: {e}")

elif manual_text:
    text_data = manual_text
    st.sidebar.success("✅ Using manually entered text.")

# --- Visualizations ---
if text_data.strip():
    # --- Word Frequency ---
    words = pd.Series(text_data.lower().split())
    word_freq = words.value_counts().head(10)

    # --- Layout ---
    col1, col2 = st.columns(2)

    # --- Word Cloud ---
    with col1:
        st.subheader("☁️ Word Cloud")
        wordcloud = WordCloud(width=600, height=300, background_color='white').generate(text_data)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

    # --- Pie Chart ---
    with col2:
        st.subheader("🥧 Top 10 Words - Pie Chart")
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(word_freq.values, labels=word_freq.index, autopct='%1.1f%%', startangle=140)
        ax_pie.axis('equal')
        st.pyplot(fig_pie)

    # --- Bar Chart ---
    st.subheader("📶 Top 10 Words - Bar Chart")
    st.bar_chart(word_freq)

else:
    st.info("Please upload a PDF or enter some text to begin visualizing.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and pdfplumber. Ideal for survey analysis, feedback reports, or health data insights.")
