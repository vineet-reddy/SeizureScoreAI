# SeizureScoreAI

Knowledge Graph + RAG system with LLMs to predict Engel scores for seizure outcomes.

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key_here
   CLAUDE_API_KEY=your_claude_key_here
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run streamlit/app.py
   ```

## Deployment

To deploy on Streamlit Cloud:

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add the following secrets in Streamlit Cloud settings:
   - OPENAI_API_KEY
   - CLAUDE_API_KEY
4. Deploy!
