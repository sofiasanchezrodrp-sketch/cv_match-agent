from langchain_anthropic import ChatAnthropic
from src.state import State
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model="claude-haiku-4-5", temperature=0.1)

def ingest(state: State) -> State:
    """Recibe el CV y la oferta — no hace nada, solo los pasa al State."""
    return state

def parse_cv(state: State) -> State:
    """Extrae las skills del CV."""
    response = model.invoke(f"""
        Analiza este CV y extrae una lista de skills técnicas, profesionales e idiomas.
        Incluye explícitamente los idiomas con su nivel (ej: "English C1", "German B1").
        Devuelve SOLO una lista Python válida de strings, sin explicaciones.
        Ejemplo: ["Python", "SQL", "LangChain", "English C1", "German B1"]
        
        CV:
        {state["cv_texto"]}
    """)
    import ast
    try:
        skills = ast.literal_eval(response.content)
    except:
        skills = [s.strip() for s in response.content.split(",")]
    return {"skills_cv": skills}

def parse_jd(state: State) -> State:
    """Extrae las skills requeridas de la oferta."""
    response = model.invoke(f"""
        Analiza esta oferta de trabajo y extrae una lista de skills requeridas.
        Incluye idiomas con su nivel si se mencionan.
        Devuelve SOLO una lista Python válida de strings, sin explicaciones.
        Ejemplo: ["Python", "SQL", "LangChain", "English C1"]
        
        Oferta:
        {state["oferta_texto"]}
    """)
    import ast
    try:
        skills = ast.literal_eval(response.content)
    except:
        skills = [s.strip() for s in response.content.split(",")]
    return {"skills_oferta": skills}

def match_skills(state: State) -> State:
    """Calcula el match semántico entre skills del CV y la oferta."""
    response = model.invoke(f"""
        Eres un experto en selección de personal.
        
        Compara estas dos listas de skills y determina cuáles del CV cubren los requisitos de la oferta.
        Ten en cuenta sinónimos y equivalencias:
        - "ML" = "Machine Learning"
        - "XGBoost" o "scikit-learn" cubren "Machine Learning"
        - Si el CV tiene un nivel de idioma IGUAL O SUPERIOR al requerido, cuenta como match
        - "Spanish native" o "Español nativo" cubre cualquier requisito de español
        - "English C1" cubre "English B2", "Inglés", "English" o cualquier nivel inferior a C1
        
        Skills del CV: {state["skills_cv"]}
        Skills requeridas en la oferta: {state["skills_oferta"]}
        
        Devuelve SOLO un JSON válido con este formato exacto, sin explicaciones:
        {{
            "match": ["skill1", "skill2"],
            "gap": ["skill3", "skill4"],
            "score": 75.0
        }}
        
        El score es el porcentaje de requisitos de la oferta que cubre el candidato (0-100).
    """)
    
    import json
    import re
    try:
        json_str = re.search(r'\{.*\}', response.content, re.DOTALL).group()
        data = json.loads(json_str)
        return {
            "skills_match": data["match"],
            "skills_gap": data["gap"],
            "fit_score": float(data["score"])
        }
    except:
        return {
            "skills_match": [],
            "skills_gap": state["skills_oferta"],
            "fit_score": 0.0
        }
    
    import json
    import re
    try:
        json_str = re.search(r'\{.*\}', response.content, re.DOTALL).group()
        data = json.loads(json_str)
        return {
            "skills_match": data["match"],
            "skills_gap": data["gap"],
            "fit_score": float(data["score"])
        }
    except:
        return {
            "skills_match": [],
            "skills_gap": state["skills_oferta"],
            "fit_score": 0.0
        }

def flag_gaps(state: State) -> State:
    """Genera recomendaciones basadas en los gaps."""
    response = model.invoke(f"""
        El candidato tiene un fit del {state["fit_score"]}% con la oferta.
        
        Skills que tiene: {state["skills_match"]}
        Skills que le faltan: {state["skills_gap"]}
        
        Genera 3-5 recomendaciones concretas y accionables para mejorar el fit.
        Sé directo y específico.
    """)
    return {"recomendaciones": response.content}

def adapt_cv(state: State) -> State:
    """Adapta el CV a la oferta sin inventarse nada."""
    response = model.invoke(f"""
        Tienes este CV original y esta oferta de trabajo.
        Reescribe el CV priorizando y destacando las experiencias más relevantes para la oferta.
        
        REGLAS ESTRICTAS:
        - No inventes nada que no esté en el CV original
        - No añadas skills que no tenga el candidato
        - Solo reorganiza, prioriza y reformula lo que ya existe
        - Usa las keywords de la oferta donde sea honestamente aplicable
        
        CV original:
        {state["cv_texto"]}
        
        Oferta:
        {state["oferta_texto"]}
        
        Skills a destacar: {state["skills_match"]}
    """)
    return {"cv_adaptado": response.content}
