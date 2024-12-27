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

# Interface utilisateur avec Streamlit
def main():
    st.title("Décryptage du Chiffre de Vigenère")
    st.write("Ce programme permet de décrypter un texte chiffré avec le chiffre de Vigenère à l'aide de méthodes analytiques.")

    # Entrée de l'utilisateur
    ciphertext = st.text_area("Entrez le texte chiffré :").upper()
    if not ciphertext:
        st.warning("Veuillez entrer un texte chiffré pour continuer.")
        return

    # Supprimer les caractères non alphabétiques
    ciphertext = ''.join(filter(str.isalpha, ciphertext))

    # Analyse avec l'indice de coïncidence
    st.subheader("Analyse automatique avec l'indice de coïncidence")
    max_len = st.slider("Longueur maximale de la clé à tester :", 1, 50, 20)
    key_len = longueur_cle_probable(ciphertext, max_len)
    st.write(f"Longueur estimée de la clé : {key_len}")

    # Estimation de la clé
    key = estimer_cle(ciphertext, key_len)
    st.write(f"Clé estimée : {key}")

    # Décryptage du texte
    decrypted_text = dechiffrer_vigenere(ciphertext, key)
    st.subheader("Résultat du décryptage")
    st.write(decrypted_text)

# Exécution de l'application
if __name__ == "__main__":
    main()


