import streamlit as st
from collections import Counter

# --- FONCTIONS DE CHIFFREMENT ET DECHIFFREMENT ---
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()
    key_repeated = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]
    ciphertext = ""
    for p, k in zip(plaintext, key_repeated):
        ciphertext += chr(((ord(p) - 65) + (ord(k) - 65)) % 26 + 65)
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    key_repeated = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    plaintext = ""
    for c, k in zip(ciphertext, key_repeated):
        plaintext += chr(((ord(c) - 65) - (ord(k) - 65)) % 26 + 65)
    return plaintext

# --- ANALYSE DE FRÉQUENCE ---
def frequency_analysis(text):
    text = text.upper()
    counter = Counter(text)
    total = sum(counter.values())
    freq = {char: round(count / total, 3) for char, count in counter.items() if char.isalpha()}
    return freq

# --- INTERFACE STREAMLIT ---
st.title("Chiffrement de Vigenère & Analyse de Fréquence")

# Input de l'utilisateur
option = st.sidebar.selectbox("Choisissez une action :", ["Chiffrement", "Déchiffrement", "Analyse de fréquence"])

if option == "Chiffrement":
    st.header("Chiffrement de Vigenère")
    plaintext = st.text_input("Entrez le texte à chiffrer :", "")
    key = st.text_input("Entrez la clé :", "")
    if plaintext and key:
        ciphertext = vigenere_encrypt(plaintext, key)
        st.write(f"Texte chiffré : `{ciphertext}`")

elif option == "Déchiffrement":
    st.header("Déchiffrement de Vigenère")
    ciphertext = st.text_input("Entrez le texte chiffré :", "")
    key = st.text_input("Entrez la clé :", "")
    if ciphertext and key:
        plaintext = vigenere_decrypt(ciphertext, key)
        st.write(f"Texte déchiffré : `{plaintext}`")

elif option == "Analyse de fréquence":
    st.header("Analyse de fréquence")
    text = st.text_area("Entrez le texte à analyser :", "")
    if text:
        freq = frequency_analysis(text)
        st.write("Fréquence des lettres dans le texte :")
        st.bar_chart(freq)





