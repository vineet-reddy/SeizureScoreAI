from swarm import Swarm, Agent
import openai
import os
from dotenv import load_dotenv
import json
import re

# Try to load .env file, but don't fail if it doesn't exist (for cloud deployment)
load_dotenv(verbose=True)

# Get API keys from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize Swarm client
client = Swarm()

# Define Agent 1: Clinical Information Extractor
def agent_1_instructions(context_variables):
    return """
You are a clinical information extractor. Your task is to extract the following entities from the provided clinical note, quoting the exact text from the note that supports each entity.

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

""".format(clinical_note=context_variables.get('clinical_note', ''))


agent_1 = Agent(
    name="Clinical Information Extractor",
    instructions=agent_1_instructions
)

# Define Agent 2: ILAE Score Calculator
def agent_2_instructions(context_variables):
    return """
You are a medical expert specializing in epilepsy. Your task is to calculate the ILAE score based on the provided clinical information extracted from the clinical note. Use the ILAE Outcome Scale criteria below to determine the correct score. Provide detailed reasoning for each entity influencing the score, citing the exact text from the clinical note that supports your reasoning.

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
- **If you cannot determine the ILAE score based on the available data, set `"ilae_score"` to `"indeterminate"`.**

**Output Format:**

Provide the output in the following JSON format (without any additional text):

{{
  "ilae_score": "...",
  "detailed_explanation": "..."
}}

Calculate the ILAE score using this information.
""".format(
    presence_of_seizure_freedom=context_variables.get('presence_of_seizure_freedom', "I don't know"),
    supporting_text_seizure_freedom=context_variables.get('supporting_texts', {}).get('presence_of_seizure_freedom', "Not provided"),
    presence_of_auras=context_variables.get('presence_of_auras', "I don't know"),
    supporting_text_auras=context_variables.get('supporting_texts', {}).get('presence_of_auras', "Not provided"),
    baseline_seizure_days=context_variables.get('baseline_seizure_days', "I don't know"),
    supporting_text_baseline=context_variables.get('supporting_texts', {}).get('baseline_seizure_days', "Not provided"),
    seizure_days_per_year=context_variables.get('seizure_days_per_year', "I don't know"),
    supporting_text_post_treatment=context_variables.get('supporting_texts', {}).get('seizure_days_per_year', "Not provided"),
    percent_reduction=context_variables.get('percent_reduction_in_seizure_days', "I don't know")
)


agent_2 = Agent(
    name="ILAE Score Calculator",
    instructions=agent_2_instructions
)

# Define Agent 3: Concise ILAE Score Reporter
def agent_3_instructions(context_variables):
    return """
You are an assistant tasked with providing a concise and clear explanation of the ILAE score based on the detailed explanation from the previous calculation. Do not recalculate or re-present the ILAE score. Your role is to summarize the detailed explanation into a concise explanation suitable for display on the frontend.

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

""".format(
    detailed_explanation=context_variables.get('detailed_explanation', "Not provided")
)


agent_3 = Agent(
    name="Concise ILAE Score Reporter",
    instructions=agent_3_instructions
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
    # Extract the assistant's last message
    assistant_message = ilae_response.messages[-1]['content']
    return assistant_message

# Define the function to generate the concise explanation
def generate_concise_explanation(context_variables):
    messages = [{"role": "user", "content": "Please provide a concise explanation of the ILAE score based on the detailed explanation provided."}]
    concise_response = client.run(
        agent=agent_3,
        messages=messages,
        context_variables=context_variables,
        max_turns=5
    )
    # Extract the assistant's last message
    assistant_message = concise_response.messages[-1]['content']
    return assistant_message

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
        # Update context_variables with the 'value' of each entity
        context_variables['presence_of_seizure_freedom'] = extracted_entities['presence_of_seizure_freedom']['value']
        context_variables['presence_of_auras'] = extracted_entities['presence_of_auras']['value']
        context_variables['baseline_seizure_days'] = extracted_entities['baseline_seizure_days']['value']
        context_variables['seizure_days_per_year'] = extracted_entities['seizure_days_per_year']['value']
        # Store the supporting texts
        context_variables['supporting_texts'] = {
            'presence_of_seizure_freedom': extracted_entities['presence_of_seizure_freedom']['supporting_text'],
            'presence_of_auras': extracted_entities['presence_of_auras']['supporting_text'],
            'baseline_seizure_days': extracted_entities['baseline_seizure_days']['supporting_text'],
            'seizure_days_per_year': extracted_entities['seizure_days_per_year']['supporting_text'],
        }
    except (KeyError, json.JSONDecodeError):
        return "Failed to parse extracted information. Please ensure the clinical note is properly formatted."

    # Calculate the percent reduction in seizure days using the formula
    try:
        baseline_seizure_days_str = context_variables['baseline_seizure_days']
        seizure_days_per_year_str = context_variables['seizure_days_per_year']

        if (baseline_seizure_days_str.lower() == "i don't know" or
            seizure_days_per_year_str.lower() == "i don't know"):
            percent_reduction = "I don't know"
            context_variables['percent_reduction_in_seizure_days'] = percent_reduction
        else:
            baseline_seizure_days = float(baseline_seizure_days_str)
            seizure_days_per_year = float(seizure_days_per_year_str)
            percent_reduction = ((baseline_seizure_days - seizure_days_per_year) / baseline_seizure_days) * 100
            context_variables['percent_reduction_in_seizure_days'] = percent_reduction
    except (ValueError, TypeError):
        context_variables['percent_reduction_in_seizure_days'] = "I don't know"

    # Calculate the ILAE score using Agent 2
    ilae_score_response = calculate_ilae_score(context_variables)

    # Parse Agent 2's output
    ilae_response_cleaned = ilae_score_response.strip()
    ilae_response_cleaned = re.sub(r'^```(?:json)?\n?', '', ilae_response_cleaned)
    ilae_response_cleaned = re.sub(r'\n?```$', '', ilae_response_cleaned)
    ilae_response_cleaned = ilae_response_cleaned.strip()

    try:
        ilae_result = json.loads(ilae_response_cleaned)
        context_variables['ilae_score'] = ilae_result['ilae_score']
        context_variables['detailed_explanation'] = ilae_result['detailed_explanation']
    except (KeyError, json.JSONDecodeError):
        return "Failed to parse ILAE score information. Please ensure the outputs are properly formatted."

    # Generate the concise explanation using Agent 3
    concise_explanation_response = generate_concise_explanation(context_variables)

    # Parse Agent 3's output
    concise_response_cleaned = concise_explanation_response.strip()
    concise_response_cleaned = re.sub(r'^```(?:json)?\n?', '', concise_response_cleaned)
    concise_response_cleaned = re.sub(r'\n?```$', '', concise_response_cleaned)
    concise_response_cleaned = concise_response_cleaned.strip()

    try:
        concise_result = json.loads(concise_response_cleaned)
        concise_explanation = concise_result['concise_explanation']
    except (KeyError, json.JSONDecodeError):
        return "Failed to parse concise explanation. Please ensure the outputs are properly formatted."

    # Store the detailed explanation separately
    detailed_explanation = context_variables['detailed_explanation']

    # Prepare the final outputs
    final_output = {
        "ilae_score": context_variables['ilae_score'],
        "concise_explanation": concise_explanation
    }

    detailed_output = {
        "detailed_explanation": detailed_explanation
    }

    # Return both outputs
    return final_output, detailed_output
