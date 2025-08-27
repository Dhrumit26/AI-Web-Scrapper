from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

moedel = OllamaLLM(model= "gemma3:1b")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


def parse_with_ollama(dom_chuncks, pharser_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | moedel

    parsed_result = []

    for i, chunk in enumerate(dom_chuncks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": pharser_description})
        print(f"Prased batch {i} of {len(dom_chuncks)}")
        parsed_result.append(response)
    
    return "\n".join(parsed_result)
