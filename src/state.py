from typing_extensions import TypedDict
from typing import Annotated
import operator

class State(TypedDict):
    cv_texto: str
    oferta_texto: str
    skills_cv: list
    skills_oferta: list
    skills_match: list
    skills_gap: list
    fit_score: float
    recomendaciones: str
    cv_adaptado: str