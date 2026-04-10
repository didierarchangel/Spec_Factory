# 📜 CONSTITUTION DU PROJET
**Date d'initialisation :** 2026-04-08

## RÈGLE CRITIQUE - INSTALLATION NPM
1. Interdiction formelle de générer des numéros de version fixes de mémoire (ex: `1.2.3`).
2. Obligation d'utiliser `@latest` pour toute nouvelle dépendance ajoutée via commande npm.
3. Si une dépendance est écrite directement dans `package.json`, utiliser:
   - `react`: `^18.0.0`
   - `vite`: `^5.0.0`
   - `@vitejs/plugin-react`: `^4.0.0`
