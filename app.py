import streamlit as st
import zipfile
import pandas as pd
import os

@st.cache_data
def load_csv_from_zip(zip_filename, csv_filename):
    extract_folder = 'unzipped_data'
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    csv_path = os.path.join(extract_folder, csv_filename)
    df = pd.read_csv(csv_path)
    return df

st.title("Fake and True News Data Viewer")

# Load both datasets
fake_df = load_csv_from_zip("Fake - Fake.zip", "Fake - Fake.csv")
true_df = load_csv_from_zip("True - True.zip", "True - True.csv")

st.subheader("Fake News Sample")
st.dataframe(fake_df.head())

st.subheader("True News Sample")
st.dataframe(true_df.head())
st.write("Files in current directory:", os.listdir('.'))

