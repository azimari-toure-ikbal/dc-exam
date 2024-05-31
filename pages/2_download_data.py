import os
import streamlit as st
import pandas as pd

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Construct the full paths to the CSV files
ordinateurs_path = os.path.join(current_dir, 'datas/ordinateurs.csv')
telephones_path = os.path.join(current_dir, 'datas/telephones.csv')
tv_path = os.path.join(current_dir, 'datas/tv-home-cinema.csv')

st.title('Download Data')
st.markdown('Here you can download scraped data using webscraper as a CSV.')


# read data from csv file
ordinateurs_data = pd.read_csv(ordinateurs_path)
telephones_data = pd.read_csv(telephones_path)
tv_data = pd.read_csv(tv_path)

# Create DataFrames
ordinateurs_df = pd.DataFrame(ordinateurs_data)
telephones_df = pd.DataFrame(telephones_data)
tv_df = pd.DataFrame(tv_data)

# Select box for category
category = st.selectbox('Select Category', ['Ordinateurs', 'Telephones', 'Tv'])

# Based on selection, provide the corresponding DataFrame
if category == 'Ordinateurs':
    df = ordinateurs_df
elif category == 'Telephones':
    df = telephones_df
else:
    df = tv_df

# Display DataFrame
st.dataframe(df)

# # Download button
# st.markdown('### Download Data as CSV')
# csv = df.to_csv(index=False)
# st.download_button(label='Download CSV', data=csv, file_name=f'expat_dakar_{category.lower()}.csv', mime='text/csv')
