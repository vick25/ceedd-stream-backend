# 🌍 STREAM – Sustainable Tools for Rainwater Evaluation And Management

STREAM est une application web de suivi et de gestion des **infrastructures de gestion des eaux pluviales** en milieu urbain.  
L’objectif est de fournir un outil cartographique interactif pour visualiser, analyser et mettre à jour les infrastructures telles que **citernes, bassins de rétention, puits perdus, barrages, végétation et zones contributives**.

---

## 🚀 Fonctionnalités principales (MVP)
- Carte interactive basée sur **OpenStreetMap + Leaflet**
- Affichage des infrastructures avec informations essentielles (photo, type, état, capacité, date de vérification)
- Tableau de bord simplifié : nombre total d’infrastructures, répartition par type, superficie végétalisée
- Interface d’administration sécurisée pour la mise à jour des données
- Base de données géospatiale avec **PostgreSQL + PostGIS**

---

## 🏗️ Architecture
- **Frontend** : React.js / Next.js + Leaflet  
- **Backend** : FastAPI (Python) ou AdonisJs (Node.js)  
- **Base de données** : PostgreSQL + PostGIS  
- **Stockage fichiers** : S3-compatible (photos, CSV, GeoJSON)  

![Architecture MVP](docs/architecture_mvp.png)

---

## 📦 Installation et exécution

### 1. Cloner le projet
```bash
git clone https://github.com/vick25/ceedd-stream-backend.git
cd ceedd-stream-backend
```

## 📄 Licence

Projet sous licence MIT – libre d’utilisation et de modification avec attribution.

## 👥 Auteurs

CEEDD – Centre d’Etudes Environnementales et de Développement Durable

---

## 🤝 Contributions

Les contributions communautaires sont les bienvenues. Veuillez consulter le fichier `CONTRIBUTING.md` pour plus de détails.
