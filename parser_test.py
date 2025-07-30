from langchain.output_parsers.regex import RegexParser

def transform(input_list):
    new_list = []
    for key in input_list:
        if 'question1' in key or 'question2' in key:
            question_dict = {}
            question_num = key[-1]
            question_dict[f'question'] = input_list[key]
            question_dict[f'A'] = input_list[f'A_{question_num}']
            question_dict[f'B'] = input_list[f'B_{question_num}']
            question_dict[f'C'] = input_list[f'C_{question_num}']
            question_dict[f'D'] = input_list[f'D_{question_num}']
            question_dict[f'reponse'] = input_list[f'reponse{question_num}']
            new_list.append(question_dict)
    return new_list

# Define input string to parse
input_string = '''Pregunta: ¿Cuál es la principal contribución del artículo?
OPCION_A: Introducir una arquitectura híbrida que combina capas de deep learning con una capa final de razonamiento basada en un modelo gráfico discreto NP-hard
OPCION_B: Proponer una nueva función de pérdida que gestiona de forma eficiente la información lógica
OPCION_C: Usar modelos gráficos discretos como lenguaje de razonamiento
OPCION_D: Todas las anteriores
Respuesta: D

Pregunta: ¿Qué tipo de problemas puede aprender a resolver eficientemente la arquitectura neuronal y la función de pérdida propuestas?
OPCION_A: Solo problemas visuales
OPCION_B: Solo problemas simbólicos
OPCION_C: Solo problemas de optimización de energía
OPCION_D: Problemas de razonamiento NP-hard expresados como modelos gráficos discretos, incluyendo problemas simbólicos, visuales y de optimización de energía
Respuesta: D
'''

output_parser = RegexParser(
    regex=r"Pregunta:\s?(.*?)\nOPCION_A:\s?(.*?)\nOPCION_B:\s?(.*?)\nOPCION_C:\s?(.*?)\nOPCION_D:\s?(.*?)\nRespuesta:\s?(.*?)\n\nPregunta:\s?(.*?)\nOPCION_A:\s?(.*?)\nOPCION_B:\s?(.*?)\nOPCION_C:\s?(.*?)\nOPCION_D:\s?(.*?)\nRespuesta:\s?(.*)",
    output_keys=["question1", "A_1", "B_1", "C_1", "D_1", "reponse1", "question2", "A_2", "B_2", "C_2", "D_2", "reponse2"]
)
# Use the RegexParser to parse the input string
output_dict = transform(output_parser.parse(input_string))



# Print the parsed output
print(output_dict)

