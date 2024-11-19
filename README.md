# SeizureScoreAI: Multi-Agent Clinical Reasoning System

A sophisticated multi-agent system designed to emulate epileptologist decision-making for ILAE outcome scoring after epilepsy surgery. The system uses Large Language Models (LLMs) in a structured pipeline to process clinical notes and determine post-surgical outcomes. **The goal is to teach an LLM to think like an epileptologist.**

## Overview

SeizureScoreAI employs a three-agent system to process clinical notes and determine ILAE (International League Against Epilepsy) outcome scores:

1. **Clinical Information Extractor**: Analyzes clinical notes to extract key metrics including:
   - Presence of seizure freedom
   - Presence of auras
   - Baseline seizure frequency
   - Post-treatment seizure frequency

2. **ILAE Score Calculator**: Applies medical expertise to:
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
- **Backend**: Multi-agent system using OpenAI and Claude APIs
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
   git clone https://github.com/yourusername/SeizureScoreAI.git
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

## Deployment

To deploy on Streamlit Cloud:

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Configure the deployment:
   - Main file path: `streamlit/app.py`
   - Python version: 3.9+
4. Add the following secrets in Streamlit Cloud settings:
   - `OPENAI_API_KEY`
   - `CLAUDE_API_KEY`

## Development

### Project Structure
```
SeizureScoreAI/
├── streamlit/
│   ├── app.py              # Streamlit frontend
│   ├── ilae_backend.py     # Multi-agent system
│   └── config.toml         # Streamlit configuration
├── datagen/
│   └── generate_clinic_notes_claudeapi.ipynb  # Test data generation
├── test_notes/            # Sample clinical notes
└── requirements.txt
```

### Testing

The system includes a comprehensive set of test clinical notes in the `test_notes/` directory, representing various post-surgical outcomes and clinical scenarios.

## Security Considerations

- API keys are managed through environment variables
- Never commit `.env` files to version control
- Streamlit Cloud secrets provide secure deployment
- Input sanitization is implemented for clinical notes

## Limitations

- Requires high-quality clinical notes for accurate scoring
- LLM responses may vary slightly between runs
- System should be used as a support tool, not a replacement for clinical judgment
- Performance depends on the quality and completeness of input clinical notes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description of changes

## License

[Your chosen license]

## Citations

### Software Citation

If you use this system in your research, please cite:

```bibtex
@software{seizurescoreai2024,
  author = {Vineet Pasam Reddy},
  title = {SeizureScoreAI: Multi-Agent Clinical Reasoning System},
  year = {2024},
  url = {https://github.com/vineet-reddy/SeizureScoreAI}
}
```

### ILAE Outcome Scale Citation

The ILAE Outcome Scale used in this system is sourced from the MGH Epilepsy Service at Harvard Medical School. For more information, visit their [Epilepsy Surgery Outcome Scales page](https://seizure.mgh.harvard.edu/engel-surgical-outcome-scale/).
