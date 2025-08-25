import argparse
import json
import os

from src.utils.agent_interfaces import OllamaInterface
from src.utils.visualization import BenchmarkVisualizer
from src.benchmarks.transfer.task_adaptation import TaskAdaptationBenchmark
from src.benchmarks.memory.episodic_memory import EpisodicMemoryBenchmark
from src.benchmarks.abstraction.concept_formation import ConceptFormationBenchmark
from src.benchmarks.planning.sequential_decision import SequentialDecisionBenchmark
from src.domains.code.code_generation import CodeGenerationBenchmark
from src.domains.vision.visual_reasoning import VisualReasoningBenchmark

def main():
    parser = argparse.ArgumentParser(description='Run AGI Benchmark Suite')
    parser.add_argument('--model', type=str, default='gemma3:latest', help='Ollama model to use')
    parser.add_argument('--benchmarks', type=str, nargs='+', 
                        choices=['transfer', 'memory', 'abstraction', 'planning', 'code', 'vision', 'all'],
                        default=['all'], help='Benchmarks to run')
    parser.add_argument('--output', type=str, default='results.json', help='Output file for results')
    parser.add_argument('--visualize', action='store_true', help='Generate visualization and reports')
    parser.add_argument('--report-format', type=str, choices=['text', 'html', 'all'], default='all',
                       help='Report format to generate')
    args = parser.parse_args()
    
    # Initialize agent interface
    agent = OllamaInterface(model_name=args.model)
    
    # Determine which benchmarks to run
    benchmarks_to_run = []
    if 'all' in args.benchmarks or 'transfer' in args.benchmarks:
        benchmarks_to_run.append(('Transfer Learning', TaskAdaptationBenchmark()))
    if 'all' in args.benchmarks or 'memory' in args.benchmarks:
        benchmarks_to_run.append(('Episodic Memory', EpisodicMemoryBenchmark()))
    if 'all' in args.benchmarks or 'abstraction' in args.benchmarks:
        benchmarks_to_run.append(('Concept Formation', ConceptFormationBenchmark()))
    if 'all' in args.benchmarks or 'planning' in args.benchmarks:
        benchmarks_to_run.append(('Sequential Decision', SequentialDecisionBenchmark()))
    if 'all' in args.benchmarks or 'code' in args.benchmarks:
        benchmarks_to_run.append(('Code Generation', CodeGenerationBenchmark()))
    if 'all' in args.benchmarks or 'vision' in args.benchmarks:
        benchmarks_to_run.append(('Visual Reasoning', VisualReasoningBenchmark()))
    
    # Run benchmarks and collect results
    results = {
        'model': args.model,
        'benchmarks': {}
    }
    
    for name, benchmark in benchmarks_to_run:
        print(f"Running {name} benchmark...")
        benchmark_results = benchmark.run(agent)
        results['benchmarks'][name] = benchmark_results
        print(f"Completed {name} benchmark. Overall score: {benchmark_results['overall_score']:.2f}")
    
    # Calculate aggregate scores
    if results['benchmarks']:
        results['overall_score'] = sum(b['overall_score'] for b in results['benchmarks'].values()) / len(results['benchmarks'])
    else:
        results['overall_score'] = 0.0
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAll benchmarks completed.")
    print(f"Overall AGI score: {results['overall_score']:.2f}")
    print(f"Detailed results saved to {args.output}")
    
    # Generate visualizations and reports if requested
    if args.visualize:
        print("\nGenerating visualizations and reports...")
        visualizer = BenchmarkVisualizer(results_data=results)
        
        # Generate reports based on format
        if args.report_format in ['text', 'all']:
            summary_file = visualizer.generate_summary_report()
            print(f"Summary report saved to {summary_file}")
            
        if args.report_format in ['html', 'all']:
            html_report = visualizer.generate_html_report()
            print(f"HTML report saved to {html_report}")
        
        # Always generate charts
        overall_chart = visualizer.plot_overall_comparison()
        print(f"Overall comparison chart saved to {overall_chart}")
        
        task_chart = visualizer.plot_task_type_comparison()
        if task_chart:
            print(f"Task type comparison chart saved to {task_chart}")

if __name__ == '__main__':
    main()