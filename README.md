# Research Lab Agents

Système multi-agents pour la gestion d'un laboratoire de recherche.  
Construit avec **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL** et **Docker**.

---

## Architecture générale

Le système est composé de trois agents principaux :

| Agent | Rôle | Statut |
|---|---|---|
| **MIS** (Management Information System) | Gestion des données : projets, personnel, équipements, budgets | ✅ Phase 1 + 2 complètes |
| **Orchestrateur** | Coordination et routage des événements entre agents | 🔜 En cours |
| **Qualité** | Surveillance et évaluation de la qualité des données | 🔜 Planifié |

---

## Stack technique

- **FastAPI** — framework API async
- **SQLAlchemy 2.0** — ORM async (syntaxe `Mapped[]`)
- **asyncpg** — driver PostgreSQL asynchrone
- **PostgreSQL 16** — base de données relationnelle (via Docker)
- **Docker Desktop** — conteneurisation de la base de données
- **Pydantic v2** — validation des schémas API

---

## Prérequis

- Python 3.13+
- Docker Desktop (en cours d'exécution)
- Git

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/wassiLabsx/research-lab-agents.git
cd research-lab-agents
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer PostgreSQL via Docker

```bash
docker compose up -d
```

Vérifie que le conteneur tourne :

```bash
docker ps
# → mis_postgres  Up  0.0.0.0:5432->5432/tcp
```

### 5. Créer les tables SQL

```bash
python create_tables.py
```

### 6. Lancer le serveur

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Structure du projet
research-lab-agents/
├── app/
│   ├── agents/
│   │   └── mis_agent.py        # Agent MIS (logique métier + événements)
│   ├── core/
│   │   ├── base_agent.py       # Classe abstraite BaseAgent
│   │   └── event_bus.py        # EventBus + InMemoryEventBus
│   ├── models/
│   │   └── mis.py              # Modèles SQLAlchemy (tables SQL)
│   ├── routers/
│   │   └── mis.py              # 20 endpoints FastAPI (CRUD)
│   ├── schemas/
│   │   ├── events.py           # Schémas Pydantic : Event, AgentAction
│   │   └── mis.py              # Schémas Pydantic : Projet, Personnel, Equipement, Budget
│   ├── database.py             # Connexion SQLAlchemy async + session + Base
│   ├── main.py                 # Point d'entrée FastAPI + lifespan
│   └── state.py                # Instance partagée du MISAgent
├── docker-compose.yml          # PostgreSQL 16 + volume persistant
├── requirements.txt
├── test_base_agent.py
├── test_event_bus.py
└── README.md
---

## API — Endpoints disponibles

### Projets
| Méthode | Route | Description |
|---|---|---|
| `POST` | `/projets/` | Créer un projet |
| `GET` | `/projets/` | Lister tous les projets |
| `GET` | `/projets/{id}` | Obtenir un projet |
| `PUT` | `/projets/{id}` | Modifier un projet |
| `DELETE` | `/projets/{id}` | Supprimer un projet |

### Personnel
| Méthode | Route | Description |
|---|---|---|
| `POST` | `/personnels/` | Créer un membre |
| `GET` | `/personnels/` | Lister le personnel |
| `GET` | `/personnels/{id}` | Obtenir un membre |
| `PUT` | `/personnels/{id}` | Modifier un membre |
| `DELETE` | `/personnels/{id}` | Supprimer un membre |

### Équipements
| Méthode | Route | Description |
|---|---|---|
| `POST` | `/equipements/` | Créer un équipement |
| `GET` | `/equipements/` | Lister les équipements |
| `GET` | `/equipements/{id}` | Obtenir un équipement |
| `PUT` | `/equipements/{id}` | Modifier un équipement |
| `DELETE` | `/equipements/{id}` | Supprimer un équipement |

### Budgets
| Méthode | Route | Description |
|---|---|---|
| `POST` | `/budgets/` | Créer un budget |
| `GET` | `/budgets/` | Lister les budgets |
| `GET` | `/budgets/{id}` | Obtenir un budget |
| `PUT` | `/budgets/{id}` | Modifier un budget |
| `DELETE` | `/budgets/{id}` | Supprimer un budget |

---

## Base de données

| Paramètre | Valeur |
|---|---|
| Image | `postgres:16` |
| Conteneur | `mis_postgres` |
| Base | `mis_db` |
| Utilisateur | `mis_user` |
| Port | `5432` |
| Volume | `postgres_data` (persistant) |

> ⚠️ Les credentials dans `docker-compose.yml` sont pour le développement local uniquement.  
> En production, utiliser un fichier `.env` non versionné.

---

## Phases du projet

- ✅ **Phase 0** — Fondations : `BaseAgent`, `EventBus`, schémas Pydantic partagés
- ✅ **Phase 1** — MIS Agent : 20 endpoints CRUD, stockage en mémoire
- ✅ **Phase 2** — PostgreSQL : migration vers une vraie base de données persistante
- 🔜 **Phase 3** — Orchestrateur : agent de coordination inter-agents
- 🔜 **Phase 4** — Agent Qualité : surveillance et évaluation

---

## Auteur

**Wassi** — Projet d'internship / académique  
Stack : FastAPI · SQLAlchemy 2.0 · PostgreSQL · Docker · Python 3.13