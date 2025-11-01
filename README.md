# Naive Grad GPT - Interactive Story Game

An interactive text-based adventure game powered by fine-tuned language models and AI image generation. Players make choices that influence the story progression in a medieval fantasy setting.

## Technologies Used

### Core Framework
- **Python 3.8+** - Primary programming language
- **Streamlit** - Web application framework for the game interface
- **Flask** - API server for model inference
- **Jupyter Notebooks** - Development and model deployment environment

### Machine Learning Stack
- **PyTorch** - Deep learning framework
- **Transformers (Hugging Face)** - Pre-trained model handling
- **PEFT (Parameter Efficient Fine-Tuning)** - LoRA adapters for model customization
- **Auto-GPTQ** - Model quantization for efficient inference
- **Accelerate** - Distributed training and inference optimization

## AI Technologies

### Language Models
- **Mistral-7B-Instruct-v0.2-GPTQ** - Base quantized language model for story generation
- **Custom Fine-tuned Adapters** - PEFT LoRA adapters trained on game-specific data
- **BERT Extractive Summarizer** - Text summarization for context management

### RAG Implementation
- **LangChain** - Framework for Retrieval-Augmented Generation
- **Sentence Transformers** - Text embedding generation
- **FAISS** - Vector similarity search for document retrieval
- **HuggingFace Embeddings** - Text vectorization

### Image Generation
- **OpenAI DALL-E API** - AI-generated scene illustrations

## Third-Party Integrations

### APIs
- **OpenAI API** - Image generation service
- **Ngrok** - Secure tunneling for Google Colab deployment

### Model Repositories
- **Hugging Face Hub** - Model hosting and version management
- **TheBloke Models** - Optimized GPTQ model variants

### Infrastructure
- **Google Colab** - Cloud GPU computing for model inference
- **GitHub** - Version control and code repository

## How to Run

### Prerequisites
- Python 3.8 or higher
- Make utility
- OpenAI API key
- Google Colab account (for GPU inference)

### Setup and Installation
```bash
# Clone the repository
git clone <repository-url>
cd project-14-naive-grad-gpt

# Setup environment and install dependencies
make setup

# Alternative: Install dependencies only
make install-deps
```

### Running the Application

#### Method 1: Using Google Colab (Recommended)
```bash
# Follow Colab setup instructions
make run-colab

# After Colab setup, run locally
make run-local
```

#### Method 2: Manual Setup
1. Upload `Inference.ipynb` to Google Colab
2. Connect to GPU runtime and execute all cells
3. Copy the generated ngrok URL from the output
4. Update the URL in `streamlit-app/pages/start_game.py:9`
5. Add your OpenAI API key to `streamlit-app/pages/start_game.py:10`
6. Run the Streamlit application:
```bash
make run-local
```

### Additional Commands
```bash
make clean      # Remove generated files and virtual environment
make help       # Display available commands
```

## Project Structure

```
project-14-naive-grad-gpt/
├── Inference.ipynb              # Main model inference notebook
├── streamlit-app/              # Streamlit web application
│   ├── streamlit-dummy.py      # Main application entry point
│   └── pages/                  # Application pages
├── old/                        # Legacy notebooks and experiments
│   ├── fine-tuning/           # Model fine-tuning notebooks
│   └── *.ipynb               # Previous project iterations
├── Makefile                   # Build and run commands
└── requirements.txt          # Python dependencies
```
