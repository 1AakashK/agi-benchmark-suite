import matplotlib.pyplot as plt
import numpy as np
import os
import json
from datetime import datetime

class BenchmarkVisualizer:
    """Visualizer for AGI benchmark results.
    
    This class provides methods to generate various visualizations and reports
    from benchmark results.
    """
    
    def __init__(self, results_file=None, results_data=None):
        """Initialize the visualizer with either a results file or data.
        
        Args:
            results_file: Path to a JSON file containing benchmark results
            results_data: Dictionary containing benchmark results
        """
        self.results = None
        
        if results_file and os.path.exists(results_file):
            with open(results_file, 'r') as f:
                self.results = json.load(f)
        elif results_data:
            self.results = results_data
            
        self.output_dir = 'reports'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_summary_report(self, output_file=None):
        """Generate a text summary report of benchmark results.
        
        Args:
            output_file: Path to save the report (default: reports/summary_YYYY-MM-DD.txt)
            
        Returns:
            str: Path to the generated report file
        """
        if not self.results:
            raise ValueError("No results data available")
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = os.path.join(self.output_dir, f"summary_{timestamp}.txt")
            
        with open(output_file, 'w') as f:
            f.write(f"AGI Benchmark Suite - Results Summary\n")
            f.write(f"=====================================\n\n")
            f.write(f"Model: {self.results.get('model', 'Unknown')}\n")
            f.write(f"Overall Score: {self.results.get('overall_score', 0):.2f}\n\n")
            
            f.write(f"Benchmark Scores:\n")
            f.write(f"----------------\n")
            
            for name, data in self.results.get('benchmarks', {}).items():
                f.write(f"{name}: {data.get('overall_score', 0):.2f}\n")
                
                # Add detailed metrics if available
                if 'transfer_efficiency' in data:
                    f.write(f"  Transfer Efficiency: {data.get('transfer_efficiency', 0):.2f}\n")
                if 'decay_rate' in data:
                    f.write(f"  Memory Decay Rate: {data.get('decay_rate', 0):.2f}\n")
                    
                # Add task-specific scores
                if 'task_type_scores' in data:
                    f.write(f"  Task Type Scores:\n")
                    for task_type, score in data['task_type_scores'].items():
                        f.write(f"    {task_type}: {score:.2f}\n")
                        
                f.write("\n")
                
        return output_file
    
    def plot_overall_comparison(self, output_file=None):
        """Generate a bar chart comparing overall benchmark scores.
        
        Args:
            output_file: Path to save the chart (default: reports/overall_comparison_YYYY-MM-DD.png)
            
        Returns:
            str: Path to the generated chart file
        """
        if not self.results:
            raise ValueError("No results data available")
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = os.path.join(self.output_dir, f"overall_comparison_{timestamp}.png")
        
        benchmark_names = []
        scores = []
        
        for name, data in self.results.get('benchmarks', {}).items():
            benchmark_names.append(name)
            scores.append(data.get('overall_score', 0))
            
        plt.figure(figsize=(10, 6))
        bars = plt.bar(benchmark_names, scores, color='skyblue')
        
        # Add score labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height:.2f}', ha='center', va='bottom')
        
        plt.axhline(y=self.results.get('overall_score', 0), color='r', linestyle='-', 
                   label=f"Overall: {self.results.get('overall_score', 0):.2f}")
        
        plt.ylim(0, 1.1)  # Assuming scores are between 0 and 1
        plt.title(f"AGI Benchmark Results - {self.results.get('model', 'Unknown')}")
        plt.ylabel('Score')
        plt.legend()
        plt.tight_layout()
        
        plt.savefig(output_file)
        plt.close()
        
        return output_file
    
    def plot_task_type_comparison(self, output_file=None):
        """Generate a grouped bar chart comparing task type scores across benchmarks.
        
        Args:
            output_file: Path to save the chart (default: reports/task_comparison_YYYY-MM-DD.png)
            
        Returns:
            str: Path to the generated chart file
        """
        if not self.results:
            raise ValueError("No results data available")
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = os.path.join(self.output_dir, f"task_comparison_{timestamp}.png")
        
        # Collect all task types across benchmarks
        all_task_types = set()
        for data in self.results.get('benchmarks', {}).values():
            if 'task_type_scores' in data:
                all_task_types.update(data['task_type_scores'].keys())
        
        if not all_task_types:
            return None  # No task type data available
        
        all_task_types = sorted(list(all_task_types))
        benchmark_names = list(self.results.get('benchmarks', {}).keys())
        
        # Prepare data for grouped bar chart
        data = []
        for task_type in all_task_types:
            task_scores = []
            for name in benchmark_names:
                benchmark_data = self.results.get('benchmarks', {}).get(name, {})
                score = benchmark_data.get('task_type_scores', {}).get(task_type, 0)
                task_scores.append(score)
            data.append(task_scores)
        
        # Create grouped bar chart
        fig, ax = plt.subplots(figsize=(12, 7))
        
        x = np.arange(len(benchmark_names))
        width = 0.8 / len(all_task_types)
        
        for i, (task_type, scores) in enumerate(zip(all_task_types, data)):
            offset = width * i - width * len(all_task_types) / 2 + width / 2
            ax.bar(x + offset, scores, width, label=task_type)
        
        ax.set_xticks(x)
        ax.set_xticklabels(benchmark_names)
        ax.set_ylim(0, 1.1)  # Assuming scores are between 0 and 1
        ax.set_ylabel('Score')
        ax.set_title(f"Task Type Performance Across Benchmarks - {self.results.get('model', 'Unknown')}")
        ax.legend(title="Task Types")
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return output_file
    
    def generate_html_report(self, output_file=None):
        """Generate a comprehensive HTML report with embedded charts.
        
        Args:
            output_file: Path to save the HTML report (default: reports/report_YYYY-MM-DD.html)
            
        Returns:
            str: Path to the generated HTML report
        """
        if not self.results:
            raise ValueError("No results data available")
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = os.path.join(self.output_dir, f"report_{timestamp}.html")
        
        # Generate charts for embedding
        chart_dir = os.path.join(self.output_dir, 'charts')
        os.makedirs(chart_dir, exist_ok=True)
        
        overall_chart = os.path.join(chart_dir, 'overall.png')
        self.plot_overall_comparison(overall_chart)
        
        task_chart = os.path.join(chart_dir, 'tasks.png')
        self.plot_task_type_comparison(task_chart)
        
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AGI Benchmark Report - {self.results.get('model', 'Unknown')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #333; }}
                .chart {{ margin: 20px 0; text-align: center; }}
                .chart img {{ max-width: 100%; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>AGI Benchmark Suite - Results Report</h1>
            <p><strong>Model:</strong> {self.results.get('model', 'Unknown')}</p>
            <p><strong>Overall Score:</strong> {self.results.get('overall_score', 0):.2f}</p>
            
            <h2>Benchmark Comparison</h2>
            <div class="chart">
                <img src="charts/overall.png" alt="Overall Benchmark Comparison">
            </div>
            
            <h2>Task Type Performance</h2>
            <div class="chart">
                <img src="charts/tasks.png" alt="Task Type Performance">
            </div>
            
            <h2>Detailed Results</h2>
        """
        
        # Add detailed results table
        html_content += """
            <table>
                <tr>
                    <th>Benchmark</th>
                    <th>Overall Score</th>
                    <th>Details</th>
                </tr>
        """
        
        for name, data in self.results.get('benchmarks', {}).items():
            details = []
            
            if 'transfer_efficiency' in data:
                details.append(f"Transfer Efficiency: {data.get('transfer_efficiency', 0):.2f}")
            if 'decay_rate' in data:
                details.append(f"Memory Decay Rate: {data.get('decay_rate', 0):.2f}")
                
            # Add task-specific scores
            if 'task_type_scores' in data:
                task_details = []
                for task_type, score in data['task_type_scores'].items():
                    task_details.append(f"{task_type}: {score:.2f}")
                if task_details:
                    details.append("Task Scores: " + ", ".join(task_details))
            
            details_str = "<br>".join(details) if details else "No detailed metrics available"
            
            html_content += f"""
                <tr>
                    <td>{name}</td>
                    <td>{data.get('overall_score', 0):.2f}</td>
                    <td>{details_str}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>Test Environment</h2>
            <p>Report generated on {timestamp}</p>
            
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        with open(output_file, 'w') as f:
            f.write(html_content)
            
        return output_file