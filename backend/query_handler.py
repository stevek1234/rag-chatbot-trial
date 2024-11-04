import openai
from pinecone import Pinecone
import os

# Constants
embed_model = "text-embedding-3-small"  # Adjust model if necessary
limit = 3750  # Character limit for prompt size

print("Starting import of query_handler")


# def initialize_services():
#     """Initializes external services only when needed."""
#     openai.api_key = os.getenv('OPENAI_API_KEY')
#     pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
#     return pc.Index("initial-rag")


def retrieve(question):
    """
    Retrieves relevant contexts from Pinecone for the given query.
    """
    print("retrieve function called")
    openai.api_key = os.getenv('OPENAI_API_KEY')
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("initial-rag")
    # Embed the query
    res = openai.embeddings.create(input=[question], model=embed_model)
    xq = res.data[0].embedding

    # Retrieve relevant contexts from Pinecone
    contexts = []
    # time_waited = 0
    # while len(contexts) < 3 and time_waited < 60 * 12:
    res = index.query(vector=xq, top_k=3, include_metadata=True)
    print("Res: ", res)
    contexts.extend([x['metadata']['text'] for x in res['matches']])

    # Construct the prompt with retrieved contexts
    prompt_start = "Answer the question based on the context below.\n\nContext:\n"
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"
    final_prompt = prompt_start + "\n\n---\n\n".join(contexts) + prompt_end

    print(final_prompt)
    return final_prompt

print("after retrieve")


def complete(final_prompt):
    """
    Sends the constructed prompt to OpenAI's ChatCompletion API to generate an answer.
    """
    print("complete function called")
    # Define system message
    sys_prompt = "You are a helpful assistant that always answers questions."

    # Generate response using OpenAI ChatCompletion
    res = openai.chat.completions.create(
        model='gpt-4o-mini-2024-07-18',  # Update model name as required
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0
    )
    return res.choices[0].message.content.strip()


# Example usage
if __name__ == "__main__":
    query = "What's a red card?"
    prompt = retrieve(query)
    answer = complete(prompt)
    print("Generated Answer:", answer)


