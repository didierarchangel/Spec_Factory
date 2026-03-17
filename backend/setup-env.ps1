# 🗄️ Script Setup pour les Configurations de Base de Données
# Utilisation: .\setup-env.ps1 -config mongodb|postgresql|supabase

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("mongodb", "postgresql", "supabase")]
    [string]$config
)

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = "$backendDir\.env"
$templateFile = "$backendDir\.env.$config"

Write-Host "🔄 Configuration du Backend..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Vérifier que le fichier template existe
if (-not (Test-Path $templateFile)) {
    Write-Host "❌ Erreur: $templateFile non trouvé!" -ForegroundColor Red
    exit 1
}

# Faire une sauvegarde du .env actuel si il existe
if (Test-Path $envFile) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = "$backendDir\.env.backup.$timestamp"
    Copy-Item $envFile $backupFile
    Write-Host "✅ Sauvegarde créée: $backupFile" -ForegroundColor Green
}

# Copier le template vers .env
Copy-Item $templateFile $envFile -Force
Write-Host "✅ Configuration copiée: $templateFile → .env" -ForegroundColor Green

# Afficher les instructions par configuration
switch ($config) {
    "mongodb" {
        Write-Host ""
        Write-Host "📦 Configuration MongoDB sélectionnée" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Instructions d'installation:" -ForegroundColor Cyan
        Write-Host "  1. Assurez-vous que MongoDB est installé et en cours d'exécution"
        Write-Host "  2. Local: mongod (port 27017)"
        Write-Host "     OU Utilisez MongoDB Atlas: https://cloud.mongodb.com"
        Write-Host ""
        Write-Host "Vérifier la connexion:" -ForegroundColor Cyan
        Write-Host "  npm run test:db" -ForegroundColor Gray
        Write-Host ""
    }
    "postgresql" {
        Write-Host ""
        Write-Host "🐘 Configuration PostgreSQL Local sélectionnée" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Instructions d'installation:" -ForegroundColor Cyan
        Write-Host "  1. Installez PostgreSQL: https://www.postgresql.org/download/windows/"
        Write-Host "  2. OU Utilisez Docker:"
        Write-Host "     docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=PASSWORD postgres:15" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Créer la base de données:" -ForegroundColor Cyan
        Write-Host "  createdb -U postgres drugstoredb" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Tester la connexion:" -ForegroundColor Cyan
        Write-Host "  psql -U postgres -h localhost -d drugstoredb" -ForegroundColor Gray
        Write-Host ""
        Write-Host "⚠️  N'OUBLIEZ PAS:" -ForegroundColor Red
        Write-Host "  - Remplacer PASSWORD par votre mot de passe PostgreSQL dans .env" -ForegroundColor Red
        Write-Host ""
    }
    "supabase" {
        Write-Host ""
        Write-Host "🚀 Configuration Supabase (PostgreSQL Cloud) sélectionnée" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Instructions:" -ForegroundColor Cyan
        Write-Host "  1. Créer un compte Supabase: https://app.supabase.com" -ForegroundColor Gray
        Write-Host "  2. Créer une nouveau projet" -ForegroundColor Gray
        Write-Host "  3. Récupérer les credentials dans Project Settings → Database" -ForegroundColor Gray
        Write-Host "  4. Remplir les variables dans .env" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Variables à récupérer:" -ForegroundColor Cyan
        Write-Host "  - PROJECT_ID (ex: abc123def456)" -ForegroundColor Gray
        Write-Host "  - DATABASE_PASSWORD" -ForegroundColor Gray
        Write-Host "  - API_KEY (anon ou service_role)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "⚠️  N'OUBLIEZ PAS:" -ForegroundColor Red
        Write-Host "  - Remplacer PROJECT_ID et PASSWORD dans .env" -ForegroundColor Red
        Write-Host "  - Ne pas commiter le .env avec les vraies valeurs" -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Configuration complète!" -ForegroundColor Green
Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. npm install" -ForegroundColor Gray
Write-Host "  2. npm run db:migrate" -ForegroundColor Gray
Write-Host "  3. npm run dev" -ForegroundColor Gray
Write-Host ""
