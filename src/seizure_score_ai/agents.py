"""
Multi-Agent Clinical Reasoning System using Google Gemini 2.5 Pro

This module implements a sequential multi-agent pipeline for processing clinical notes
and calculating ILAE outcome scores. Each agent is a specialized function that calls
Google's Gemini 2.5 Pro with tailored prompts.

Architecture:
    Agent 1: Clinical Information Extractor
    Agent 2: ILAE Score Calculator  
    Agent 3: Concise Explanation Reporter
"""

from google import genai
import os
from dotenv import load_dotenv
import json
import re
from typing import Dict, Tuple, Optional

# Load environment variables
load_dotenv(verbose=True)

# Initialize Gemini client
def setup_gemini_client() -> genai.Client:
    """Setup and verify the Gemini client with API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not found. "
            "Please set it in your .env file."
        )
    
    os.environ["GEMINI_API_KEY"] = api_key
    return genai.Client()

# Initialize the global client
client = setup_gemini_client()

# Model configuration
GEMINI_MODEL = "gemini-2.5-pro"


def extract_clinical_information(clinical_note: str) -> Dict:
    """
    Agent 1: Clinical Information Extractor
    
    Extracts key clinical entities from the clinical note including:
    - Presence of seizure freedom
    - Presence of auras
    - Baseline seizure days (pre-treatment)
    - Seizure days per year (post-treatment)
    
    Args:
        clinical_note: Raw clinical note text
        
    Returns:
        Dictionary containing extracted entities with values and supporting texts
    """
    
    prompt = f"""You are a clinical information extractor. Your task is to extract the following entities from the provided clinical note, quoting the exact text from the note that supports each entity.

Entities to extract:

1. **Presence of seizure freedom** (Yes/No/I don't know)
2. **Presence of auras** (Yes/No/I don't know)
3. **Baseline seizure days (pre-treatment)** (Numeric value or "I don't know")
4. **Seizure days per year (post-treatment)** (Numeric value or "I don't know")

For each entity, provide:

- **Value**: As specified above.
- **Supporting text**: Exact quote from the clinical note that supports the value.

**Important Guidelines:**

- **Use only the information in the clinical note**. Do not add any information not present.
- **Quote the supporting text exactly** as it appears in the clinical note.
- **Do not paraphrase, summarize, or interpret** beyond the given text.
- If the information is **not present or cannot be determined**, set the value to "I don't know" and the supporting text to "Not found in the clinical note."

**Output Format:**

Provide **only** the extracted entities in the following JSON format (without any additional text):

{{
  "presence_of_seizure_freedom": {{
    "value": "...",
    "supporting_text": "..."
  }},
  "presence_of_auras": {{
    "value": "...",
    "supporting_text": "..."
  }},
  "baseline_seizure_days": {{
    "value": "...",
    "supporting_text": "..."
  }},
  "seizure_days_per_year": {{
    "value": "...",
    "supporting_text": "..."
  }}
}}

**Clinical Note:**

{clinical_note}
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Agent 1: {e}")
        print(f"Response text: {response.text}")
        raise
    except Exception as e:
        print(f"Error in Clinical Information Extractor: {e}")
        raise


def calculate_ilae_score(extracted_entities: Dict) -> Dict:
    """
    Agent 2: ILAE Score Calculator
    
    Calculates the ILAE outcome score based on extracted clinical information
    using the ILAE Outcome Scale criteria.
    
    Args:
        extracted_entities: Dictionary of extracted clinical information from Agent 1
        
    Returns:
        Dictionary containing ILAE score and detailed explanation
    """
    
    # Extract values and supporting texts
    presence_of_seizure_freedom = extracted_entities['presence_of_seizure_freedom']['value']
    supporting_text_seizure_freedom = extracted_entities['presence_of_seizure_freedom']['supporting_text']
    
    presence_of_auras = extracted_entities['presence_of_auras']['value']
    supporting_text_auras = extracted_entities['presence_of_auras']['supporting_text']
    
    baseline_seizure_days = extracted_entities['baseline_seizure_days']['value']
    supporting_text_baseline = extracted_entities['baseline_seizure_days']['supporting_text']
    
    seizure_days_per_year = extracted_entities['seizure_days_per_year']['value']
    supporting_text_post_treatment = extracted_entities['seizure_days_per_year']['supporting_text']
    
    # Calculate percent reduction
    try:
        if (str(baseline_seizure_days).lower() == "i don't know" or 
            str(seizure_days_per_year).lower() == "i don't know"):
            percent_reduction = "I don't know"
        else:
            baseline = float(baseline_seizure_days)
            post = float(seizure_days_per_year)
            percent_reduction = ((baseline - post) / baseline) * 100 if baseline > 0 else 0
    except (ValueError, TypeError):
        percent_reduction = "I don't know"
    
    prompt = f"""You are a medical expert specializing in epilepsy. Your task is to calculate the ILAE score based on the provided clinical information extracted from the clinical note. Use the ILAE Outcome Scale criteria below to determine the correct score. Provide detailed reasoning for each entity influencing the score, citing the exact text from the clinical note that supports your reasoning.

**ILAE Outcome Scale:**
- **Class 1**: Completely seizure free; no auras
- **Class 2**: Only auras; no other seizures
- **Class 3**: 1 to 3 seizure days per year; ± auras
- **Class 4**: 4 seizure days per year to 50% reduction of baseline seizure days; ± auras
- **Class 5**: Less than 50% reduction of baseline seizure days; ± auras
- **Class 6**: More than 100% increase of baseline seizure days; ± auras

**Extracted Entities and Supporting Texts:**
1. Presence of seizure freedom: {presence_of_seizure_freedom}
   - Supporting text: {supporting_text_seizure_freedom}
2. Presence of auras: {presence_of_auras}
   - Supporting text: {supporting_text_auras}
3. Baseline seizure days (pre-treatment): {baseline_seizure_days}
   - Supporting text: {supporting_text_baseline}
4. Seizure days per year (post-treatment): {seizure_days_per_year}
   - Supporting text: {supporting_text_post_treatment}
5. Percent reduction in seizure days: {percent_reduction}

**Instructions:**
- Use the provided information to calculate the ILAE score.
- Provide detailed reasoning for each entity influencing the score.
- Cite the supporting texts in your reasoning.
- If any information is uncertain or not available, acknowledge this in your reasoning and proceed based on the available data.
- **Note**: If the patient has only auras and no other seizures, classify them as **Class 2**, even if baseline and post-treatment seizure days are unknown.
- **If you cannot determine the ILAE score based on the available data, set `"ilae_score"` to `"indeterminate"`.**

**Output Format:**

Provide the output in the following JSON format (without any additional text):

{{
  "ilae_score": "...",
  "detailed_explanation": "..."
}}

Calculate the ILAE score using this information.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Agent 2: {e}")
        print(f"Response text: {response.text}")
        raise
    except Exception as e:
        print(f"Error in ILAE Score Calculator: {e}")
        raise


def generate_concise_explanation(detailed_explanation: str) -> Dict:
    """
    Agent 3: Concise Explanation Reporter
    
    Summarizes the detailed ILAE score explanation into a concise format
    suitable for frontend display.
    
    Args:
        detailed_explanation: Detailed explanation from Agent 2
        
    Returns:
        Dictionary containing concise explanation
    """
    
    prompt = f"""You are an assistant tasked with providing a concise and clear explanation of the ILAE score based on the detailed explanation from the previous calculation. Do not recalculate or re-present the ILAE score. Your role is to summarize the detailed explanation into a concise explanation suitable for display on the frontend.

**Instructions:**

- Summarize the detailed explanation provided.
- Do not recalculate or re-present the ILAE score.
- Provide the concise explanation without any unnecessary details.

**Output Format:**

Provide the output in the following JSON format (without any additional text):

{{
  "concise_explanation": "..."
}}

**Detailed Explanation from the previous calculation:**

{detailed_explanation}
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Agent 3: {e}")
        print(f"Response text: {response.text}")
        raise
    except Exception as e:
        print(f"Error in Concise Explanation Reporter: {e}")
        raise


def process_clinical_note(clinical_note: str) -> Tuple[Dict, Dict]:
    """
    Main orchestration function for the multi-agent clinical reasoning pipeline.
    
    Processes a clinical note through three sequential agents:
    1. Clinical Information Extractor
    2. ILAE Score Calculator
    3. Concise Explanation Reporter
    
    Args:
        clinical_note: Raw clinical note text
        
    Returns:
        Tuple of (final_output, detailed_output) where:
        - final_output contains: ilae_score, concise_explanation, extracted_entities
        - detailed_output contains: detailed_explanation
    """
    
    try:
        # Agent 1: Extract clinical information
        print("Agent 1: Extracting clinical information...")
        extracted_entities = extract_clinical_information(clinical_note)
        
        # Agent 2: Calculate ILAE score
        print("Agent 2: Calculating ILAE score...")
        ilae_result = calculate_ilae_score(extracted_entities)
        
        ilae_score = ilae_result['ilae_score']
        detailed_explanation = ilae_result['detailed_explanation']
        
        # Agent 3: Generate concise explanation
        print("Agent 3: Generating concise explanation...")
        concise_result = generate_concise_explanation(detailed_explanation)
        
        concise_explanation = concise_result['concise_explanation']
        
        # Prepare final outputs
        final_output = {
            "ilae_score": ilae_score,
            "concise_explanation": concise_explanation,
            "extracted_entities": extracted_entities
        }
        
        detailed_output = {
            "detailed_explanation": detailed_explanation
        }
        
        print("Processing complete!")
        return final_output, detailed_output
        
    except Exception as e:
        print(f"Error in process_clinical_note: {e}")
        raise
