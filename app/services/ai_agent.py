import os
import json
import logging
from typing import List, Dict, Any
from fastapi import HTTPException
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_json_response(raw: str) -> str:
    """Clean JSON response from AI"""
    return raw.strip().replace("'", '"').replace("```json", "").replace("```", "")

async def run_legal_agent(
    country: str,
    product_features: List[str],
    structured_rules: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    system_prompt = """Analyze features against rules. Return JSON object with:
- 'results': array containing:
  - 'feature': Original text
  - 'compliance': 'Compliant', 'Not Compliant', or 'Needs Review'
  - 'justification': Rule references"""
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4-1106-preview",  # Updated model supporting JSON
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({
                    "country": country,
                    "features": product_features,
                    "rules": structured_rules
                })}
            ],
            temperature=0,
            max_tokens=2000
        )
        
        cleaned = clean_json_response(response.choices[0].message.content)
        data = json.loads(cleaned)
        return data.get("results", [])
    
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        raise HTTPException(500, "Compliance analysis failed")