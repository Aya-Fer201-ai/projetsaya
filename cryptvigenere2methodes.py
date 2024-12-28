import numpy as np
from collections import Counter
import streamlit as st

# Fonction pour calculer l'indice de coïncidence
def indice_coincidence(text):
    n = len(text)
    if n <= 1:
        return 0
    freq = Counter(text)
    IC = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return IC

# Fonction pour trouver la longueur probable de la clé
def longueur_cle_probable(text, max_len=20):
    ICs = []
    for k in range(1, max_len + 1):
        segments = [text[i::k] for i in range(k)]
        if any(len(segment) <= 1 for segment in segments):
            ICs.append(0)
        else:
            ICs.append(np.mean([indice_coincidence(segment) for segment in segments]))
    return ICs.index(max(ICs)) + 1 if ICs else 1

# Fonction pour chiffrer le texte en utilisant le chiffre de Vigenère
def chiffrer_vigenere(text, key):
    key = key.upper()
    encrypted = []
    key_len = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)
    return ''.join(encrypted)

# Fonction pour déchiffrer le texte chiffré en utilisant la clé estimée
def dechiffrer_vigenere(text, key):
    key = key.upper()
    decrypted = []
    key_len = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# Fonction pour estimer la clé en utilisant l'analyse fréquentielle
def estimer_cle(text, key_len):
    subtexts = [''.join(text[i::key_len]) for i in range(key_len)]
    key = ''
    for subtext in subtexts:
        if not subtext:
            key += 'A'  # Par défaut, ajouter 'A' si le segment est vide
        else:
            freq = Counter(subtext)
            most_common = freq.most_common(1)[0][0]
            shift = (ord(most_common) - ord('E')) % 26
            key += chr(shift + ord('A'))
    return key

# Fonction pour estimer la clé en utilisant l'analyse de fréquence par sous-texte
def estimer_cle_freq(text, key_len):
    key = ""
    for i in range(key_len):
        subtext = text[i::key_len]
        freq = Counter(subtext)
        most_common = freq.most_common(1)[0][0]
        shift = (ord(most_common) - ord('E')) % 26
        key += chr(shift + ord('A'))
    return key

# Interface utilisateur avec Streamlit
st.title("Chiffre de Vigenère")
plaintext = st.text_input("Veuillez entrer le texte à chiffrer :").upper()
key = st.text_input("Veuillez entrer la clé :").upper()

if st.button("Chiffrer"):
    # Retirer les espaces et les caractères non alphabétiques du texte clair
    plaintext_filtered = ''.join(filter(str.isalpha, plaintext))

    # Chiffrer le texte
    ciphertext = chiffrer_vigenere(plaintext_filtered, key)
    
    # Afficher le texte chiffré
    st.write(f"Texte chiffré : {ciphertext}")

    # Demander à l'utilisateur de choisir la méthode de déchiffrement
    choix = st.radio("Choisissez une méthode pour déchiffrer :", ("Estimation de la clé avec analyse fréquentielle", "Analyse avec l'indice de coïncidence"))

    # Déterminer la longueur de la clé probable
    key_len = longueur_cle_probable(ciphertext)
    
    # Afficher la longueur estimée de la clé
    st.write(f"Longueur estimée de la clé : {key_len}")

    # Estimer la clé et déchiffrer le texte
    if choix == 'Estimation de la clé avec analyse fréquentielle':
        key_estimee = estimer_cle(ciphertext, key_len)
    else:
        key_estimee = estimer_cle_freq(ciphertext, key_len)

    st.write(f"Clé estimée : {key_estimee}")
    
    decrypted_text = dechiffrer_vigenere(ciphertext, key_estimee)
    
    # Afficher le texte déchiffré
    st.write("Texte déchiffré :")
    st.write(decrypted_text)

# Exécuter l'application Streamlit