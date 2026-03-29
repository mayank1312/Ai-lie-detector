import torch
import json
import re
import ollama
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from src.fact_check import fact_check

tokenizer = DistilBertTokenizerFast.from_pretrained("model/bert_model")
model = DistilBertForSequenceClassification.from_pretrained("model/bert_model")


def generate_final_reason(statement, final_verdict, statement_type):
    prompt = f"""
You are an AI assistant.

Explain the result in simple terms.

Statement: "{statement}"
Final Verdict: {final_verdict}
Type: {statement_type}

Rules:

- If Final Verdict is True:
    - If type is Objective → write only:
      "This statement is true based on real-world facts and evidence."
    - If type is Personal or Opinion → write only:
      "Does not sound suspicious and can be true."

- If Final Verdict is False:
    - If type is Objective → write only:
      "This statement is false based on real-world facts and evidence."
    - If type is Personal or Opinion → write only:
      "Sounds suspicious and is likely false."

- No extra text
- Only the sentence
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def run_pipeline(text: str):
    text = text.strip()

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits).item()
        probs = torch.softmax(logits, dim=1)

    label = "true" if prediction == 1 else "false"
    confidence = torch.max(probs).item()

    response = fact_check(text, label, confidence)

    try:
        data = json.loads(response)
    except:
        json_str = re.search(r'\{.*\}', response, re.DOTALL).group()
        data = json.loads(json_str)

    statement_type = data["type"]
    llm_verdict = data["verdict"]
    statement = data["statement"]
    confidence = data["confidence"]
    ml_prediction = label

    if statement_type == "Objective":
        final = llm_verdict
    else:
        if llm_verdict.lower() == "false":
            if ml_prediction == "false":
                final = "False"
            else:
                final = "True"
        elif llm_verdict.lower() == "true":
            if ml_prediction == "true":
                final = "True"
            else:
                final = "False"
        elif ml_prediction == "false":
            final = "False"
        else:
            final = "True"

    final = "True" if final.lower() == "true" else "False"

    final_reason = generate_final_reason(statement, final, statement_type)

    return {
        "statement": statement,
        "type": statement_type,
        "confidence": round(confidence * 100, 2),
        "verdict": final,
        "reason": final_reason
    }