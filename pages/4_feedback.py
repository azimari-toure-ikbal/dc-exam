import requests
import streamlit as st

kobo_api_url = 'https://kf.kobotoolbox.org/api/v2/assets/ahsc39nfXJMptxKZ4nMo8d/submissions'
kobo_api_token = ""

def submit_to_kobo(data):
    headers = {
        'Authorization': kobo_api_token, 
        'Content-Type': 'application/json'
    }
    response = requests.post(kobo_api_url, json=data, headers=headers)
    return response

st.title('Feedback')
st.markdown("Certes, nobles visiteurs et preux compagnons, Soyez les bienvenus en cette humble demeure virtuelle, où se dresse notre formulaire d'appréciation. En ce lieu sacré, vos avis et ressentis sont des trésors plus précieux que l'or des royaumes. Par vos paroles sincères et éclairées, vous nous permettrez d'améliorer notre projet et d'accroître la satisfaction de tous ceux qui s'y aventurent. Nous vous prions donc de prendre un instant pour nous faire part de vos pensées et observations. Chaque mot que vous laisserez en ces pages sera considéré avec la plus grande révérence et gratitude. Ainsi, votre expérience et vos suggestions guideront nos futurs pas et renforceront notre quête commune de perfection. Que votre plume soit guidée par la sagesse et la bienveillance, et que votre honnêteté illumine notre chemin. Avec nos salutations respectueuses et notre reconnaissance éternelle, L'Équipe de votre projet dévoué")

with st.form(key='feedback_form'):
    # Form fields
    prenom_nom = st.text_input('Prénom et Nom')
    
    st.markdown('### UI / UX')
    ui_ux_options = ["Boff", "Pas mal", "Bon", "Chapeau l'artiste"]
    ui_ux_rating = st.radio("Sur combien notez-vous l'expérience utilisateur et le design de l'application ?", ui_ux_options, index=0)
    
    st.markdown('### Informations')
    informations = st.radio("Est-ce que les informations sur ce site vous ont été utiles ?", ["Oui", "Non"], index=0)
    
    st.markdown('### Recommendations')
    recommendations = st.radio("Seriez-vous tenter de recommander notre site à vos proches ?", ["Oui", "Non", "Maybeee"], index=0)
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Prepare data for KoboToolbox
    data = {
        'prenom_nom': prenom_nom,
        'ui_ux_rating': ui_ux_rating,
        'informations': informations,
        'recommendations': recommendations
    }
    
    response = submit_to_kobo(data)
    
    if response.status_code == 201:
        st.success('Feedback submitted successfully!')
    else:
        print(response.text)
        st.error(f'Failed to submit feedback. Status code: {response.status_code}')