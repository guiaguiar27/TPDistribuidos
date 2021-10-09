-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: albumdb
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `album`
--

DROP TABLE IF EXISTS `album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quantityCards` int DEFAULT NULL,
  `quantityStickeredCards` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album`
--

LOCK TABLES `album` WRITE;
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
INSERT INTO `album` VALUES (1,0,0),(2,0,0),(10,0,0),(11,0,0),(12,0,0),(13,0,0),(14,0,0),(15,0,0),(16,0,0),(17,0,0),(18,0,0),(19,0,0),(20,0,0),(21,0,0),(22,0,0),(23,0,0),(24,0,0);
/*!40000 ALTER TABLE `album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `picture` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card`
--

LOCK TABLES `card` WRITE;
/*!40000 ALTER TABLE `card` DISABLE KEYS */;
INSERT INTO `card` VALUES (1,'fogo','carta de fogo',NULL),(2,'agua','carta de agua',NULL),(3,'terra','terra terra',NULL),(4,'Stark','Seated in Winterfell.',NULL),(5,'Lannister','House Lannister is seated at Casterly Rock .',NULL),(6,'Baratheon','The principle house of the Stormlands.',NULL),(7,'Targaryen','Originally from Valyria.',NULL),(8,'Greyjoy','Seated in Pyke in the Iron Islands.',NULL),(9,'Arryn','The principle house in the Vale .',NULL),(10,'Martell','Seated at Sunspear Castle in Dorne.',NULL),(11,'Tully','Is seated at Riverrun in the Riverlands.',NULL),(12,'Tyrell','The principle house in the Reach.',NULL);
/*!40000 ALTER TABLE `card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collection_cards`
--

DROP TABLE IF EXISTS `collection_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collection_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idAlbum` int NOT NULL,
  `idCard` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_CardsCollection_idx` (`idCard`),
  KEY `fk_CardsCollection_idx1` (`idAlbum`),
  CONSTRAINT `fk_CardsCollection_Album` FOREIGN KEY (`idAlbum`) REFERENCES `album` (`id`),
  CONSTRAINT `fk_CardsCollection_Card` FOREIGN KEY (`idCard`) REFERENCES `card` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collection_cards`
--

LOCK TABLES `collection_cards` WRITE;
/*!40000 ALTER TABLE `collection_cards` DISABLE KEYS */;
INSERT INTO `collection_cards` VALUES (1,1,1),(2,1,2),(3,1,8),(4,1,7),(5,1,4),(6,1,5),(7,1,9),(8,1,11),(9,1,3),(10,1,10);
/*!40000 ALTER TABLE `collection_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collector`
--

DROP TABLE IF EXISTS `collector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collector` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `coins` float DEFAULT NULL,
  `idAlbum` int NOT NULL,
  `accessFrequency` int DEFAULT '0',
  `lastConnection` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_Collector_Album2_idx` (`idAlbum`),
  CONSTRAINT `fk_Collector_Album2` FOREIGN KEY (`idAlbum`) REFERENCES `album` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collector`
--

LOCK TABLES `collector` WRITE;
/*!40000 ALTER TABLE `collector` DISABLE KEYS */;
INSERT INTO `collector` VALUES (2,'Guilherme Aguiar','guilezim@guile.com','123guile123',342,1,0,'2021-09-19 03:00:00'),(3,'Arthur Lenda','arthur@lendario.com','descontoemmoveis',50,2,0,'2021-09-19 23:10:38'),(9,'lucas','teste@','123',12,10,1,'2021-09-18 03:00:00'),(21,'sw3luke','luke@luke.com','123luke',50,22,0,'2021-10-02 18:56:00'),(22,'teste','teste@teste123.com','123',10,23,0,'2021-10-06 22:23:22'),(23,'guileguile','guile@guileguile','123',10,24,0,'2021-10-08 20:49:59');
/*!40000 ALTER TABLE `collector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchanges`
--

DROP TABLE IF EXISTS `exchanges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchanges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCollectorOwner` int NOT NULL,
  `idCollectorTarget` int NOT NULL,
  `idCard` int NOT NULL,
  `idCardReceived` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idCard` (`idCard`),
  KEY `idCardReceived` (`idCardReceived`),
  KEY `idCollectorOwner` (`idCollectorOwner`),
  KEY `idCollectorTarget` (`idCollectorTarget`),
  CONSTRAINT `exchanges_ibfk_1` FOREIGN KEY (`idCard`) REFERENCES `card` (`id`),
  CONSTRAINT `exchanges_ibfk_2` FOREIGN KEY (`idCardReceived`) REFERENCES `card` (`id`),
  CONSTRAINT `exchanges_ibfk_3` FOREIGN KEY (`idCollectorOwner`) REFERENCES `collector` (`id`),
  CONSTRAINT `exchanges_ibfk_4` FOREIGN KEY (`idCollectorTarget`) REFERENCES `collector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchanges`
--

LOCK TABLES `exchanges` WRITE;
/*!40000 ALTER TABLE `exchanges` DISABLE KEYS */;
INSERT INTO `exchanges` VALUES (5,2,22,8,9);
/*!40000 ALTER TABLE `exchanges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_cards`
--

DROP TABLE IF EXISTS `inventory_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCard` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `idCollector` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Inventory_Cards_idx` (`idCard`),
  KEY `fk_Inventory_Cards_Collector1_idx` (`idCollector`),
  CONSTRAINT `fk_Inventory_Cards` FOREIGN KEY (`idCard`) REFERENCES `card` (`id`),
  CONSTRAINT `fk_Inventory_Cards_Collector1` FOREIGN KEY (`idCollector`) REFERENCES `collector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_cards`
--

LOCK TABLES `inventory_cards` WRITE;
/*!40000 ALTER TABLE `inventory_cards` DISABLE KEYS */;
INSERT INTO `inventory_cards` VALUES (1,1,11,2),(5,2,6,2),(12,3,4,2),(18,1,6,21),(21,3,2,2),(27,8,1,21),(28,11,2,21),(31,5,3,2),(32,3,2,21),(33,7,1,21);
/*!40000 ALTER TABLE `inventory_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_cards`
--

DROP TABLE IF EXISTS `store_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `price` float DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `idCollector` int DEFAULT NULL,
  `idCards` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Store_idCollector_idx` (`idCollector`),
  KEY `fk_Store_Cards_Card1_idx` (`idCards`),
  CONSTRAINT `fk_Store_Cards_Card1` FOREIGN KEY (`idCards`) REFERENCES `card` (`id`),
  CONSTRAINT `fk_Store_idCollector` FOREIGN KEY (`idCollector`) REFERENCES `collector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_cards`
--

LOCK TABLES `store_cards` WRITE;
/*!40000 ALTER TABLE `store_cards` DISABLE KEYS */;
INSERT INTO `store_cards` VALUES (5,4,NULL,NULL,NULL,5);
/*!40000 ALTER TABLE `store_cards` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-08 23:11:44
