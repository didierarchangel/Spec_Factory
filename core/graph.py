# Le "Cerveau" du Spec-Kit 
# Implémentation du graphe de base
# Ce module implémente le graphe de traitement LangGraph qui exécute les tâches de manière itérative et conditionnelle.

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
import operator

# 1. Définition de l'état du graphe (Mémoire) [cite: 162-168]
class AgentState(TypedDict):
    project_description: str
    proposed_arch: str
    is_validated: bool
    user_feedback: str
    user_request: str
    task_id: str
    constitution: str
    current_step: str
    task_content: str
    validation_result: str
    next_task: str
    completed_tasks: list

# 2. Initialisation du graphe
graph_builder = StateGraph(AgentState)

# 3. Définition des nœuds (Fonctions) [cite: 170-175]
def architect_node(state: AgentState): # load constitution
    # Logique de chargement de CONSTITUTION.md
    return {"constitution": "Contenu de la constitution..."}

def execute_task(state: AgentState):
    # Logique d'exécution de la tâche via LangChain
    return {"task_content": "Résultat de l'exécution..."}

def human_validation_node(state: AgentState):
    # Ce nœud sert de pause pour l'utilisateur [cite: 5, 19]
    pass

def validate_task(state: GraphState):
    # Logique de validation (Appel au Validator)
    return {"validation_result": "OK/KO"}

def decide_next_step(state: GraphState):
    # Logique conditionnelle (Si KO -> Revenir en arrière, Si OK -> Avancer)
    if state["validation_result"] == "OK":
        return "next_task"
    else:
        return "previous_task"

# 4. Construction du graphe (Assemblage/Workflow) [cite: 176-180]
graph_builder.add_node("architect", architect_node)
graph_builder.add_node("validator", human_validation_node)
graph_builder.set_entry_point("architect")
graph_builder.add_edge("architect", "validator")

graph_builder.add_node("load_constitution", load_constitution)
graph_builder.add_node("execute_task", execute_task)
graph_builder.add_node("validate_task", validate_task)
graph_builder.add_node("decide_next_step", decide_next_step)

# 5. Définition des transitions (Flux) [cite: 181-185]
graph_builder.add_edge(START, "load_constitution")
graph_builder.add_edge("load_constitution", "execute_task")
graph_builder.add_edge("execute_task", "validate_task")
graph_builder.add_edge("validate_task", "decide_next_step")

# Boucle conditionnelle : Si la validation échoue, on retourne à l'exécution de la tâche précédente
graph_builder.add_conditional_edges(
    "decide_next_step",
    decide_next_step,
    {
        "next_task": "execute_task",
        "previous_task": "execute_task" # Simplifié pour l'exemple
    }
)

graph_builder.add_edge("decide_next_step", END)

# Si validé -> Fin, sinon -> Retour à l'architecte [cite: 19]
graph_builder.add_conditional_edges("validator", lambda x: "end" if x["is_validated"] else "architect")

# Compilation du graphe
app = graph_builder.compile()
