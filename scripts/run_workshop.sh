#!/bin/bash
# Run workshop examples

# Source environment
source venv/bin/activate
source .env

# Menu
echo "Terminal AI Agents Workshop"
echo "=========================="
echo "1. Run minimal agent"
echo "2. Run complete agent"
echo "3. Compare agents benchmark"
echo "4. Run tests"
echo "5. Start Jupyter notebook"

read -p "Select option: " choice

case $choice in
    1) python src/labs/minimal_agent.py ;;
    2) python src/examples/complete_agent.py ;;
    3) python src/labs/agent_comparison.py ;;
    4) pytest tests/ -v ;;
    5) jupyter notebook ;;
    *) echo "Invalid option" ;;
esac
