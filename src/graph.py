from langgraph.graph import StateGraph, START, END
from src.state import State
from src.nodes import ingest, parse_cv, parse_jd, match_skills, flag_gaps, adapt_cv

def build_graph():
    builder = StateGraph(State)

    # Añadir nodos
    builder.add_node("ingest", ingest)
    builder.add_node("parse_cv", parse_cv)
    builder.add_node("parse_jd", parse_jd)
    builder.add_node("match_skills", match_skills)
    builder.add_node("flag_gaps", flag_gaps)
    builder.add_node("adapt_cv", adapt_cv)

    # Edges
    builder.add_edge(START, "ingest")
    
    # Paralelo: ingest → parse_cv y parse_jd a la vez
    builder.add_edge("ingest", "parse_cv")
    builder.add_edge("ingest", "parse_jd")
    
    # Ambos convergen en match_skills
    builder.add_edge("parse_cv", "match_skills")
    builder.add_edge("parse_jd", "match_skills")
    
    # match_skills → paralelo: flag_gaps y adapt_cv
    builder.add_edge("match_skills", "flag_gaps")
    builder.add_edge("match_skills", "adapt_cv")
    
    # Ambos convergen en END
    builder.add_edge("flag_gaps", END)
    builder.add_edge("adapt_cv", END)

    return builder.compile()