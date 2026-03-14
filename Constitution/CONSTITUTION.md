# 📜 Constitution du Projet (Store-Manager)

## ⚖️ Principes Fondamentaux
- **Sanctuarisation** : Le code validé ne doit être modifié que sur ordre explicite.
- **Additivité** : Privilégier l'ajout de code plutôt que la modification de l'existant.
- **Zéro Placeholder** : Pas de `TODO`, `FIXME` ou fonctions vides.

## 🔧 Configuration TC (ES Modules - ESM Obligatoire)

**Tous les projets Speckit.Factory doivent être configurés en ES Modules (ESM).**

### Backend Configuration
- **Type**: `"type": "module"` (obligatoire dans `backend/package.json`)
- **TypeScript**: `tsconfig.json` avec `"module": "ESNext"` et `"target": "ES2022"`
- **Exécution**: `ts-node --esm` ou `nodemon --exec ts-node --esm`
- **Build Output**: `dist/` avec fichiers `.js` compilés depuis TypeScript
- **Imports**: Tous les chemins relatifs doivent inclure l'extension `.js` (ex: `import { User } from "./models/user.js"`)
- **Interdiction**: Zéro usage de `require()` ou `import ... = require()`

### Frontend Configuration
- **Type**: `"type": "module"` (Vite gère cela nativement)
- **Build**: Vite crée des bundles ESM par défaut
- **Imports**: Aucune extension requise sur les imports locaux (Vite normalise)

---

## 🎨 Design Constitution
L'intelligence graphique du projet est pilotée par le subagent `GraphicDesign`.

### Principes Graphiques
- **Clarté & Minimalisme** : Interfaces épurées, focus sur le contenu.
- **Réactivité** : Design "Mobile-First" utilisant Tailwind CSS.
- **Identité Visuelle** :
  - **Standard** : Basé sur Material Tailwind.
  - **Premium (premium)** : Palette bleu/blanc, ombres douces, typographie monospacée pour les données numériques.

### Règles de Mise en Page
- **Conteneurs** : `max-w-7xl mx-auto px-6`
- **Espacement des Sections** : `py-16`
- **Cartes** : `rounded-xl shadow-md p-6` (Standard) ou `rounded-xl shadow-xl border border-gray-100` (Premium).

### Couleurs de Référence
- **Primaire** : `blue-600` / `indigo-600`
- **Neutre** : `slate-800`
- **Accent** : `emerald-500` / `indigo-500`
