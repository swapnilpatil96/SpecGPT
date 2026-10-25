
def generate_answer(client, query, context, model_name="gpt-4o-mini"):
    """Generate an answer using retrieved specification context."""

    system_prompt = """
You are SpecGPT, an assistant that answers questions
about functional specification documents.

Use only the provided specification context to answer.
Do not invent requirements or business rules.
If the context does not contain enough information,
clearly say that the specification does not provide
sufficient information to answer.

Mention the relevant section or subsection when possible.
"""

    user_prompt = f"""
Question:
{query}

Specification context:
{context}
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content
