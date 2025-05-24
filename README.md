# Stock Analysis RAG Pipeline

This project implements a Retrieval Augmented Generation (RAG) pipeline for analyzing stock data and generating investment recommendations. The system combines financial metrics with recent news sentiment to provide comprehensive investment advice.

## Features

- Processes financial metrics and stock data
- Analyzes recent news sentiment
- Generates detailed investment recommendations
- Uses LangChain for RAG implementation
- Leverages Ollama with Mistral model for local inference

## Prerequisites

- Python 3.8+
- Ollama installed and running locally (with Mistral model)
- Required Python packages (listed in requirements.txt)

## Installation

1. Install Ollama:
```bash
# For macOS/Linux
curl https://ollama.ai/install.sh | sh

# For Windows
# Download from https://ollama.ai/download
```

2. Pull the Mistral model:
```bash
ollama pull mistral
```

3. Clone the repository

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure Ollama is running:
```bash
# Start Ollama service
ollama serve
```

2. Ensure your stock data is in the correct format in `stock_data.json`

3. Run the analysis:
```bash
python stock_analysis_rag.py
```

The script will output a detailed investment recommendation considering:
- Financial metrics
- Recent news sentiment
- Market trends
- Risk factors

## Output Format

The recommendation includes:
1. Key strengths and concerns
2. Recent developments and their impact
3. Clear buy/hold/sell recommendation with reasoning
4. Risk factors to consider

## Data Sources

- Financial metrics from stock_data.json
- News data from integrated news sources
- Market sentiment analysis

## Benefits of Using Ollama

- Free and open-source
- Runs completely locally
- No API keys required
- Fast inference with Mistral model
- Privacy-preserving (no data sent to external services)

## Note

This tool is for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions. 