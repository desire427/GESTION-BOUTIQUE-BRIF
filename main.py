import mysql.connector
from datetime import date

# Connexion
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Desire@17",
    database="GESTION_BOUTIQUE"
)
cursor = conn.cursor()

# Fonctions existantes
def ajouter_categorie(nom):
    sql = "INSERT INTO CATEGORIES (nom_categorie) VALUES (%s)"
    cursor.execute(sql, (nom,))
    conn.commit()
    print(f"OK Categorie '{nom}' ajoutee.")

def lister_categories():
    cursor.execute("SELECT * FROM CATEGORIES")
    return cursor.fetchall()

def ajouter_produit(designation, prix, id_categorie):
    sql = """INSERT INTO PRODUITS (designation, prix, id_categorie) VALUES (%s, %s, %s)"""
    cursor.execute(sql, (designation, prix, id_categorie))
    conn.commit()
    print(f"OK Produit '{designation}' ajoute.")

def mouvement_stock(id_produit, id_utilisateur, quantite):
    type_mvt = 'ENTREE' if quantite > 0 else 'SORTIE'
    sql_transaction = """INSERT INTO TRANSACTIONS (id_produit, id_utilisateur, quantite, type_mouvement, date_mouvement) 
                         VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql_transaction, (id_produit, id_utilisateur, quantite, type_mvt, date.today()))
    
    if quantite > 0:
        sql_update = "UPDATE PRODUITS SET stock_actuel = stock_actuel + %s WHERE id = %s"
    else:
        sql_update = "UPDATE PRODUITS SET stock_actuel = stock_actuel - %s WHERE id = %s"
    
    cursor.execute(sql_update, (abs(quantite), id_produit))
    conn.commit()
    print(f"OK Mouvement de {quantite} unites enregistre.")

def lister_produits_categorie():
    sql = """SELECT p.id, p.designation, p.prix, p.stock_actuel, c.nom_categorie 
             FROM PRODUITS p JOIN CATEGORIES c ON p.id_categorie = c.id"""
    cursor.execute(sql)
    return cursor.fetchall()

def alerte_stock_faible():
    sql = "SELECT * FROM PRODUITS WHERE stock_actuel < 5"
    cursor.execute(sql)
    return cursor.fetchall()

def supprimer_categorie(id_categorie):
    sql = "DELETE FROM CATEGORIES WHERE id = %s"
    cursor.execute(sql, (id_categorie,))
    conn.commit()
    print(f"OK Categorie ID {id_categorie} supprimee.")

def supprimer_produit(id_produit):
    sql = "DELETE FROM PRODUITS WHERE id = %s"
    cursor.execute(sql, (id_produit,))
    conn.commit()
    print(f"OK Produit ID {id_produit} supprime.")

def historique_transactions_total():
    sql = """SELECT t.date_mouvement, p.designation, t.quantite, t.type_mouvement, u.nom, u.prenom
             FROM TRANSACTIONS t
             JOIN PRODUITS p ON t.id_produit = p.id
             JOIN UTILISATEURS u ON t.id_utilisateur = u.id_utilisateur
             ORDER BY t.date_mouvement DESC"""
    cursor.execute(sql)
    return cursor.fetchall()

def historique_entrees():
    sql = """SELECT t.date_mouvement, p.designation, t.quantite, u.nom, u.prenom
             FROM TRANSACTIONS t
             JOIN PRODUITS p ON t.id_produit = p.id
             JOIN UTILISATEURS u ON t.id_utilisateur = u.id_utilisateur
             WHERE t.type_mouvement = 'ENTREE'
             ORDER BY t.date_mouvement DESC"""
    cursor.execute(sql)
    return cursor.fetchall()

def historique_sorties():
    sql = """SELECT t.date_mouvement, p.designation, t.quantite, u.nom, u.prenom
             FROM TRANSACTIONS t
             JOIN PRODUITS p ON t.id_produit = p.id
             JOIN UTILISATEURS u ON t.id_utilisateur = u.id_utilisateur
             WHERE t.type_mouvement = 'SORTIE'
             ORDER BY t.date_mouvement DESC"""
    cursor.execute(sql)
    return cursor.fetchall()

# MENU PRINCIPAL
def menu():
    while True:
        print("\n" + "="*50)
        print("GESTION DE STOCK - MENU PRINCIPAL")
        print("="*50)
        print("1. Gestion des Categories")
        print("2. Catalogue Produits")
        print("3. Mouvement de Stock")
        print("4. Liste des produits avec categories")
        print("5. Alertes stock faible (<5 unites)")
        print("6. Historique des transactions")
        print("7. Supprimer une categorie")
        print("8. Supprimer un produit")
        print("9. Quitter")
        print("-"*50)
        
        choix = input("Votre choix (1-9): ")
        
        if choix == "1":
            menu_categories()
        elif choix == "2":
            menu_produits()
        elif choix == "3":
            menu_mouvements()
        elif choix == "4":
            menu_liste_produits()
        elif choix == "5":
            menu_alertes()
        elif choix == "6":
            menu_historique()
        elif choix == "7":
            menu_supprimer_categorie()
        elif choix == "8":
            menu_supprimer_produit()
        elif choix == "9":
            print("Au revoir!")
            break
        else:
            print("Choix invalide!")

# SOUS-MENUS EXISTANTS
def menu_categories():
    while True:
        print("\n--- GESTION CATEGORIES ---")
        print("1. Ajouter une categorie")
        print("2. Lister toutes les categories")
        print("3. Retour au menu principal")
        
        choix = input("Choix: ")
        
        if choix == "1":
            nom = input("Nom de la categorie: ")
            ajouter_categorie(nom)
        elif choix == "2":
            categories = lister_categories()
            print("\nListe des categories:")
            for cat in categories:
                print(f"ID: {cat[0]} - {cat[1]}")
        elif choix == "3":
            break

def menu_produits():
    print("\n--- AJOUTER UN PRODUIT ---")
    designation = input("Designation: ")
    prix = float(input("Prix: "))
    
    print("\nCategories disponibles:")
    for cat in lister_categories():
        print(f"{cat[0]}. {cat[1]}")
    
    id_categorie = int(input("ID de la categorie: "))
    ajouter_produit(designation, prix, id_categorie)

def menu_mouvements():
    print("\n--- MOUVEMENT DE STOCK ---")
    id_produit = int(input("ID du produit: "))
    id_utilisateur = int(input("ID utilisateur: "))
    quantite = int(input("Quantite (+ pour entree, - pour sortie): "))
    mouvement_stock(id_produit, id_utilisateur, quantite)

def menu_liste_produits():
    produits = lister_produits_categorie()
    print("\n--- PRODUITS AVEC CATEGORIES ---")
    for p in produits:
        print(f"ID: {p[0]} | {p[1]} | Prix: {p[2]} | Stock: {p[3]} | Categorie: {p[4]}")

def menu_alertes():
    alertes = alerte_stock_faible()
    print("\nALERTES - STOCK FAIBLE (<5 unites)")
    if alertes:
        for a in alertes:
            print(f"ID: {a[0]} | {a[1]} | Stock: {a[3]}")
    else:
        print("Aucun produit en stock faible.")

# NOUVEAUX SOUS-MENUS
def menu_historique():
    while True:
        print("\n--- HISTORIQUE DES TRANSACTIONS ---")
        print("1. Toutes les transactions")
        print("2. Seulement les entrees")
        print("3. Seulement les sorties")
        print("4. Retour")
        
        choix = input("Choix: ")
        
        if choix == "1":
            transactions = historique_transactions_total()
            print("\n--- TOUTES LES TRANSACTIONS ---")
            for t in transactions:
                print(f"Date: {t[0]} | Produit: {t[1]} | Quantite: {t[2]} | Type: {t[3]} | Par: {t[5]} {t[4]}")
        
        elif choix == "2":
            entrees = historique_entrees()
            print("\n--- ENTREES DE STOCK ---")
            for e in entrees:
                print(f"Date: {e[0]} | Produit: {e[1]} | Quantite: {e[2]} | Par: {e[4]} {e[3]}")
        
        elif choix == "3":
            sorties = historique_sorties()
            print("\n--- SORTIES DE STOCK ---")
            for s in sorties:
                print(f"Date: {s[0]} | Produit: {s[1]} | Quantite: {s[2]} | Par: {s[4]} {s[3]}")
        
        elif choix == "4":
            break

def menu_supprimer_categorie():
    print("\n--- SUPPRIMER UNE CATEGORIE ---")
    print("Categories existantes:")
    for cat in lister_categories():
        print(f"ID: {cat[0]} - {cat[1]}")
    
    id_categorie = int(input("ID de la categorie a supprimer: "))
    confirm = input(f"Confirmer la suppression de la categorie ID {id_categorie}? (o/n): ")
    
    if confirm.lower() == 'o':
        supprimer_categorie(id_categorie)
    else:
        print("Suppression annulee.")

def menu_supprimer_produit():
    print("\n--- SUPPRIMER UN PRODUIT ---")
    produits = lister_produits_categorie()
    print("Produits existants:")
    for p in produits:
        print(f"ID: {p[0]} - {p[1]} | Categorie: {p[4]}")
    
    id_produit = int(input("ID du produit a supprimer: "))
    confirm = input(f"Confirmer la suppression du produit ID {id_produit}? (o/n): ")
    
    if confirm.lower() == 'o':
        supprimer_produit(id_produit)
    else:
        print("Suppression annulee.")

# Lancer l'application
menu()
cursor.close()
conn.close()