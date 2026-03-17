# 🗄️ Configuration des Bases de Données - Guide Interactif

Ce document décrit comment Speckit.Factory configure automatiquement votre backend selon la base de données sélectionnée.

---

## 📊 Sélection automatique lors de `speckit init`

Lors de l'initialisation, vous avez le choix entre 3 bases de données :

### 1️⃣ MongoDB (NoSQL Document-based)
```
Sélection : 1) MongoDB (NoSQL - Flexible)
```

**Dépendances installées** :
- `mongoose` (^8.0.0) - ODM MongoDB
- `mongodb` (^6.0.0) - Driver officiel

**Fichier .env généré** :
```env
MONGODB_URI=mongodb://localhost:27017/mon_projet
JWT_SECRET=super_secret_key_à_changer_en_production
NODE_ENV=development
```

**Package.json Scripts** :
```json
"dev": "cross-env NODE_OPTIONS='--loader ts-node/esm' nodemon --exec ts-node --esm src/app.ts"
"build": "tsc"
"start": "node dist/index.js"
```

**Installation locale** :
```bash
# Docker
docker run -d -p 27017:27017 --name mongodb mongo

# OU installation directe
# Windows: Télécharger depuis https://www.mongodb.com/try/download/community
# macOS: brew tap mongodb/brew && brew install mongodb-community
```

---

### 2️⃣ PostgreSQL Local (SQL Relational)
```
Sélection : 2) PostgreSQL Local (SQL Relational)
```

**Dépendances installées** :
- `@prisma/client` (5.13.0) - Prisma ORM
- `prisma` (5.13.0) - CLI Prisma

**Fichier .env généré** :
```env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/drugstoredb
DATABASE_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=PASSWORD
DB_NAME=drugstoredb
JWT_SECRET=super_secret_key_à_changer_en_production
NODE_ENV=development
```

**Package.json Scripts** :
```json
"dev": "cross-env NODE_OPTIONS='--loader ts-node/esm' nodemon --exec ts-node --esm src/app.ts"
"build": "tsc"
"start": "node dist/index.js"
"prisma:generate": "prisma generate"
"prisma:migrate": "prisma migrate dev"
"prisma:studio": "prisma studio"
```

**Installation locale** :
```bash
# Docker (recommandé)
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=PASSWORD \
  -e POSTGRES_DB=drugstoredb \
  --name postgres postgres:15

# OU installation directe
# Windows: https://www.postgresql.org/download/windows/
# macOS: brew install postgresql@15
# Linux: sudo apt-get install postgresql postgresql-contrib

# Créer la base de données
createdb -U postgres drugstoredb

# Vérifier la connexion
psql -U postgres -h localhost -d drugstoredb
```

**Commandes Prisma** :
```bash
# Générer le client Prisma
npm run prisma:generate

# Créer une migration
npm run prisma:migrate

# Visualiser la BD
npm run prisma:studio
```

**Schéma Prisma (schema.prisma)** :
```prisma
// Exemple de configuration
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id    Int     @id @default(autoincrement())
  name  String
  email String  @unique
}
```

---

### 3️⃣ Supabase (PostgreSQL Cloud)
```
Sélection : 3) Supabase (PostgreSQL Cloud)
```

**Dépendances installées** :
- `@prisma/client` (5.13.0) - Prisma ORM
- `prisma` (5.13.0) - CLI Prisma

**Fichier .env généré** :
```env
DATABASE_URL=postgresql://postgres.PROJECT_ID:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres
DATABASE_TYPE=postgres
DB_HOST=db.PROJECT_ID.supabase.co
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=PASSWORD
DB_NAME=postgres
SUPABASE_PROJECT_ID=PROJECT_ID
SUPABASE_API_KEY=your_supabase_api_key
SUPABASE_URL=https://PROJECT_ID.supabase.co
JWT_SECRET=super_secret_key_à_changer_en_production
NODE_ENV=production
```

**Package.json Scripts** :
```json
"dev": "cross-env NODE_OPTIONS='--loader ts-node/esm' nodemon --exec ts-node --esm src/app.ts"
"build": "tsc"
"start": "node dist/index.js"
"prisma:generate": "prisma generate"
"prisma:migrate": "prisma migrate deploy"
"prisma:studio": "prisma studio"
```

**Setup Supabase** :
```bash
# 1. Créer un compte sur https://app.supabase.com
# 2. Créer un nouveau projet
# 3. Récupérer les credentials :
#    - Project ID : Dans Settings → General
#    - Database Password : Dans Settings → Database
#    - API Key : Dans Settings → API

# 4. Remplir le .env avec les valeurs
# 5. Installer Prisma et générer le client
npm install @prisma/client prisma
npm run prisma:generate

# 6. Créer la première migration
npm run prisma:migrate
```

**Features inclus avec Supabase** :
- ✅ PostgreSQL managé et sécurisé
- ✅ Backups automatiques
- ✅ Authentication intégrée
- ✅ Real-time subscriptions
- ✅ Storage (fichiers)
- ✅ CDN global

---

## 🔧 Configuration après l'initialisation

### Vérifier quelle BD est sélectionnée

```bash
# Vérifier dans .spec-lock.json
cat .spec-lock.json | grep database

# Ou regarder le fichier .env du backend
cat backend/.env
```

### Changer de base de données

Si vous avez besoin de changer de BD :

```bash
# 1. Mettre à jour backend/.env avec les nouvelles credentials

# 2. Réinstaller les dépendances si nécessaire
npm install

# 3. Si passage MongoDB → PostgreSQL :
#    - Installer Prisma : npm install @prisma/client prisma
#    - Créer schema.prisma
#    - Générer migrations : npm run prisma:migrate

# 4. Si passage PostgreSQL → Supabase :
#    - Mettre à jour DATABASE_URL avec Supabase credentials
#    - Vérifier la connexion
#    - Redéployer : npm run prisma:migrate
```

---

## 📝 Scripts disponibles par type de BD

### MongoDB
```bash
npm run dev          # Start dev server
npm run build        # Build TypeScript
npm run start        # Run compiled code
npm run lint         # ESLint check
npm run format       # Format code with Prettier
npm run test         # Run tests
```

### PostgreSQL / Supabase
```bash
npm run dev                    # Start dev server avec hot-reload
npm run build                  # Build TypeScript
npm run start                  # Run compiled code
npm run prisma:generate        # Generate Prisma client
npm run prisma:migrate         # Create/apply migrations
npm run prisma:studio          # Open Prisma Studio (GUI)
npm run lint                   # ESLint check
npm run format                 # Format code with Prettier
npm run test                   # Run tests
```

---

## 🔐 Sécurité - Fichiers sensibles

⚠️ **NE JAMAIS versionner** :
- `.env` - Contient les vraies credentials
- `.env.local`

✅ **À versionner** :
- `.env.example` - Template avec valeurs fictives
- `package.json` - Dépendances déclarées
- `prisma/schema.prisma` - Schéma (ne contient pas de secrets)

---

## 🚀 Prochaines étapes

1. **Installation des dépendances** :
   ```bash
   npm install
   ```

2. **Configuration .env** :
   ```bash
   # Remplacer les placeholders dans backend/.env
   # Exemple : PASSWORD, PROJECT_ID, etc.
   ```

3. **Démarrer le serveur** :
   ```bash
   npm run dev
   ```

4. **Tests** :
   ```bash
   npm run test
   ```

---

## 💡 Recommandations

### Pour le développement local
👉 **MongoDB** ou **PostgreSQL Local**
- Plus rapide à setup
- Pas d'accès internet requis
- Idéal pour le prototypage

### Pour la production
👉 **Supabase** (PostgreSQL Cloud)
- Sécurité renforcée
- Backups automatiques
- Scalable et performant
- Inclus : Auth, Real-time, Storage

### Migration de données
Si vous devez migrer de MongoDB vers PostgreSQL :
```bash
# 1. Exporter MongoDB
mongoexport --collection users --out users.json

# 2. Transformer en SQL
# Scripts custom usando Prisma ou outils comme pgloader

# 3. Importer dans PostgreSQL
psql -U postgres -d drugstoredb -f import.sql
```

---

**Créé**: Mars 2026  
**Dernière mise à jour**: Mars 17, 2026
**Version**: 1.0
