# EngelAI

Knowledge Graph + RAG system with LLMs to predict Engel scores for seizure outcomes.

This project builds upon an original AI ATL Hackathon project developed by [Vineet Reddy](https://github.com/vineet-reddy), [Viresh Pati](https://github.com/vireshpati), [MukProgram](https://github.com/MukProgram), and [Sachi Goel](https://github.com/computer-s-2). 

[Ananda Badari](https://github.com/abadari3)) helped develop the logic for the knowledge graph predicting ILAE and Engel scores.

The hackathon prototype served as a foundation for this more comprehensive system, which now aims to predict Engel scores from clinical notes in order to assist with seizure outcome assessments.

## Project Overview

EngelAI leverages a hybrid approach, combining a Knowledge Graph with a Retrieval-Augmented Generation (RAG) system and a Large Language Model (LLM) to predict Engel scores for patients based on clinical documentation. This approach integrates structured and unstructured data to support more precise and interpretable predictions, particularly focusing on seizure outcomes.

## Features

- **Knowledge Graph Integration**: Encodes structured patient and outcome data for context-rich predictions.
- **RAG System**: Allows for efficient retrieval of relevant information to enhance LLM performance on clinical notes.
- **LLM-Powered Scoring**: Employs a state-of-the-art LLM fine-tuned for clinical language, aiming to predict Engel scores that measure seizure control and surgical outcome.

## Engel Score Prediction

The Engel scoring system is a widely accepted measure for evaluating seizure outcomes post-surgery. By automating Engel score predictions from clinical notes, EngelAI hopes to provide clinicians with timely, data-driven insights into patient progress and treatment efficacy.
