import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def plot_data(df):
    # Count the number of different "etat" per "marque"
    count_data = df.groupby(['marque', 'etat']).size().unstack(fill_value=0)

    # Plotting
    count_data.plot(kind='bar', stacked=True, figsize=(20, 14))
    plt.title('Number of Different "Etat" per "Marque"')
    plt.xlabel('Marque')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Etat')
    plt.tight_layout()

# Function to load data
def load_data(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    return pd.read_csv(file_path)

# Load data
ordinateurs_df = load_data('datas/ordinateurs.csv')
telephones_df = load_data('datas/telephones.csv')
tv_home_cinema_df = load_data('datas/tv-home-cinema.csv')

# print(f"ORDINATEURS: {}")

st.set_option('deprecation.showPyplotGlobalUse', False)

# Streamlit app
st.title('Dashboard View')
st.markdown('This is the dashboard view where you can visualize the data.')

# Create a 3-column layout
col1, col2 = st.columns(2)


# # Column 1: Ordinateurs
with col1:
    st.header('Ordinateurs')
    plot_data(ordinateurs_df)
    st.pyplot()
    
# # Column 2: Telephones
with col2:
    st.header('Telephones')
    plot_data(telephones_df)
    st.pyplot()

# # Column 3: TV & Home Cinema
with col1:
    st.header('TV')
    plot_data(tv_home_cinema_df)
    st.pyplot()