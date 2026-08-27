from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

def analyze_abstract(abstract_text):
    prompt = f"""You are analyzing a technical research abstract. Your job is to interpret it carefully WITHOUT hallucinating information not supported by the text.

Abstract:
\"\"\"{abstract_text}\"\"\"

Return ONLY a JSON object (no other text, no markdown formatting) with exactly these fields:

- "problem": the research problem being addressed
- "gap": the limitation or gap in existing approaches, or "This cannot be determined reliably from the abstract." if not inferable
- "approach": the proposed solution/method/architecture
- "probable_innovation": the likely main contribution (use "Probable Innovation", not "Confirmed")
- "why_it_may_work": a simple explanation, clearly labeling parts as "Explicitly stated in abstract", "AI inference", or "Not enough information"
- "technical_terms": a list of objects, each with "term", "simple_meaning", "role_in_research"
- "simple_explanation": the main idea rewritten for a non-expert
- "researchers_message": what the researcher is essentially trying to communicate
- "evidence": short phrases/sentences from the abstract supporting the interpretation
- "confidence": one of "High", "Medium", "Low", with a brief reason why

If the abstract is too short or unclear to determine something, say so explicitly rather than guessing.
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json\n", "", 1)

    return json.loads(raw_text)