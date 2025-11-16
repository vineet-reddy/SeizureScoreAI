# SeizureScoreAI: Multi-Agent Clinical Reasoning System

A multi-agent system designed to emulate epileptologist decision-making for ILAE outcome scoring after epilepsy surgery. Built with **Google's Agent Development Kit (ADK)**, the system uses Gemini 2.5 Pro models in a hierarchical agent architecture to process clinical notes and determine post-surgical outcomes. The goal is to teach an LLM to reason like an epileptologist.

## Overview

SeizureScoreAI employs a three-agent system to process clinical notes and determine ILAE (International League Against Epilepsy) outcome scores:

1. **Clinical Information Extractor**: Analyzes clinical notes to extract key metrics including:
   - Presence of seizure freedom
   - Presence of auras
   - Baseline seizure frequency
   - Post-treatment seizure frequency

2. **ILAE Score Calculator**: Applies expertise to:
   - Process extracted clinical information
   - Calculate ILAE outcome scores based on standard criteria
   - Provide detailed reasoning for score determination

3. **Concise Reporter**: Generates clear, concise explanations of:
   - Final ILAE score
   - Key factors influencing the score
   - Clinical reasoning behind the determination


## Technical Architecture

### Components

- **Frontend**: Streamlit interface for clinical note input and result display
- **Backend**: Multi-agent system built with **Google Agent Development Kit (ADK)**
- **Agent Framework**: Hierarchical agent architecture using ADK's `LlmAgent` class
- **Model**: Gemini 2.5 Pro for all agents
- **Agent Orchestration**: Root orchestrator agent coordinates three specialized sub-agents
- **Structured Output**: JSON-formatted data for consistent processing

### Data Flow

1. Clinical note input → Information Extraction
2. Structured data → ILAE Score Calculation
3. Detailed analysis → Concise Reporting
4. Final output → User presentation

## Usage

Run the Streamlit application:
```bash
streamlit run app/streamlit_app.py
```

The application will:
1. Accept clinical notes as input
2. Process them through the multi-agent system
3. Return ILAE scores with explanations
4. Provide detailed reasoning for the determination

## ILAE Outcome Scale

The system evaluates surgical outcomes based on the following scale[^1]:
- **Class 1**: Completely seizure free; no auras
- **Class 2**: Only auras; no other seizures
- **Class 3**: 1-3 seizure days per year; ± auras
- **Class 4**: 4 seizure days per year to 50% reduction of baseline seizure days; ± auras
- **Class 5**: Less than 50% reduction of baseline seizure days; ± auras
- **Class 6**: More than 100% increase of baseline seizure days; ± auras

[^1]: Source: [MGH Epilepsy Service - Epilepsy Surgery Outcome Scales](https://seizure.mgh.harvard.edu/engel-surgical-outcome-scale/)

## Development

### Project Structure
```
SeizureScoreAI/
├── src/
│   └── seizure_score_ai/
│       ├── __init__.py                          # Package initialization
│       └── agents.py                            # Multi-agent system using Google ADK with LlmAgent
├── app/
│   ├── streamlit_app.py                         # Streamlit frontend
│   ├── assets/
│   │   └── brainmodlab.png                      # UI assets
│   ├── example_notes/                           # Example clinical notes for demo
│   │   ├── ilaeclass1.txt
│   │   ├── ilaeclass2.txt
│   │   └── ilaeclass3.txt
│   └── config.toml                              # Streamlit configuration
├── scripts/
│   └── generate_clinic_notes.py                 # Synthetic clinic note generator
├── tests/
│   └── test_gemini.py                           # API verification test
├── data/
│   └── test_notes/                              # Sample clinical notes (synthetic)
│       ├── clinic_note_1.txt
│       ├── clinic_note_2.txt
│       └── ...
├── docs/
│   ├── ilae_kg.drawio                           # Visual representation of scoring logic
│   └── ...                                      # Presentations and documentation
├── .env                                         # Environment variables (not in repo)
├── .gitignore                                   # Git ignore rules
├── requirements.txt                             # Python dependencies
└── README.md                                    # Project documentation
```

### Testing

The system includes a comprehensive set of **synthetically generated test clinical notes** in the `test_notes/` directory, representing various post-surgical outcomes and clinical scenarios. These notes are designed to simulate real-world inputs but **do not contain any Protected Health Information (PHI)**, ensuring compliance with privacy regulations.


## Technology Stack

- **AI Framework**: **[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)** (`google-adk>=0.3.0`)
  - **Agent Architecture**: Hierarchical multi-agent system with `LlmAgent` class
  - **Model**: Gemini 2.5 Pro for all three specialized agents
  - **Orchestration**: Root agent coordinates sub-agents (Clinical Information Extractor, ILAE Score Calculator, Concise Reporter)
  - **Runner**: ADK's `Runner` class for agent execution and lifecycle management
  - **Benefits**: Production-ready framework with built-in tools, memory, observability, and deployment capabilities
- **Frontend**: Streamlit web application
- **Programming Language**: Python 3.12+
- **Environment Management**: python-dotenv for secure API key handling

## Security Considerations
- The system is **not currently HIPAA compliant**. Users must ensure that input clinical notes do not contain any Protected Health Information (PHI) before using the system.
- API keys are managed through environment variables
- Never commit `.env` files to version control
- Streamlit Cloud secrets provide secure deployment

## Limitations

- Requires high-quality clinical notes for accurate scoring
- LLM responses may vary slightly between runs
- System should be used as a support tool, not a replacement for clinical judgment
- Performance depends on the quality and completeness of input clinical notes

## Contributing

Interested in contributing? Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started!

## Project History

This project originated as a proof-of-concept at the 2024 AI ATL Hackathon and has since undergone a complete architectural rewrite. The current implementation uses Google's Agent Development Kit with a multi-agent system, representing a fundamental redesign from the original NER/Knowledge Graph approach. See [CONTRIBUTING.md](CONTRIBUTING.md#project-history-and-contributors) for detailed project evolution and contributor information.

## Citation

The ILAE Outcome Scale used in this system is sourced from the Massachusetts General Hospital Epilepsy Service. For more information, visit their [Epilepsy Surgery Outcome Scales page](https://seizure.mgh.harvard.edu/engel-surgical-outcome-scale/).
