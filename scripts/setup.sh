#!/bin/bash
# Setup script for Terminal AI Agents Workshop

echo "Setting up Terminal AI Agents Workshop..."

# Create directory structure
mkdir -p src/{patterns,labs,tools,examples}
mkdir -p tests
mkdir -p docs
mkdir -p images

# Install Python dependencies
cat > requirements.txt << EOF
anthropic>=0.18.0
openai>=1.0.0
google-generativeai>=0.3.0
requests>=2.31.0
pytest>=7.4.0
python-dotenv>=1.0.0
EOF

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
cat > .env.example << EOF
# API Keys
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
SEARCH_API_KEY=your-key-here

# Agent Configuration
DEFAULT_MODEL=claude-3-sonnet-20240229
MAX_TOKENS=4096
TEMPERATURE=0.7
EOF

echo "Setup complete! Don't forget to:"
echo "1. Copy .env.example to .env and add your API keys"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the examples: python src/examples/complete_agent.py"
