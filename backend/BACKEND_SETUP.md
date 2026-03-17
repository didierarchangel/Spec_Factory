# 💻 Backend - Setup Complet

Ce dossier contient le backend de votre application. La configuration varie selon la base de données sélectionnée lors de `speckit init`.

---

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```bash
npm install
```

### 2. Configuration de l'environnement

```bash
# Vérifier/modifier le fichier .env
cat .env

# Les valeurs à adapter selon votre BD:
# - MongoDB: MONGODB_URI
# - PostgreSQL: DATABASE_URL, DB_PASSWORD
# - Supabase: DATABASE_URL, SUPABASE_PROJECT_ID, SUPABASE_API_KEY
```

### 3. Initialiser la base de données (PostgreSQL/Supabase uniquement)

```bash
# Générer le client Prisma
npm run prisma:generate

# Créer la première migration
npm run prisma:migrate

# (Optionnel) Visualiser la BD
npm run prisma:studio
```

### 4. Démarrer le serveur

```bash
# Développement (avec hot-reload)
npm run dev

# Production
npm run build
npm run start
```

---

## 📦 Structure du Projet

```
backend/
├── src/
│   ├── app.ts              # Application Express principale
│   ├── routes/             # Routes API
│   ├── controllers/         # Contrôleurs métier
│   ├── services/           # Services (logique métier)
│   ├── models/             # Modèles (Mongoose ou Prisma schemas)
│   ├── middlewares/        # Middlewares Express
│   ├── utils/              # Utilitaires
│   └── types/              # Types TypeScript
├── prisma/                 # (PostgreSQL/Supabase seulement)
│   ├── schema.prisma       # Schéma Prisma
│   └── migrations/         # Fichiers de migration
├── tests/
│   ├── unit/              # Tests unitaires
│   └── integration/       # Tests d'intégration
├── .env                    # Variables d'environnement (NE PAS VERSIONNER)
├── .env.example            # Template .env
├── package.json            # Dépendances et scripts
├── tsconfig.json           # Configuration TypeScript
└── jest.config.js          # Configuration des tests
```

---

## 🗄️ Configuration selon la Base de Données

### MongoDB

**BD sélectionnée lors de `speckit init`**

```javascript
// Connexion MongoDB avec Mongoose
import mongoose from 'mongoose'

await mongoose.connect(process.env.MONGODB_URI!)

// Créer un schéma
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  name: String,
  password: String
})

const User = mongoose.model('User', userSchema)

// Utiliser
const user = await User.create({ email: 'test@example.com' })
```

**Variables .env requises** :
```env
MONGODB_URI=mongodb://localhost:27017/mon_projet
JWT_SECRET=votre_secret
NODE_ENV=development
```

**Installation de la BD** :
```bash
# Docker
docker run -d -p 27017:27017 --name mongodb mongo

# OU directement
# Windows: https://www.mongodb.com/try/download/community
# macOS: brew tap mongodb/brew && brew install mongodb-community
# Linux: https://docs.mongodb.com/manual/administration/install-on-linux/
```

---

### PostgreSQL Local

**BD sélectionnée lors de `speckit init`**

```javascript
// Utiliser Prisma
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Créer un utilisateur
const user = await prisma.user.create({
  data: {
    email: 'test@example.com',
    name: 'Test User'
  }
})

// Récupérer les données
const users = await prisma.user.findMany()

// Fermer la connexion
await prisma.$disconnect()
```

**Variables .env requises** :
```env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/drugstoredb
DATABASE_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=PASSWORD
DB_NAME=drugstoredb
JWT_SECRET=votre_secret
NODE_ENV=development
```

**Installation de la BD** :
```bash
# Docker (recommandé)
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=PASSWORD \
  -e POSTGRES_DB=drugstoredb \
  --name postgres postgres:15

# OU directement
# Windows: https://www.postgresql.org/download/windows/
# macOS: brew install postgresql@15
# Linux: sudo apt-get install postgresql postgresql-contrib

# Créer la base de données
createdb -U postgres drugstoredb

# Vérifier la connexion
psql -U postgres -h localhost -d drugstoredb
```

**Scripts Prisma** :
```bash
npm run prisma:generate   # Générer le client
npm run prisma:migrate    # Créer des migrations
npm run prisma:studio     # Visualiser la BD (GUI)
```

---

### Supabase (PostgreSQL Cloud)

**BD sélectionnée lors de `speckit init`**

```javascript
// Même approche que PostgreSQL Local
// La différence : la BD est sur le cloud Supabase
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const user = await prisma.user.create({
  data: { email: 'test@example.com' }
})

// Supabase inclut également :
// - Authentication
// - Real-time subscriptions
// - Storage (fichiers)
```

**Variables .env requises** :
```env
DATABASE_URL=postgresql://postgres.PROJECT_ID:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres
SUPABASE_PROJECT_ID=PROJECT_ID
SUPABASE_API_KEY=votre_cle_api
SUPABASE_URL=https://PROJECT_ID.supabase.co
JWT_SECRET=votre_secret
NODE_ENV=production
```

**Setup Supabase** :
```bash
# 1. Créer un compte : https://app.supabase.com
# 2. Créer un nouveau projet
# 3. Copier les credentials depuis Project Settings
# 4. Remplir le .env

# Vérifier la connexion
npm run prisma:generate
npm run prisma:migrate
```

---

## 📝 Scripts npm disponibles

| Script | Description | Disponible pour |
|--------|-------------|-----------------|
| `npm run dev` | Démarrer en développement avec hot-reload | Tous (Node.js) |
| `npm run build` | Compiler TypeScript en JavaScript | Tous |
| `npm run start` | Démarrer le serveur compilé | Tous |
| `npm run prisma:generate` | Générer le client Prisma | PostgreSQL, Supabase |
| `npm run prisma:migrate` | Créer/appliquer les migrations | PostgreSQL, Supabase |
| `npm run prisma:studio` | Ouvrir Prisma Studio (GUI) | PostgreSQL, Supabase |
| `npm run lint` | Vérifier le code avec ESLint | Tous |
| `npm run format` | Formater le code avec Prettier | Tous |
| `npm run test` | Exécuter les tests Jest | Tous |

---

## 🔐 Authentification JWT

```typescript
// Middleware d'authentification
import jwt from 'jsonwebtoken'

const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  
  if (!token) {
    return res.status(401).json({ error: 'No token' })
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!)
    req.user = decoded
    next()
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' })
  }
}

// Créer un token
const token = jwt.sign(
  { id: user.id, email: user.email },
  process.env.JWT_SECRET!,
  { expiresIn: '7d' }
)
```

---

## 🧪 Tests

```bash
# Exécuter tous les tests
npm run test

# Mode watch
npm run test -- --watch

# Avec couverture
npm run test -- --coverage
```

---

## ✅ Checklist de Setup

- [ ] `npm install` - Dépendances installées
- [ ] `.env` configuré avec les bonnes credentials
- [ ] Base de données créée et accessible
- [ ] (PostgreSQL/Supabase) : `npm run prisma:generate` exécuté
- [ ] (PostgreSQL/Supabase) : `npm run prisma:migrate` exécuté
- [ ] `npm run dev` démarre sans erreur
- [ ] Vérifier les endpoints avec Postman/Thunder Client
- [ ] `npm run test` passe tous les tests

---

## 🆘 Dépannage

### Erreur de connexion à la BD

```bash
# MongoDB
# Vérifier que MongoDB est en cours d'exécution
mongod --version

# PostgreSQL
# Vérifier la connexion
psql -U postgres -h localhost -d drugstoredb

# Supabase
# Vérifier les credentials dans le dashboard
```

### Erreur Prisma

```bash
# Régénérer le client Prisma
npm run prisma:generate

# Réappliquer les migrations
npm run prisma:migrate
```

### Port déjà utilisé

```bash
# Changer le port dans .env ou src/app.ts
# Exemple : PORT=5001
```

---

## 📚 Ressources

- **Express.js** : https://expressjs.com
- **TypeScript** : https://www.typescriptlang.org
- **Prisma** : https://www.prisma.io
- **Mongoose** : https://mongoosejs.com
- **JWT** : https://jwt.io
- **bcryptjs** : https://github.com/dcodeIO/bcrypt.js

---

**Créé**: Mars 2026  
**Dernière mise à jour**: Mars 17, 2026
**Version**: 1.0
