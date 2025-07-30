"""LLM Chain specifically for generating examples for QCM (Question Choix Multiples) answering."""
from __future__ import annotations

from typing import Any

from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.output_parsers.regex import RegexParser

from langchain.prompts import PromptTemplate

template = """Eres un profesor creando preguntas para un cuestionario.
Dado el siguiente documento, genera exactamente 2 preguntas de opción múltiple (MCQ),
cada una con 4 opciones (OPCION_A, OPCION_B, OPCION_C, OPCION_D) y la letra de la respuesta correcta.

Usa el siguiente formato:

Pregunta: <escribe la pregunta aquí>
OPCION_A: <primera opción>
OPCION_B: <segunda opción>
OPCION_C: <tercera opción>
OPCION_D: <cuarta opción>
Respuesta: <A o B o C o D>

Las preguntas deben ser detalladas, claras y basadas únicamente en la información proporcionada en el documento.

<Begin Document>
{doc}
<End Document>"""


output_parser = RegexParser(
    regex=r"Pregunta:\s?\n?(.*?)\nOPCION_A:\s?(.*?)\nOPCION_B:\s?(.*?)\nOPCION_C:\s?(.*?)\nOPCION_D:\s?(.*?)\nRespuesta:\s?(.*?)\n\nPregunta:\s?\n?(.*?)\nOPCION_A:\s?(.*?)\nOPCION_B:\s?(.*?)\nOPCION_C:\s?(.*?)\nOPCION_D:\s?(.*?)\nRespuesta:\s?(.*)",
    output_keys=["question1", "A_1", "B_1", "C_1", "D_1", "reponse1", "question2", "A_2", "B_2", "C_2", "D_2", "reponse2"]
)

PROMPT = PromptTemplate(
    input_variables=["doc"], template=template, output_parser=output_parser
)

class QCMGenerateChain(LLMChain):
    """LLM Chain specifically for generating examples for QCM answering."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, **kwargs: Any) -> QCMGenerateChain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)
