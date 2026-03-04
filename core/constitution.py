# Gestion de la création/mise à jour de la Constitution 
# Le fichier constitution.py doit agir comme un gardien. 
# Il utilise LangChain pour transformer la demande brute de l'utilisateur en une architecture structurée,
# puis la fige dans le marbre numérique

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path
import hashlib

class ConstitutionManager:
    def __init__(self, constitution_path="Constitution/CONSTITUTION.md"):
        self.path = Path(constitution_path)
        self.llm = ChatOpenAI(model="gpt-4o-mini") # Ou gpt-3.5-turbo

    def _calculate_hash(self, content: str) -> str:
        """Calcule le hash SHA256 pour détecter les changements."""
        return hashlib.sha256(content.encode()).hexdigest()

    def generate_constitution(self, user_request: str) -> str:
        """Génère la constitution à partir de la demande utilisateur."""
        
        # Prompting stratégique pour forcer l'architecture en 4 piliers
        prompt = ChatPromptTemplate.from_template(
            f"""
            Tu es l'Architecte en Chef de Speckit.Factory.
            Transforme la demande utilisateur suivante en une Constitution formelle.
            
            RÈGLES STRICTES :
            1. La Constitution DOIT être structurée en 4 sections principales (Piliers).
            2. Utilise exactement ce format Markdown :
            
            # 1. PILIER ARCHITECTURAL
            [Description de l'architecture logicielle]
            
            # 2. PILIER DE SÉCURITÉ
            [Règles de chiffrement, gestion des accès]
            
            # 3. PILIER DE PERFORMANCE
            [Exigences de latence, scalabilité]
            
            # 4. PILIER DE MAINTENANCE
            [Logs, tests, déploiement]
            
            Demande utilisateur : "{user_request}"
            
            Rends la réponse concise mais complète.
            """
        )

        chain = prompt | self.llm
        result = chain.invoke({"user_request": user_request})
        return result.content

    def update_constitution(self, new_content: str) -> bool:
        """Met à jour la constitution si le contenu a changé."""
        
        # Lire le contenu actuel (s'il existe)
        current_content = ""
        if self.path.exists():
            current_content = self.path.read_text(encoding="utf-8")
        
        # Comparer les hashes
        if self._calculate_hash(current_content) == self._calculate_hash(new_content):
            print("✅ La Constitution est déjà à jour (Hash identique).")
            return False
        
        # Écrire le nouveau contenu
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(new_content, encoding="utf-8")
        
        print(f"✅ Constitution mise à jour et verrouillée (Hash: {self._calculate_hash(new_content)}).")
        return True