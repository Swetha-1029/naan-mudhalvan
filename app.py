import streamlit as st
import zipfile
import pandas as pd
import os

@st.cache_data
def load_data_from_zip(zip_path, csv_filename):
    extract_folder = 'temp_data'
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    csv_file = os.path.join(extract_folder, csv_filename)
    df = pd.read_csv(csv_file)
    return df

def main():
    st.title("Dual Dataset Viewer")

    dataset_choice = st.selectbox("Choose dataset to view:", ["Dataset A", "Dataset B"])

    if dataset_choice == "Dataset A":
        df = load_data_from_zip("Fake-Fake.zip", "Fake-Fake.csv")
    else:
        df = load_data_from_zip("True-True.zip", "True-True.csv")

    st.write(f"Showing data from: {dataset_choice}")
    st.dataframe(df.head())

if __name__ == "__main__":
    main()
