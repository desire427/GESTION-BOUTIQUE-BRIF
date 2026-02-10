-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: GESTION_BOUTIQUE
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CATEGORIES`
--

DROP TABLE IF EXISTS `CATEGORIES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CATEGORIES` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_categorie` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom_categorie` (`nom_categorie`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CATEGORIES`
--

LOCK TABLES `CATEGORIES` WRITE;
/*!40000 ALTER TABLE `CATEGORIES` DISABLE KEYS */;
INSERT INTO `CATEGORIES` VALUES (5,'Connectique'),(1,'Informatique'),(3,'Mobilier'),(2,'Papeterie'),(4,'Périphériques');
/*!40000 ALTER TABLE `CATEGORIES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUITS`
--

DROP TABLE IF EXISTS `PRODUITS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUITS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `designation` varchar(200) NOT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `stock_actuel` int DEFAULT '0',
  `seuil_alerte` int DEFAULT '5',
  `en_rupture` tinyint(1) DEFAULT '0',
  `id_categorie` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_categorie` (`id_categorie`),
  CONSTRAINT `PRODUITS_ibfk_1` FOREIGN KEY (`id_categorie`) REFERENCES `CATEGORIES` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUITS`
--

LOCK TABLES `PRODUITS` WRITE;
/*!40000 ALTER TABLE `PRODUITS` DISABLE KEYS */;
INSERT INTO `PRODUITS` VALUES (1,'Ordinateur portable HP',450000.00,18,3,0,1),(2,'Clavier français',25000.00,7,5,0,1),(3,'Souris optique',15000.00,3,5,0,4),(4,'Cahier 100 pages',1500.00,4,20,1,2),(5,'Chaise bureau',75000.00,15,2,0,3),(6,'Écran LED 22\"',120000.00,6,3,0,1),(7,'Câble USB 3.0',5000.00,30,10,0,5),(8,'Rame papier A4',3500.00,4,15,0,2),(9,'Casque avec micro',35000.00,8,5,0,4),(10,'Table réunion',200000.00,5,2,0,3),(11,'Ordinateur portable Dell',650000.00,10,3,0,1),(12,'assessoir electique',13000.00,-10,5,0,4);
/*!40000 ALTER TABLE `PRODUITS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRANSACTIONS`
--

DROP TABLE IF EXISTS `TRANSACTIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TRANSACTIONS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_produit` int NOT NULL,
  `id_utilisateur` int NOT NULL,
  `quantite` int NOT NULL,
  `type_mouvement` enum('ENTREE','SORTIE') NOT NULL DEFAULT 'ENTREE',
  `date_mouvement` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_produit` (`id_produit`),
  KEY `id_utilisateur` (`id_utilisateur`),
  CONSTRAINT `TRANSACTIONS_ibfk_1` FOREIGN KEY (`id_produit`) REFERENCES `PRODUITS` (`id`) ON DELETE CASCADE,
  CONSTRAINT `TRANSACTIONS_ibfk_2` FOREIGN KEY (`id_utilisateur`) REFERENCES `UTILISATEURS` (`id_utilisateur`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRANSACTIONS`
--

LOCK TABLES `TRANSACTIONS` WRITE;
/*!40000 ALTER TABLE `TRANSACTIONS` DISABLE KEYS */;
INSERT INTO `TRANSACTIONS` VALUES (1,1,1,10,'ENTREE','2024-01-10'),(2,1,2,-2,'SORTIE','2024-01-11'),(3,2,3,20,'ENTREE','2024-01-12'),(4,2,4,-8,'SORTIE','2024-01-13'),(5,3,5,15,'ENTREE','2024-01-14'),(6,3,1,-12,'SORTIE','2024-01-15'),(7,4,2,50,'ENTREE','2024-01-16'),(8,4,3,-50,'SORTIE','2024-01-17'),(9,5,4,10,'ENTREE','2024-01-18'),(10,5,5,-3,'SORTIE','2024-01-19'),(11,6,1,8,'ENTREE','2024-01-20'),(12,6,2,-2,'SORTIE','2024-01-21'),(13,7,3,25,'ENTREE','2024-01-22'),(14,7,4,-10,'SORTIE','2024-01-23'),(15,8,5,20,'ENTREE','2024-01-24'),(16,8,1,-16,'SORTIE','2024-01-25'),(17,9,2,5,'ENTREE','2024-01-26'),(18,9,3,-3,'SORTIE','2024-01-27'),(19,10,4,6,'ENTREE','2024-01-28'),(20,10,5,-1,'SORTIE','2024-01-29'),(21,1,1,10,'ENTREE','2026-02-09'),(22,2,1,-5,'SORTIE','2026-02-09'),(23,12,1,-10,'SORTIE','2026-02-10'),(24,4,1,4,'ENTREE','2026-02-10'),(25,9,2,6,'ENTREE','2026-02-10');
/*!40000 ALTER TABLE `TRANSACTIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UTILISATEURS`
--

DROP TABLE IF EXISTS `UTILISATEURS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UTILISATEURS` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) NOT NULL,
  `prenom` varchar(20) NOT NULL,
  `role` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  PRIMARY KEY (`id_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UTILISATEURS`
--

LOCK TABLES `UTILISATEURS` WRITE;
/*!40000 ALTER TABLE `UTILISATEURS` DISABLE KEYS */;
INSERT INTO `UTILISATEURS` VALUES (1,'Ndiaye','Fatou','Administrateur','f.ndiaye@boutique.sn','771234567'),(2,'Diop','Mamadou','Gestionnaire','m.diop@boutique.sn','772345678'),(3,'Sow','Aïssatou','Responsable','a.sow@boutique.sn','773456789'),(4,'Fall','Ousmane','Stagiaire','o.fall@boutique.sn','774567890'),(5,'Gueye','Khadija','Bénévole','k.gueye@boutique.sn','775678901');
/*!40000 ALTER TABLE `UTILISATEURS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-10 13:04:53
