import numpy as np
from collections import Counter

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

# Fonction principale
def main():
    # Demander à l'utilisateur d'entrer le texte à chiffrer et la clé
    plaintext = input("Veuillez entrer le texte à chiffrer : ").upper()
    key = input("Veuillez entrer la clé : ").upper()

    # Retirer les espaces et les caractères non alphabétiques du texte clair
    plaintext = ''.join(filter(str.isalpha, plaintext))

    # Chiffrer le texte
    ciphertext = chiffrer_vigenere(plaintext, key)
    print(f"Texte chiffré : {ciphertext}")

    # Retirer les espaces et les caractères non alphabétiques du texte chiffré
    ciphertext = ''.join(filter(str.isalpha, ciphertext))

    # Demander à l'utilisateur de choisir la méthode de déchiffrement
    print("Choisissez une méthode pour déchiffrer :")
    print("1. Estimation de la clé avec analyse fréquentielle")
    print("2. Analyse avec l'indice de coïncidence")
    choix = input("Entrez 1 ou 2 : ")

    # Déterminer la longueur de la clé probable
    key_len = longueur_cle_probable(ciphertext)
    print(f"Longueur estimée de la clé : {key_len}")

    # Estimer la clé et déchiffrer le texte
    if choix == '1':
        key_estimee = estimer_cle(ciphertext, key_len)
    elif choix == '2':
        key_estimee = estimer_cle_freq(ciphertext, key_len)
    else:
        print("Choix invalide.")
        return

    print(f"Clé estimée : {key_estimee}")
    decrypted_text = dechiffrer_vigenere(ciphertext, key_estimee)
    print("Texte déchiffré :")
    print(decrypted_text)

# Exécuter la fonction principale
if _name_ == "_main_":
    main()

