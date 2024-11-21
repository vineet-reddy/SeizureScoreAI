# SeizureScoreAI: Multi-Agent Clinical Reasoning System

A multi-agent system designed to emulate epileptologist decision-making for ILAE outcome scoring after epilepsy surgery. The system uses Large Language Models (LLMs) in a structured pipeline to process clinical notes and determine post-surgical outcomes. The goal is to teach an LLM to reason like an epileptologist.

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
- **Backend**: Multi-agent system using OpenAI APIs
- **Agent Pipeline**: Sequential processing through specialized agents
- **Structured Output**: JSON-formatted data for consistent processing

### Data Flow

1. Clinical note input → Information Extraction
2. Structured data → ILAE Score Calculation
3. Detailed analysis → Concise Reporting
4. Final output → User presentation

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/vineet-reddy/SeizureScoreAI
   cd SeizureScoreAI
   ```

2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   CLAUDE_API_KEY=your_claude_key_here
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run streamlit/app.py
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
├── data/
│   ├── datagen/
│   │   └── generate_clinic_notes_claudeapi.ipynb  # Test data generation script
│   └── test_notes/                               # Sample clinical notes (synthetic)
│       ├── clinic_note_1.txt
│       ├── clinic_note_2.txt
│       └── ...
├── docs/
│   └── ILAE Knowledge Graph.drawio              # Visual representation of scoring logic
├── streamlit/
│   ├── app.py                                   # Streamlit frontend
│   ├── ilae_backend.py                          # Multi-agent system
│   └── config.toml                              # Streamlit configuration
├── .env                                         # Environment variables (not in repo)
├── .gitignore                                   # Git ignore rules
├── README.md                                    # Project documentation
└── requirements.txt                             # Python dependencies
```

### Testing

The system includes a comprehensive set of **synthetically generated test clinical notes** in the `test_notes/` directory, representing various post-surgical outcomes and clinical scenarios. These notes are designed to simulate real-world inputs but **do not contain any Protected Health Information (PHI)**, ensuring compliance with privacy regulations.


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

## Contributions

This project originated at the AI ATL Hackathon and was developed by [Vineet Reddy](https://github.com/vineet-reddy), [Viresh Pati](https://github.com/vireshpati), [Mukesh Paranthaman](https://github.com/MukProgram), and [Sachi Goel](https://github.com/computer-s-2).

- **[Vineet Reddy](https://github.com/vineet-reddy):** Conceived the idea to analyze epilepsy clinic notes and output ILAE scores. Developed the original Named Entity Recognition (NER) system with Viresh Pati. After the hackathon, revamped the project by creating the advanced multi-agent RAG system and updating the user interface.  
- **[Viresh Pati](https://github.com/vireshpati):** Co-designed the initial NER and knowledge graph retrieval-augmented generation (KG RAG) system.  
- **[Mukesh Paranthaman](https://github.com/MukProgram):** Co-built the backend for the original NER and KG RAG system.  
- **[Sachi Goel](https://github.com/computer-s-2):** Designed the initial Streamlit frontend.  
- **[Ananda Badari](https://github.com/abadari3):** Developed the now-deprecated logic for predicting ILAE and Engel scores using the knowledge graph, which informed the current system.

Their foundational work made the advanced multi-agent RAG system and updated interface possible.

### ILAE Outcome Scale Citation

The ILAE Outcome Scale used in this system is sourced from the Massachusetts General Hospital Epilepsy Service. For more information, visit their [Epilepsy Surgery Outcome Scales page](https://seizure.mgh.harvard.edu/engel-surgical-outcome-scale/).
