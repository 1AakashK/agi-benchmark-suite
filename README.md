# AGI Benchmark Suite

A comprehensive benchmark suite for testing AGI capabilities across multiple domains and cognitive abilities.

## Overview

This benchmark suite evaluates AI systems on key traits associated with Artificial General Intelligence:

- **Transfer Learning**: Ability to apply knowledge from one domain to another
- **Memory**: Ability to retain and recall information over time
- **Abstraction**: Ability to form concepts and generalize from examples
- **Planning**: Ability to formulate multi-step plans and adapt to changing conditions

Across multiple domains:

- **Code**: Programming and software development tasks
- **Logic**: Logical reasoning and problem-solving
- **Vision**: Visual pattern recognition and reasoning
- **Reasoning**: General reasoning across diverse scenarios

## Installation

```bash
# Clone the repository
git clone https://github.com/1AakashK/AGI_Benchmark_Suite.git
cd AGI_Benchmark_Suite

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running with Ollama

This benchmark suite supports testing Ollama models. Make sure you have Ollama installed and running locally.

```bash
# Run all benchmarks with the default Llama2 model
python -m src.main

# Run specific benchmarks with a different model
python -m src.main --model mistral --benchmarks transfer memory

# Save results to a custom file
python -m src.main --output my_results.json
```

### Visualization and Reporting

The benchmark suite includes visualization and reporting capabilities to help analyze results:

```bash
# Run benchmarks and generate visualizations and reports
python -m src.main --visualize

# Specify report format (text, html, or all)
python -m src.main --visualize --report-format html
```

Reports and visualizations are saved to the `reports` directory and include:
- Summary text reports
- Interactive HTML reports
- Benchmark comparison charts
- Task type performance charts

## Benchmark Details

### Transfer Learning

Tests how well an agent can apply knowledge from one task to another related but different task. Inspired by human ability to leverage past experiences for new challenges.

### Memory

Evaluates how well an agent can remember details from previous interactions and use them in current tasks. Tests both short-term and long-term recall abilities.

### Abstraction

Assesses how well an agent can identify patterns and form generalizable concepts from examples. Based on the ARC (Abstraction and Reasoning Corpus) challenge.

### Planning

Measures how well an agent can formulate multi-step plans and adapt them as new information becomes available. Tests both deterministic and stochastic environments.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
