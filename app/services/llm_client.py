import os
import json
from dotenv import load_dotenv
from mistralai.client import Mistral
from app.schemas.qualite import EvaluationIA
load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def evaluer_projet(projet_data: dict) -> EvaluationIA:
    prompt = f"""Tu es un expert en évaluation qualité de projets de recherche scientifique.

Voici les données du projet à évaluer :
{json.dumps(projet_data, indent=2, ensure_ascii=False)}

Analyse ce projet et réponds UNIQUEMENT avec un JSON valide, sans aucun texte avant ou après, respectant exactement cette structure :
{{
  "forces": ["force 1", "force 2"],
  "faiblesses": ["faiblesse 1", "faiblesse 2"],
  "risques": ["risque 1", "risque 2"],
  "niveau_risque": "faible" | "modere" | "eleve" | "critique",
  "recommandation": "une recommandation concrète",
  "resume": "un résumé en 2-3 phrases"
}}"""

    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

   

    contenu_brut = response.choices[0].message.content
    contenu_nettoye = contenu_brut.strip()
    if contenu_nettoye.startswith("```"):
        contenu_nettoye = contenu_nettoye.split("```")[1]
        if contenu_nettoye.startswith("json"):
            contenu_nettoye = contenu_nettoye[4:]
    contenu_nettoye = contenu_nettoye.strip()

    try:
        donnees_json = json.loads(contenu_nettoye)

        return EvaluationIA(
            projet_id=projet_data.get("id", "inconnu"),
            forces=donnees_json["forces"],
            faiblesses=donnees_json["faiblesses"],
            risques=donnees_json["risques"],
            niveau_risque=donnees_json["niveau_risque"],
            recommandation=donnees_json["recommandation"],
            resume=donnees_json["resume"]
        )

    except (json.JSONDecodeError, KeyError) as erreur:
        return EvaluationIA(
            projet_id=projet_data.get("id", "inconnu"),
            forces=[],
            faiblesses=[],
            risques=["Erreur lors de l'analyse IA : réponse du LLM non exploitable"],
            niveau_risque="critique",
            recommandation="Réessayer l'évaluation ou vérifier manuellement le projet",
            resume=f"L'évaluation automatique a échoué ({type(erreur).__name__})"
        )