import streamlit as st
import pandas as pd
from utils.scrape import scrape_pages, test

# Define URLs for categories
CATEGORIES = {
    'Ordinateurs': 'https://www.expat-dakar.com/ordinateurs',
    'Telephones': 'https://www.expat-dakar.com/telephones',
    "TV Home Cinema": "https://www.expat-dakar.com/tv-home-cinema"
}

st.title('Expat-Dakar Scraper')

# Information about the app
st.markdown("""
This app scrapes data from Expat-Dakar and displays it in a DataFrame. It uses:
- **BeautifulSoup** to parse the HTML
- **Requests** to fetch the data
- **Pandas** to create the DataFrame
""")

# Selection box for categories
category = st.selectbox('Select Category', list(CATEGORIES.keys()))

# Input field for number of pages
pages = st.number_input('Number of pages to scrape', min_value=1, value=1)

df_test = test(2)
st.subheader('Test')
st.dataframe(df_test)

if st.button('Scrape Data'):
    url = CATEGORIES[category]
    items = scrape_pages(url, pages, tv=True if category == "TV Home Cinema" else False)
    
    # print("items", items)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(items)
    
    st.subheader(f'{category}')
    st.dataframe(df)

    