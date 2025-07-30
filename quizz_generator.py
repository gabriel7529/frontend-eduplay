from qcm_chain import QCMGenerateChain
from qa_llm import QaLlm
import asyncio

async def llm_call(qa_chain: QCMGenerateChain, text: str):
    batch_examples = await asyncio.gather(qa_chain.aapply_and_parse(text))
    print(f"llm lo ha realizado.")

    return batch_examples

async def generate_quizz(content:str):
    """
    Generates a quizz from the given content.
    """
    qa_llm = QaLlm()
    qa_chain = QCMGenerateChain.from_llm(qa_llm.get_llm())

    return await llm_call(qa_chain, [{"doc": content}])


