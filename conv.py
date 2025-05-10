from PIL import Image
from pathlib import Path
import os

def convertir_image_en_lignes_axidraw(chemin_image, chemin_sortie, espacement=5):
    """
    Convertit une image PNG en script pour AxiDraw utilisant grosdoudou
    en traçant des lignes horizontales espacées
    """
    try:
        image = Image.open(chemin_image)
    except FileNotFoundError:
        print(f"Erreur : image introuvable à {chemin_image}")
        return False
    
    # Vérifier les dimensions de l'image
    largeur, hauteur = image.size
    if largeur != 1060 or hauteur != 750:
        print(f"Erreur : l'image doit être de 1060x750 pixels (dimensions actuelles: {largeur}x{hauteur})")
        return False
    
    # Vérifier le format de l'image
    if not chemin_image.lower().endswith('.png'):
        print("Erreur : l'image doit être au format PNG")
        return False

    # Convertir l'image en niveau de gris si elle est en couleur
    if image.mode != 'L':  # L = niveau de gris
        image = image.convert('L')
    
    pixels = image.load()
    
    # Créer le script Python pour AxiDraw
    nom_fichier = Path(chemin_image).stem
    chemin_script = os.path.join(chemin_sortie, f"{nom_fichier}_lignes_axidraw.py")
    
    # Seuil pour déterminer si un pixel est noir ou blanc (0-255)
    seuil = 128
    
    with open(chemin_script, "w") as script:
        # En-tête et importations
        script.write(f"""# Script généré à partir de l'image: {chemin_image}
# Conversion en lignes horizontales avec espacement de {espacement} pixels

from grosdoudou import *

# Création de l'objet dessin avec un nom personnalisé
dessin = Dessin()

# Tracer la bordure
dessin.bordure()

# Tracé de l'image avec des lignes horizontales espacées
""")
        
        # Parcourir l'image par lignes horizontales espacées
        lignes_tracees = 0
        for y in range(20, hauteur-20, espacement):  # Respecter les marges de sécurité
            script.write(f"\n# Ligne y = {y}\n")
            
            # Pour chaque ligne, on trace des segments où il y a du noir
            segment_en_cours = False
            debut_x = 0
            
            for x in range(20, largeur-20):  # Respecter les marges de sécurité
                est_noir = pixels[x, y] < seuil
                
                if est_noir:
                    # Si on commence un nouveau segment
                    if not segment_en_cours:
                        segment_en_cours = True
                        debut_x = x
                else:
                    # Si on termine un segment
                    if segment_en_cours:
                        segment_en_cours = False
                        script.write(f"dessin.segment({debut_x}, {y}, {x}, {y})  # Segment noir\n")
                        lignes_tracees += 1
            
            # Ne pas oublier le dernier segment de la ligne s'il est en cours
            if segment_en_cours:
                script.write(f"dessin.segment({debut_x}, {y}, {largeur-20}, {y})  # Segment noir final\n")
                lignes_tracees += 1
        
        # Tracer le dessin et déconnecter l'AxiDraw
        script.write(f"""
# Nombre total de segments tracés: {lignes_tracees}

# Tracer le dessin
dessin.tracer()

# Déconnecter l'AxiDraw
dessin.deconnecter_axidraw()
""")
    
    print(f"Script AxiDraw généré avec succès: {chemin_script}")
    print(f"Nombre total de segments tracés: {lignes_tracees}")
    return True

def main():
    print("Convertisseur d'image PNG vers AxiDraw (style lignes horizontales)")
    print("-----------------------------------------------------------------")
    print("Note: L'image doit être en 1060x750 pixels et au format PNG")
    
    chemin_image = input("Entrez le chemin absolu de l'image PNG: ")
    chemin_sortie = input("Entrez le chemin absolu du dossier où enregistrer le script: ")
    
    try:
        espacement = int(input("Entrez l'espacement entre les lignes (par défaut 5 pixels): ") or "5")
    except ValueError:
        print("Valeur incorrecte, utilisation de la valeur par défaut (5)")
        espacement = 5
    
    convertir_image_en_lignes_axidraw(chemin_image, chemin_sortie, espacement)

if __name__ == "__main__":
    main()