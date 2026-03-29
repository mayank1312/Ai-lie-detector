import ollama
def fact_check(statement, deception_label, confidence):
    prompt = f"""
You are an AI assistant.

You are given:
- Statement: "{statement}"
- Deception Signal: {deception_label}
- Confidence: {confidence:.2f}

----------------------------------------

STEP 1 — CLASSIFY:

- Objective → real-world fact
- Personal → personal claim
- Opinion → subjective belief

IMPORTANT:
- If statement involves events, dates, countries → ALWAYS Objective

----------------------------------------

STEP 2 — VERDICT:

- If Objective → give ONLY True or False based on real-world knowledge
- If Personal or Opinion → give True or False based on how believable it sounds

----------------------------------------

STEP 3 — OUTPUT (STRICT JSON):

{{
  "type": "Objective/Personal/Opinion",
  "verdict": "True/False",
  "statement": "{statement}",
  "confidence": {confidence:.2f}
}}

RULES:
- No extra text
- Only JSON
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]