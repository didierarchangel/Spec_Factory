#!/bin/bash

# 🗄️ Script Setup pour les Configurations de Base de Données
# Utilisation: ./setup-env.sh mongodb|postgresql|supabase

# Vérifier les arguments
if [ -z "$1" ]; then
    echo "❌ Erreur: Vous devez spécifier une configuration"
    echo ""
    echo "Utilisation: ./setup-env.sh {mongodb|postgresql|supabase}"
    echo ""
    echo "Exemples:"
    echo "  ./setup-env.sh mongodb"
    echo "  ./setup-env.sh postgresql"
    echo "  ./setup-env.sh supabase"
    exit 1
fi

config=$1
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
env_file="$script_dir/.env"
template_file="$script_dir/.env.$config"

# Validation
if [[ ! "$config" =~ ^(mongodb|postgresql|supabase)$ ]]; then
    echo "❌ Erreur: Configuration invalide: $config"
    echo "Valeurs autorisées: mongodb|postgresql|supabase"
    exit 1
fi

echo "🔄 Configuration du Backend..."
echo "================================"

# Vérifier que le template existe
if [ ! -f "$template_file" ]; then
    echo "❌ Erreur: $template_file non trouvé!"
    exit 1
fi

# Sauvegarder le .env actuel
if [ -f "$env_file" ]; then
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="$script_dir/.env.backup.$timestamp"
    cp "$env_file" "$backup_file"
    echo "✅ Sauvegarde créée: $backup_file"
fi

# Copier le template vers .env
cp "$template_file" "$env_file"
echo "✅ Configuration copiée: $template_file → .env"

# Instructions par configuration
case $config in
    mongodb)
        echo ""
        echo -e "\033[1;33m📦 Configuration MongoDB sélectionnée\033[0m"
        echo ""
        echo -e "\033[1;36mInstructions d'installation:\033[0m"
        echo "  1. Assurez-vous que MongoDB est installé et en cours d'exécution"
        echo "  2. Local: mongod (port 27017)"
        echo "     OU Utilisez MongoDB Atlas: https://cloud.mongodb.com"
        echo ""
        echo -e "\033[1;36mVérifier la connexion:\033[0m"
        echo -e "  \033[90mnpm run test:db\033[0m"
        echo ""
        ;;
    postgresql)
        echo ""
        echo -e "\033[1;33m🐘 Configuration PostgreSQL Local sélectionnée\033[0m"
        echo ""
        echo -e "\033[1;36mInstructions d'installation:\033[0m"
        echo "  1. Installez PostgreSQL:"
        echo "     macOS: brew install postgresql@15"
        echo "     Linux: sudo apt-get install postgresql"
        echo "  2. OU Utilisez Docker:"
        echo -e "     \033[90mdocker run -d -p 5432:5432 -e POSTGRES_PASSWORD=PASSWORD postgres:15\033[0m"
        echo ""
        echo -e "\033[1;36mCréer la base de données:\033[0m"
        echo -e "  \033[90mcreatdb -U postgres drugstoredb\033[0m"
        echo ""
        echo -e "\033[1;36mTester la connexion:\033[0m"
        echo -e "  \033[90mpsql -U postgres -h localhost -d drugstoredb\033[0m"
        echo ""
        echo -e "\033[1;31m⚠️  N'OUBLIEZ PAS:\033[0m"
        echo -e "  \033[1;31m- Remplacer PASSWORD par votre mot de passe PostgreSQL dans .env\033[0m"
        echo ""
        ;;
    supabase)
        echo ""
        echo -e "\033[1;33m🚀 Configuration Supabase (PostgreSQL Cloud) sélectionnée\033[0m"
        echo ""
        echo -e "\033[1;36mInstructions:\033[0m"
        echo -e "  1. Créer un compte Supabase: \033[90mhttps://app.supabase.com\033[0m"
        echo "  2. Créer une nouveau projet"
        echo "  3. Récupérer les credentials dans Project Settings → Database"
        echo "  4. Remplir les variables dans .env"
        echo ""
        echo -e "\033[1;36mVariables à récupérer:\033[0m"
        echo -e "  - PROJECT_ID (ex: abc123def456)"
        echo -e "  - DATABASE_PASSWORD"
        echo -e "  - API_KEY (anon ou service_role)"
        echo ""
        echo -e "\033[1;31m⚠️  N'OUBLIEZ PAS:\033[0m"
        echo -e "  \033[1;31m- Remplacer PROJECT_ID et PASSWORD dans .env\033[0m"
        echo -e "  \033[1;31m- Ne pas commiter le .env avec les vraies valeurs\033[0m"
        echo ""
        ;;
esac

echo "================================"
echo -e "\033[1;32m✅ Configuration complète!\033[0m"
echo ""
echo -e "\033[1;36mProchaines étapes:\033[0m"
echo -e "  1. \033[90mnpm install\033[0m"
echo -e "  2. \033[90mnpm run db:migrate\033[0m"
echo -e "  3. \033[90mnpm run dev\033[0m"
echo ""
