# SeizureScoreAI: Multi-Agent Clinical Reasoning with Gemini

## Workshop Overview

This workshop demonstrates how to build a sophisticated multi-agent clinical reasoning system using Google's Gemini 2.5 Pro. The system processes epilepsy surgery clinic notes and determines ILAE (International League Against Epilepsy) outcome scores through a sequential pipeline of specialized AI agents.

### Key Learning Objectives

- **Multi-Agent Architecture**: Learn how to design and implement a sequential multi-agent system where each agent has a specialized role
- **Structured Outputs**: Master Gemini's native JSON mode for reliable, parseable responses
- **Clinical AI Applications**: Understand how to apply LLMs to complex medical decision-making tasks
- **Prompt Engineering**: Explore effective prompting strategies for information extraction and reasoning
- **Production Integration**: See how to integrate Gemini agents into a real-world application with a Streamlit frontend

## What This Workshop Demonstrates

### Gemini 2.5 Pro Capabilities

1. **Advanced Reasoning**: The system demonstrates Gemini's ability to perform multi-step clinical reasoning, matching the decision-making process of medical specialists
2. **Information Extraction**: Precise entity extraction from unstructured medical text
3. **Structured Generation**: Reliable JSON outputs using Gemini's native JSON mode
4. **Domain Expertise**: Application of medical knowledge (ILAE Outcome Scale) with supporting evidence
5. **Summarization**: Converting detailed clinical reasoning into concise, user-friendly explanations

### Architecture Highlights

```
Clinical Note Input
       ↓
┌──────────────────────────────────────┐
│   Agent 1: Information Extractor     │
│   - Extracts clinical entities       │
│   - Cites supporting text            │
│   - Returns structured JSON          │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│   Agent 2: ILAE Score Calculator     │
│   - Applies medical criteria         │
│   - Performs clinical reasoning      │
│   - Provides detailed explanation    │
└──────────────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│   Agent 3: Concise Reporter          │
│   - Summarizes findings              │
│   - Generates user-friendly output   │
│   - Maintains accuracy               │
└──────────────────────────────────────┘
       ↓
   Final Results
```

## The Clinical Challenge

### ILAE Outcome Scale

After epilepsy surgery, neurologists use the ILAE Outcome Scale to assess treatment effectiveness:

- **Class 1**: Completely seizure free; no auras
- **Class 2**: Only auras; no other seizures
- **Class 3**: 1-3 seizure days per year; ± auras
- **Class 4**: 4 seizure days per year to 50% reduction of baseline; ± auras
- **Class 5**: Less than 50% reduction of baseline; ± auras
- **Class 6**: More than 100% increase of baseline; ± auras

### The AI Solution

This system automates the ILAE classification process by:

1. **Extracting** key clinical information from free-text notes
2. **Reasoning** through the ILAE criteria systematically
3. **Explaining** the classification with evidence-based justification

## Technical Implementation

### Agent 1: Clinical Information Extractor

**Role**: Extract structured data from unstructured clinical notes

**Key Features**:
- Exact text citation for each extracted entity
- Uncertainty handling ("I don't know" when information is absent)
- No hallucination - only uses information present in the note

**Implementation Pattern**:
```python
def extract_clinical_information(clinical_note: str) -> Dict:
    prompt = """You are a clinical information extractor...
    Extract: seizure freedom, auras, baseline seizure days, post-treatment seizure days
    Format: JSON with value and supporting_text for each entity"""
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)
```

### Agent 2: ILAE Score Calculator

**Role**: Apply medical expertise to calculate ILAE score

**Key Features**:
- Implements the ILAE Outcome Scale criteria
- Provides detailed clinical reasoning
- Cites evidence from extracted information
- Handles edge cases and missing data

**Implementation Pattern**:
```python
def calculate_ilae_score(extracted_entities: Dict) -> Dict:
    # Calculate percent reduction
    percent_reduction = calculate_reduction(
        extracted_entities['baseline_seizure_days'],
        extracted_entities['seizure_days_per_year']
    )
    
    prompt = """You are a medical expert specializing in epilepsy...
    Apply ILAE Outcome Scale criteria...
    Provide: ilae_score, detailed_explanation"""
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)
```

### Agent 3: Concise Reporter

**Role**: Summarize detailed reasoning for end users

**Key Features**:
- Maintains accuracy while being concise
- Removes technical details
- Keeps essential clinical information

## Setup and Installation

### Prerequisites

- Python 3.12+
- Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/vineet-reddy/SeizureScoreAI
cd SeizureScoreAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### Testing the Installation

```bash
# Test Gemini API connection
python tests/test_gemini.py

# Test clinic note generation (Gemini 2.5 Flash)
python scripts/generate_clinic_notes.py
```

## Usage Examples

### Example 1: Running the Full Pipeline

```python
from seizure_score_ai.agents import process_clinical_note

# Load a clinical note
with open('app/example_notes/ilaeclass1.txt', 'r') as f:
    clinical_note = f.read()

# Process through multi-agent pipeline
final_output, detailed_output = process_clinical_note(clinical_note)

# Results
print(f"ILAE Score: {final_output['ilae_score']}")
print(f"Explanation: {final_output['concise_explanation']}")
print(f"Extracted Entities: {final_output['extracted_entities']}")
```

### Example 2: Running the Web Interface

```bash
streamlit run app/streamlit_app.py
```

Then:
1. Upload a clinical note (or use the example notes)
2. View the calculated ILAE score
3. See extracted entities highlighted in the note
4. Read the concise and detailed explanations

## Workshop Exercises

### Exercise 1: Understanding Agent Specialization

**Objective**: Modify Agent 1 to extract additional clinical entities

**Tasks**:
1. Add extraction of "medication names" to Agent 1
2. Test with example notes
3. Observe how structured prompting affects extraction quality

### Exercise 2: Improving Clinical Reasoning

**Objective**: Enhance Agent 2's reasoning capabilities

**Tasks**:
1. Add handling for edge cases (e.g., patients with unknown baseline)
2. Implement confidence scoring
3. Test with challenging cases

### Exercise 3: Custom Clinical Application

**Objective**: Build a new multi-agent system for a different clinical task

**Ideas**:
- Medication side effect extraction
- Treatment plan summarization
- Clinical trial eligibility screening

## Advanced Topics

### Rate Limiting and Production Considerations

**Free Tier Limits**: Gemini 2.5 Pro allows 2 requests per minute on the free tier. For production:

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(3))
def call_gemini_with_retry(prompt, model="gemini-2.5-pro"):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)
```

### Structured Output Schemas

For more complex outputs, define explicit JSON schemas:

```python
schema = {
    "type": "object",
    "properties": {
        "ilae_score": {"type": "string"},
        "confidence": {"type": "number"},
        "reasoning_steps": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["ilae_score", "confidence"]
}

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": schema
    }
)
```

### Alternative Architectures

**Parallel Processing**: For independent agents, use concurrent execution:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_note_parallel(clinical_note):
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Execute independent agents in parallel
        futures = [
            executor.submit(extract_medications, clinical_note),
            executor.submit(extract_diagnoses, clinical_note),
            executor.submit(extract_procedures, clinical_note)
        ]
        results = [f.result() for f in futures]
    return results
```

## Real-World Applications

### Clinical Decision Support

This architecture can be adapted for:
- Automated chart review
- Quality assurance in medical documentation
- Clinical trial screening
- Treatment plan optimization

### Key Considerations

1. **HIPAA Compliance**: Never use PHI in non-compliant systems
2. **Validation**: Always validate AI outputs with human experts
3. **Transparency**: Provide clear explanations for clinical decisions
4. **Accuracy**: Regularly evaluate system performance against expert annotations

## Resources

### Gemini Documentation

- [Gemini 2.5 Pro Model Card](https://ai.google.dev/gemini-api/docs/models/gemini-2-5)
- [Structured Output Guide](https://ai.google.dev/gemini-api/docs/json-mode)
- [google-genai Python SDK](https://github.com/google/generative-ai-python)

### Medical AI Guidelines

- [FDA AI/ML in Healthcare](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices)
- [ILAE Outcome Scale](https://seizure.mgh.harvard.edu/engel-surgical-outcome-scale/)

### Related Workshops

Explore other Gemini workshops at [google-gemini/workshops](https://github.com/google-gemini/workshops):
- Multi-agent game simulations
- Content generation pipelines
- AI-powered assistants

## Contributing

We welcome contributions! Areas for improvement:

1. **Additional Clinical Domains**: Extend to other medical specialties
2. **Enhanced Reasoning**: Implement chain-of-thought prompting
3. **Evaluation**: Build benchmarks against expert annotations
4. **UI/UX**: Improve the Streamlit interface
5. **Documentation**: Add more examples and tutorials

## License

This project is part of the Gemini workshops series. For specific licensing information, see the LICENSE file.

## Acknowledgments

Developed as part of the AI ATL Hackathon by:
- [Vineet Reddy](https://github.com/vineet-reddy)
- [Viresh Pati](https://github.com/vireshpati)
- [Mukesh Paranthaman](https://github.com/MukProgram)
- [Sachi Goel](https://github.com/computer-s-2)

Migrated to Gemini 2.5 Pro to demonstrate Google's state-of-the-art multi-agent capabilities for clinical AI applications.

---

**Note**: This is a demonstration system for educational purposes. It is not HIPAA compliant and should not be used with real patient data. Always consult with qualified healthcare professionals for medical decisions.

