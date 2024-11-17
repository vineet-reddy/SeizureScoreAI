# ilae_backend.py

from swarm import Swarm, Agent
import openai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()  # Load environment variables from .env

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Swarm client
client = Swarm()

# Define Agent 2: ILAE Score Calculator
def agent_2_instructions(context_variables):
    return f"""
You are a medical expert specializing in epilepsy. Your task is to calculate the ILAE score based on the provided clinical information. Use the ILAE Outcome Scale criteria below to determine the correct score. Provide detailed reasoning for each entity influencing the score.

**ILAE Outcome Scale:**
- **Class 1**: Completely seizure free; no auras
- **Class 2**: Only auras; no other seizures
- **Class 3**: 1 to 3 seizure days per year; ± auras
- **Class 4**: 4 seizure days per year to 50% reduction of baseline seizure days; ± auras
- **Class 5**: Less than 50% reduction of baseline seizure days; ± auras
- **Class 6**: More than 100% increase of baseline seizure days; ± auras

**Extracted Entities:**
1. Presence of seizure freedom: {context_variables.get('presence_of_seizure_freedom', "I don't know")}
2. Presence of auras: {context_variables.get('presence_of_auras', "I don't know")}
3. Baseline seizure days (pre-treatment): {context_variables.get('baseline_seizure_days', "I don't know")}
4. Seizure days per year (post-treatment): {context_variables.get('seizure_days_per_year', "I don't know")}
5. Percent reduction in seizure days: {context_variables.get('percent_reduction_in_seizure_days', "I don't know")}

Calculate the ILAE score using this information, and provide detailed reasoning for each entity influencing the score.
    """

agent_2 = Agent(
    name="ILAE Score Calculator",
    instructions=agent_2_instructions
)

# Define the function to calculate the ILAE score
def calculate_ilae_score(context_variables):
    messages = [{"role": "user", "content": "Please calculate the ILAE score based on the extracted clinical information."}]
    ilae_response = client.run(
        agent=agent_2,
        messages=messages,
        context_variables=context_variables,
        max_turns=5
    )
    return ilae_response

# Define Agent 1: Clinical Information Extractor
def agent_1_instructions(context_variables):
    return f"""
You are a clinical information extractor. Your task is to extract the following entities from the clinical note provided:

1. Presence of seizure freedom.
2. Presence of auras.
3. Baseline seizure days (pre-treatment).
4. Seizure days per year (post-treatment).

Please ensure that:
- **Baseline seizure days** refers to the number of seizure days per year before any treatment or surgery (pre-treatment).
- **Seizure days per year** refers to the number of seizure days per year after treatment or surgery (post-treatment).

Clinical Note:
{context_variables.get('clinical_note', '')}

Use the clinical note to extract these entities accurately. If any entity information is missing or not explicitly stated in the clinical note, respond with "I don't know" for that particular entity. Once you have extracted the information, calculate the percent reduction in seizure days.

**Important:**
- Output **only** the extracted entities in the following JSON format, without any additional text, explanations, or code fences.
- Do **not** include any markdown formatting or code blocks.

JSON Format:
{{
  "presence_of_seizure_freedom": "...",
  "presence_of_auras": "...",
  "baseline_seizure_days": "...",
  "seizure_days_per_year": "...",
  "percent_reduction_in_seizure_days": "..."
}}

Replace the '...' with the appropriate values.
"""

agent_1 = Agent(
    name="Clinical Information Extractor",
    instructions=agent_1_instructions
)

# Wrap the main processing logic into a function
def process_clinical_note(clinical_note):
    # Set up context variables
    context_variables = {
        "clinical_note": clinical_note
    }
    
    # Run the Swarm client with Agent 1 to extract clinical information
    response = client.run(
        agent=agent_1,
        messages=[{"role": "user", "content": "Please process the clinical note."}],
        context_variables=context_variables,
        max_turns=5
    )
    
    # Extract Agent 1's output
    agent1_output = response.messages[-1]['content']
    
    # Clean the output by removing code fences and extra whitespace
    agent1_output_cleaned = agent1_output.strip()
    agent1_output_cleaned = re.sub(r'^```(?:json)?\n?', '', agent1_output_cleaned)
    agent1_output_cleaned = re.sub(r'\n?```$', '', agent1_output_cleaned)
    agent1_output_cleaned = agent1_output_cleaned.strip()
    
    # Parse the output and update context_variables
    try:
        extracted_entities = json.loads(agent1_output_cleaned)
        context_variables.update(extracted_entities)
    except json.JSONDecodeError:
        return "Failed to parse extracted information. Please ensure the clinical note is properly formatted."
    
    # Calculate the ILAE score using Agent 2
    ilae_score_response = calculate_ilae_score(context_variables)
    
    # Collect the final response from Agent 2
    final_response = "\n".join([message['content'] for message in ilae_score_response.messages if message['role'] == 'assistant'])
    
    return final_response
