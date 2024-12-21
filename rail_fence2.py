import streamlit as st

# Fonction pour chiffrer avec le Rail Fence Cipher
def rail_fence_encrypt(plaintext, k):
    rails = [''] * k
    direction = 1  # 1 signifie descendre, -1 signifie remonter
    rail_index = 0

    for char in plaintext:
        rails[rail_index] += char
        if rail_index == 0:
            direction = 1
        elif rail_index == k - 1:
            direction = -1
        rail_index += direction

    return ''.join(rails)

# Fonction pour déchiffrer avec le Rail Fence Cipher
def rail_fence_decrypt(ciphertext, k):
    rails = [''] * k
    direction = 1
    rail_index = 0
    rail_lengths = [0] * k

    for char in ciphertext:
        rail_lengths[rail_index] += 1
        if rail_index == 0:
            direction = 1
        elif rail_index == k - 1:
            direction = -1
        rail_index += direction

    index = 0
    for i in range(k):
        rails[i] = ciphertext[index:index + rail_lengths[i]]
        index += rail_lengths[i]

    result = []
    rail_index = 0
    direction = 1

    for _ in range(len(ciphertext)):
        result.append(rails[rail_index][0])
        rails[rail_index] = rails[rail_index][1:]
        if rail_index == 0:
            direction = 1
        elif rail_index == k - 1:
            direction = -1
        rail_index += direction

    return ''.join(result)

# Interface Streamlit
st.title("Chiffrement Rail Fence")

# Entrée du nombre de niveaux (k)
k = st.number_input("Entrez le nombre de niveaux (k >= 2) :", min_value=2, value=2, step=1)

# Texte d'entrée
text = st.text_input("Entrez le texte :")

# Choix entre chiffrer ou déchiffrer
action = st.radio("Action :", ["Chiffrer", "Déchiffrer"])

if st.button("Exécuter"):
    if action == "Chiffrer":
        if text:
            ciphertext = rail_fence_encrypt(text.replace(" ", "").upper(), k)
            st.success(f"Texte chiffré : {ciphertext}")
        else:
            st.error("Veuillez entrer un texte à chiffrer.")
    elif action == "Déchiffrer":
        if text:
            decrypted_text = rail_fence_decrypt(text, k)
            st.success(f"Texte déchiffré : {decrypted_text}")
        else:
            st.error("Veuillez entrer un texte à déchiffrer.")
