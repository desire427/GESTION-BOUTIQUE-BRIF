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

# Fonctions
def ajouter_categorie(nom):
    sql = "INSERT INTO CATEGORIES (nom_categorie) VALUES (%s)"
    cursor.execute(sql, (nom,))
    conn.commit()
    print(f"Categorie '{nom}' ajoutee.")

def lister_categories():
    cursor.execute("SELECT * FROM CATEGORIES")
    return cursor.fetchall()

def ajouter_produit(designation, prix, id_categorie):
    sql = """INSERT INTO PRODUITS (designation, prix, id_categorie) VALUES (%s, %s, %s)"""
    cursor.execute(sql, (designation, prix, id_categorie))
    conn.commit()
    print(f"Produit '{designation}' ajoute.")

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
    print(f"Mouvement de {quantite} unites enregistre.")

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


def menu_supprimer_categorie():
    print("\n--- SUPPRIMER UNE CATEGORIE ---")
    print("Categories existantes:")
    for cat in lister_categories():
        print(f"ID: {cat[0]} - {cat[1]}")
    
    while True:
        try:
            id_categorie = int(input("ID de la categorie a supprimer: "))
            break
        except ValueError:
            print("Valeur invalide")
    
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
    
    while True:
        try:
            id_produit = int(input("ID du produit a supprimer: "))
            break
        except ValueError:
            print("Valeur invalide")
    
    confirm = input(f"Confirmer la suppression du produit ID {id_produit}? (o/n): ")
    
    if confirm.lower() == 'o':
        supprimer_produit(id_produit)
    else:
        print("Suppression annulee.")


# SOUS-MENUS EXISTANTS
def menu_categories():
    while True:
        print("\n--- GESTION CATEGORIES ---")
        print("1. Ajouter une categorie")
        print("2. Lister toutes les categories")
        print("3. Supprimer une categorie")
        print("4. Retour")
        
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
            menu_supprimer_categorie()
        elif choix == "4":
            break
        else:
            print("Choix invalide!")

def menu_produits():
    while True:
        print("\n--- GESTION PRODUITS ---")
        print("1. Ajouter un produit")
        print("2. Supprimer un produit")
        print("3. Retour")
        
        choix = input("Choix: ")
        
        if choix == "1":
            designation = input("Designation: ")
            
            while True:
                try:
                    prix = float(input("Prix: "))
                    break
                except ValueError:
                    print("Valeur invalide")
            
            print("\nCategories disponibles:")
            for cat in lister_categories():
                print(f"{cat[0]}. {cat[1]}")
            
            while True:
                try:
                    id_categorie = int(input("ID de la categorie: "))
                    break
                except ValueError:
                    print("Valeur invalide")
            
            ajouter_produit(designation, prix, id_categorie)
        
        elif choix == "2":
            menu_supprimer_produit()
        
        elif choix == "3":
            break
        else:
            print("Choix invalide!")

def lister_tous_produits():
    cursor.execute("SELECT id, designation, stock_actuel FROM PRODUITS")
    return cursor.fetchall()

def lister_utilisateurs():
    cursor.execute("SELECT id_utilisateur, nom, prenom, role FROM UTILISATEURS")
    return cursor.fetchall()

def menu_mouvements():
    print("\n--- MOUVEMENT DE STOCK ---")

    print("\nProduits disponibles:")
    produits = lister_tous_produits()
    for p in produits:
        print(f"ID: {p[0]} | {p[1]} | Stock actuel: {p[2]}")

    while True:
        try:
            id_produit = int(input("ID du produit: "))
            break
        except ValueError:
            print("Valeur invalide")

    cursor.execute("SELECT stock_actuel FROM PRODUITS WHERE id = %s", (id_produit,))
    stock_avant = cursor.fetchone()[0]

    print("\nUtilisateurs disponibles:")
    utilisateurs = lister_utilisateurs()
    for u in utilisateurs:
        print(f"ID: {u[0]} | {u[1]} {u[2]} | Role: {u[3]}")

    while True:
        try:
            id_utilisateur = int(input("ID utilisateur: "))
            break
        except ValueError:
            print("Valeur invalide")

    print(f"Stock actuel avant mouvement: {stock_avant}")
    
    while True:
        try:
            quantite = int(input("Quantite (+ pour entree, - pour sortie): "))
            break
        except ValueError:
            print("Valeur invalide")

    mouvement_stock(id_produit, id_utilisateur, quantite)

    cursor.execute("SELECT stock_actuel FROM PRODUITS WHERE id = %s", (id_produit,))
    stock_apres = cursor.fetchone()[0]

    print(f"Quantite actuelle est de {stock_apres}")

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


# MENU PRINCIPAL
def menu():
    while True:
        print("\n" + "="*50)
        print("GESTION DE STOCK - MENU PRINCIPAL")
        print("="*50)
        print("1. Gestion des Categories")
        print("2. Gestion des Produits")
        print("3. Mouvement de Stock")
        print("4. Liste des produits avec categories")
        print("5. Alertes stock faible (<5 unites)")
        print("6. Historique des transactions")
        print("7. Quitter")
        print("-"*50)
        
        choix = input("Votre choix (1-7): ")
        
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
            print("Au revoir!")
            break
        else:
            print("Choix invalide!")


menu()
cursor.close()
conn.close()