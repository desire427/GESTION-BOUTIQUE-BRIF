import re
from datetime import datetime
import mysql.connector
import sys
boutique_gestion_systeme = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = 'Birane_2024!',
  database ='boutique_gestion_systeme'
)
print("Connexion réussie")


def afficher_separateur(caractere="=", longueur=70):
    print(caractere * longueur)

def formater_prix(prix):
    return f"{prix:,.0f}".replace(",", " ")

def obtenir_date_heure():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def generer_code_produit():
    cursor = boutique_gestion_systeme.cursor()
    cursor.execute("SELECT MAX(id_produit) FROM Produits")
    res = cursor.fetchone()[0]
    next_id = (res or 0) + 1
    return f"P{next_id:03d}"

# --- FONCTIONNALITÉS ---

# Ajout d'une Catégorie
def ajouter_categorie():
    cursor = boutique_gestion_systeme.cursor()
    while True:
        nom_categorie = input("Nouvelle catégorie : ").strip().capitalize()
        if nom_categorie.isalpha():
            break
        else:
            print("Nom invalide, lettres uniquement !")
    
    try:
        cursor.execute("INSERT INTO Categories (nom_categorie) VALUES (%s)", (nom_categorie,))
        boutique_gestion_systeme.commit()
        print(f" Catégorie '{nom_categorie}' ajoutée.")
    except mysql.connector.Error:
        print("Erreur : Cette catégorie existe déjà.")

# Ajout d'un produit
def ajouter_produit():
    cursor = boutique_gestion_systeme.cursor()
    
    # Lister catégories
    cursor.execute("SELECT id_categorie, nom_categorie FROM Categories")
    cats = cursor.fetchall()
    print("\nCatégories :")
    for c in cats: 
        print(f"[{c[0]}] {c[1]}")
    
    while True:
        id_categorie = input("ID Catégorie : ")
        if id_categorie.isdigit() and any(int(id_categorie) == c[0] for c in cats):
            break
        else:
            print("ID inexistant !")
    
    while True:
        designation = input("Désignation : ").strip().capitalize()
        if designation.replace(" ", "").isalnum() and len(designation) >= 3: 
            break
        else:
            print("Veuillez saisir une désignation valide (lettres/chiffres, min 3 caractères)")
        
    while True:
        prix = input("Prix unitaire : ")
        if prix.isdigit() and int(prix) >=100:
            break
        else:
            print("Montant invalide !")
        
    while True:
        quantite = input("Quantité initiale : ")
        if quantite.isdigit(): 
            break
        else:
            print("Veuillez saisir uniquement des chiffres !")

    code = generer_code_produit()
    statut = 'Disponible' if int(quantite) > 0 else 'En rupture'
    
    try:
        cursor.execute("""
            INSERT INTO Produits (code_produit, designation, prix, quantite, statut_produit, id_categorie)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (code, designation, float(prix), int(quantite), statut, int(id_categorie)))
        
        id_produit = cursor.lastrowid
        if int(quantite) > 0:
            cursor.execute("INSERT INTO Mouvements (nature_mouvement, quantite_mouv, id_produit) VALUES ('Achat', %s, %s)", (int(quantite), id_produit))
        boutique_gestion_systeme.commit()
        print(f" Produit {code} ajouté avec succès !")
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

# Affichage des produits
def afficher_tous_produits():
    cursor = boutique_gestion_systeme.cursor()
    cursor.execute("""
        SELECT p.code_produit, p.designation, c.nom_categorie, p.prix, p.quantite, p.statut_produit
        FROM Produits as p JOIN Categories as c ON p.id_categorie = c.id_categorie
    """)
    rows = cursor.fetchall()
    
    afficher_separateur("─", 85)
    print(f"{'Code':<8} {'Nom':<25} {'Catégorie':<15} {'Prix':<12} {'Qté':<6} {'Statut'}")
    afficher_separateur("─", 85)
    
    for r in rows:
        print(f"{r[0]:<8} {r[1]:<25} {r[2]:<15} {formater_prix(r[3]):>9}   {r[4]:>4}   {r[5]}")
    
    afficher_separateur("─", 85)

# Liste des produits par catégorie
def lister_produits_par_categorie():
    cursor = boutique_gestion_systeme.cursor()
    cursor.execute("SELECT id_categorie, nom_categorie FROM Categories")
    cats = cursor.fetchall()
    
    if not cats:
        print("Aucune catégorie enregistrée.")
        return

    print("\nChoisissez une catégorie :")
    for c in cats:
        print(f"[{c[0]}] {c[1]}")
    
    choix = input("ID Catégorie : ")
    if not choix.isdigit() or not any(int(choix) == c[0] for c in cats):
        print("ID invalide.")
        return

    cursor.execute("""
        SELECT p.code_produit, p.designation, p.prix, p.quantite, p.statut_produit
        FROM Produits p WHERE p.id_categorie = %s
    """, (int(choix),))
    rows = cursor.fetchall()

    print(f"\nProduits de la catégorie sélectionnée :")
    afficher_separateur("─", 75)
    print(f"{'Code':<8} {'Nom':<25} {'Prix':<12} {'Qté':<6} {'Statut'}")
    afficher_separateur("─", 75)
    for r in rows:
        print(f"{r[0]:<8} {r[1]:<25} {formater_prix(r[2]):>9}   {r[3]:>4}   {r[4]}")
    afficher_separateur("─", 75)

# Vendre un produit
def vendre_produit():
    cursor = boutique_gestion_systeme.cursor()
    while True:
        code = input("Code produit à vendre : ").strip().upper()
        query = """ INSERT INTO Produits (id_produit, code_produit, designation, prix, quantite) VALUES (%s, %s, %s, %s, %s)"""
        # ... inside vendre_produit() ...
        cursor.execute("SELECT id_produit, designation, prix, quantite FROM Produits WHERE code_produit = %s", (code,))
        res = cursor.fetchone()

        if not res:
            print(" Code inconnu.")
            continue

        id_produit, designation, prix, quantite = res

        if quantite <= 0:
            print(f" Rupture de stock pour {designation} !")
            return
        else:
            break

    while True:
        qte = input(f"Quantité à vendre (Max {quantite}) : ")
        if qte.isdigit() and 0 < int(qte) <= quantite:
            qte = int(qte)
            break
        else:
            print("Quantité invalide !")

    nouveau_stock = quantite - qte
    statut = 'Disponible' if nouveau_stock > 0 else 'En rupture'
    
    cursor.execute("UPDATE Produits SET quantite = %s, statut_produit = %s WHERE id_produit = %s", (nouveau_stock, statut, id_produit))
    cursor.execute("INSERT INTO Mouvements (nature_mouvement, quantite_mouv, id_produit) VALUES ('Vente', %s, %s)", (qte, id_produit))
    
    boutique_gestion_systeme.commit()
    print(f" Vente réussie ! Total : {formater_prix(prix * qte)} F CFA")
# Affichage du stock restant
def afficher_alertes():
    cursor = boutique_gestion_systeme.cursor()
    cursor.execute("SELECT designation, quantite FROM Produits WHERE quantite < 5")
    rows = cursor.fetchall()
    print("\n ALERTES STOCK FAIBLE (< 5) :")
    if not rows: 
        print("Aucune alerte.")
    else:
        for r in rows:
            print(f"- {r[0]} : {r[1]} restant(s)")

# Modification d'un produit
def modifier_produit():
    """Modifie les informations d'un produit existant"""
    cursor = boutique_gestion_systeme.cursor()
    print("\n" + "─" * 60)
    print("   MODIFIER UN PRODUIT")
    print("─" * 60)
    
    code = input("Code du produit à modifier : ").strip().upper()
    cursor.execute("SELECT id_produit, designation, prix, quantite FROM Produits WHERE code_produit = %s", (code,))
    res = cursor.fetchone()
    
    if not res:
        print(f" Aucun produit trouvé avec le code '{code}'.")
        return
    
    id_produit, designation, prix_actuel, quantite_actuelle = res
    print(f"\n Produit actuel :")
    print(f"   Nom : {designation}")
    print(f"   Prix : {formater_prix(prix_actuel)} F CFA")
    print(f"   Quantité : {quantite_actuelle}")
    
    print("\n" + "─" * 60)
    print("Nouvelles informations (appuyez sur Entrée pour conserver)")
    print("─" * 60)
    
    try:
        # Modification du nom
        nouveau_nom = input(f"Nouveau nom [{designation}] : ").strip()
        if not nouveau_nom:
            nouveau_nom = designation
        
        # Modification du prix
        nouveau_prix_input = input(f"Nouveau prix [{formater_prix(prix_actuel)}] : ").strip()
        if nouveau_prix_input:
            nouveau_prix = float(nouveau_prix_input)
            if nouveau_prix < 0:
                print("  Le prix ne peut pas être négatif. Valeur conservée.")
                nouveau_prix = prix_actuel
        else:
            nouveau_prix = prix_actuel
        
        # Modification de la quantité
        nouvelle_quantite_input = input(f"Nouvelle quantité [{quantite_actuelle}] : ").strip()
        if nouvelle_quantite_input:
            nouvelle_quantite = int(nouvelle_quantite_input)
            if nouvelle_quantite < 0:
                print("  La quantité ne peut pas être négative. Valeur conservée.")
                nouvelle_quantite = quantite_actuelle
        else:
            nouvelle_quantite = quantite_actuelle
            
        statut = 'Disponible' if nouvelle_quantite > 0 else 'En rupture'
        
        cursor.execute("""
            UPDATE Produits 
            SET designation = %s, prix = %s, quantite = %s, statut_produit = %s 
            WHERE id_produit = %s
        """, (nouveau_nom, nouveau_prix, nouvelle_quantite, statut, id_produit))
        
        boutique_gestion_systeme.commit()
        print("\n Produit modifié avec succès !")
        
    except ValueError:
        print(" Erreur : Valeurs invalides. Modification annulée.")
    except Exception as e:
        print(f" Erreur inattendue : {e}")

# Suppression d'un produit
def supprimer_produit():
    """Supprime un produit du stock"""
    cursor = boutique_gestion_systeme.cursor()
    print("\n" + "─" * 60)
    print("   SUPPRIMER UN PRODUIT")
    print("─" * 60)
    
    code = input("Code du produit à supprimer : ").strip().upper()
    cursor.execute("SELECT id_produit, designation, prix, quantite FROM Produits WHERE code_produit = %s", (code,))
    res = cursor.fetchone()
    
    resultat = res
    if not res:
        print(f" Aucun produit trouvé avec le code '{code}'.")
        return
  
    id_produit, designation, prix, quantite = resultat
    res =resultat
    print(f"\n Produit à supprimer :")
    print(f"   Code : {code}")
    print(f"   Nom : {designation}")
    print(f"   Prix : {formater_prix(prix)} F CFA")
    print(f"   Quantité : {quantite}")
    
    confirmation = input("\n  Êtes-vous sûr de vouloir supprimer ce produit ? (oui/non) : ").strip().lower()
    
    if confirmation in ['oui', 'o', 'yes', 'y']:
        cursor.execute("DELETE FROM Produits WHERE id_produit = %s", (id_produit,))
        boutique_gestion_systeme.commit()
        print(f" Produit '{designation}' supprimé avec succès !")
    else:
        print(" Suppression annulée.")

# Affichage de l'historique
def afficher_historique():
    cursor = boutique_gestion_systeme.cursor()
    cursor.execute("""
        SELECT m.date_mouvement, p.designation, m.nature_mouvement, m.quantite_mouv
        FROM Mouvements m JOIN Produits p ON m.id_produit = p.id_produit
        ORDER BY m.date_mouvement DESC
    """)
    rows = cursor.fetchall()
    print("\n--- HISTORIQUE DES MOUVEMENTS ---")
    for r in rows:
        print(f"[{r[0]}] {r[1]} | {r[2]} | Qté: {r[3]}")

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("    GESTION DE STOCK - BOUTIQUE")
        print("="*40)
        print("1. Ajouter une catégorie")
        print("2. Ajouter un produit")
        print("3. Afficher tous les produits")
        print("4. Lister tous les produits par catégorie")
        print("5. Vendre un produit")
        print("6. Modifier un produit")
        print("7. Supprimer un produit")
        print("8. Alertes stock faible")
        print("9. Historique des mouvements")
        print("0. Quitter")
        
        choix = input("\nVotre choix : ")
        if choix == '1': ajouter_categorie()
        elif choix == '2': ajouter_produit()
        elif choix == '3': afficher_tous_produits()
        elif choix == '4': lister_produits_par_categorie()
        elif choix == '5': vendre_produit()
        elif choix == '6': modifier_produit()
        elif choix == '7': supprimer_produit()
        elif choix == '8': afficher_alertes()
        elif choix == '9': afficher_historique()
        elif choix == '0': break
        else: print("Choix invalide !")

if __name__ == "__main__":
    menu_principal()