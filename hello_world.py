import sqlite3
import pandas as pd
import os

db_path = 'data/inge.sqlite'

if os.path.exists(db_path):
    os.remove(db_path)
def creer_base_de_donnees():
    # Connexion à la base de données (si elle n'existe pas, elle sera créée)
    conn = sqlite3.connect(db_path)

    # Création d'un objet curseur
    curseur = conn.cursor()

    # Création d'une table exemple
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS Magasins (
            ID_Magasin INTEGER PRIMARY KEY,
            Ville VARCHAR(255),
            Nombre_de_salarie INTEGER
        )""")
    
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS Produits (
            Nom VARCHAR(255),
            ID_Reference_produit VARCHAR(255) PRIMARY KEY,
            Prix FLOAT,
            Stock INTEGER
        )""")

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS Ventes (
            Date DATE,
            ID_Reference_produit VARCHAR(255),
            Quantite INTEGER,
            ID_Magasin INTEGER,
            FOREIGN KEY (ID_Reference_produit) REFERENCES Produits (ID_Reference_produit),
            FOREIGN KEY (ID_Magasin) REFERENCES Magasins (ID_Magasin)
        )""")

    curseur.execute("""
        INSERT INTO Magasins (ID_Magasin, Ville, Nombre_de_salarie) VALUES
        (1, 'Paris', 10),
        (2, 'Marseille', 5),
        (3, 'Lyon', 8),
        (4, 'Bordeaux', 12),
        (5, 'Lille', 6),
        (6, 'Nantes', 7),
        (7, 'Strasbourg', 9)
        """)
    
    curseur.execute("""
        INSERT INTO Produits (Nom, ID_Reference_produit, Prix, Stock) VALUES
        ('Produit A', 'REF001', 49.99, 100),
        ('Produit B', 'REF002', 19.99, 50),
        ('Produit C', 'REF003', 29.99, 75),
        ('Produit D', 'REF004', 79.99, 120),
        ('Produit E', 'REF005', 39.99, 80)
        """)
    
    curseur.execute("""
        INSERT INTO Ventes (Date, ID_Reference_produit, Quantite, ID_Magasin) VALUES
        ('2023-05-27', 'REF001', 5, 1),
        ('2023-05-28', 'REF002', 3, 2),
        ('2023-05-29', 'REF003', 2, 1),
        ('2023-05-30', 'REF004', 4, 3),
        ('2023-05-31', 'REF005', 7, 2),
        ('2023-06-01', 'REF001', 3, 4),
        ('2023-06-02', 'REF002', 6, 1),
        ('2023-06-03', 'REF003', 1, 5),
        ('2023-06-04', 'REF004', 2, 3),
        ('2023-06-05', 'REF005', 5, 6),
        ('2023-06-06', 'REF001', 4, 7),
        ('2023-06-07', 'REF002', 3, 2),
        ('2023-06-08', 'REF003', 6, 4),
        ('2023-06-09', 'REF004', 2, 1),
        ('2023-06-10', 'REF005', 8, 3),
        ('2023-06-11', 'REF001', 3, 2),
        ('2023-06-12', 'REF002', 5, 4),
        ('2023-06-13', 'REF003', 2, 5),
        ('2023-06-14', 'REF004', 4, 7),
        ('2023-06-15', 'REF005', 6, 6),
        ('2023-06-16', 'REF001', 3, 1),
        ('2023-06-17', 'REF002', 7, 2),
        ('2023-06-18', 'REF003', 2, 3),
        ('2023-06-19', 'REF004', 5, 4),
        ('2023-06-20', 'REF005', 4, 5),
        ('2023-06-21', 'REF001', 6, 6),
        ('2023-06-22', 'REF002', 3, 7),
        ('2023-06-23', 'REF003', 2, 1),
        ('2023-06-24', 'REF004', 4, 2),
        ('2023-06-25', 'REF005', 5, 3)
        """)    


    # Commit pour sauvegarder les modifications
    conn.commit()

    # Fermeture de la connexion
    conn.close()

def analysis(db_path):
    conn = sqlite3.connect(db_path)
    

    # Exemple d'analyse SQL : Chiffre d'affaires total
    query_ca = '''
        SELECT SUM(Quantite * Prix) AS Chiffre_affaires_total
        FROM Ventes
        JOIN Produits ON Ventes.ID_Reference_produit = Produits.ID_Reference_produit;
    '''
    chiffre_affaires_total = pd.read_sql_query(query_ca, conn)

    # Exemple d'analyse SQL : Ventes par produit
    query_ventes_produit = '''
        SELECT Nom, SUM(Quantite) AS Total_Ventes
        FROM Ventes
        JOIN Produits ON Ventes.ID_Reference_produit = Produits.ID_Reference_produit
        GROUP BY Nom;
    '''
    ventes_par_produit = pd.read_sql_query(query_ventes_produit, conn)

    # Exemple d'analyse SQL : Ventes par région
    query_ventes_region = '''
        SELECT Ville, SUM(Quantite) AS Total_Ventes
        FROM Ventes
        JOIN Magasins ON Ventes.ID_Magasin = Magasins.ID_Magasin
        GROUP BY Ville;
    '''
    ventes_par_region = pd.read_sql_query(query_ventes_region, conn)

    # Affichage des résultats
    print("Chiffre d'affaires total:")
    print(chiffre_affaires_total)

    print("\nVentes par produit:")
    print(ventes_par_produit)

    print("\nVentes par région:")
    print(ventes_par_region)

    # Fermer la connexion
    conn.close()
    
if __name__ == "__main__":
    # Appel de la fonction pour créer la base de données
    creer_base_de_donnees()
    analysis(db_path)
