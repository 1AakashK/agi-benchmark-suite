import os
import json
from ...utils.evaluation import evaluate_response

class TaskAdaptationBenchmark:
    """Benchmark for testing an agent's ability to adapt to new tasks.
    
    This benchmark tests how well an agent can apply knowledge from one task to another
    related but different task without explicit retraining.
    """
    
    def __init__(self, config_path=None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        # Default configuration
        self.config.setdefault('difficulty_levels', ['easy', 'medium', 'hard'])
        self.config.setdefault('num_tasks', 5)
        self.config.setdefault('time_limit', 300)  # seconds
        
        self.tasks = self._generate_tasks()
    
    def _generate_tasks(self):
        """Generate a series of related tasks with increasing difficulty."""
        tasks = []
        # Implementation would generate task pairs where knowledge from the first
        # should transfer to the second
        return tasks
    
    def run(self, agent_interface):
        """Run the benchmark on the provided agent interface.
        
        Args:
            agent_interface: An object with a 'solve' method that takes a task description
                            and returns a solution.
        
        Returns:
            dict: Results including scores, timing, and analysis of transfer efficiency.
        """
        results = {
            'tasks': [],
            'overall_score': 0,
            'transfer_efficiency': 0
        }
        
        for i, task_pair in enumerate(self.tasks):
            # First task - baseline performance
            base_task, transfer_task = task_pair
            
            base_result = self._evaluate_task(agent_interface, base_task)
            transfer_result = self._evaluate_task(agent_interface, transfer_task)
            
            # Calculate transfer efficiency
            transfer_efficiency = self._calculate_transfer_efficiency(base_result, transfer_result)
            
            results['tasks'].append({
                'base_task': base_result,
                'transfer_task': transfer_result,
                'transfer_efficiency': transfer_efficiency
            })
            
            results['overall_score'] += (base_result['score'] + transfer_result['score']) / 2
            results['transfer_efficiency'] += transfer_efficiency
        
        # Normalize scores
        if self.tasks:
            results['overall_score'] /= len(self.tasks)
            results['transfer_efficiency'] /= len(self.tasks)
        
        return results
    
    def _evaluate_task(self, agent_interface, task):
        """Evaluate an agent on a single task."""
        start_time = time.time()
        solution = agent_interface.solve(task['description'])
        solve_time = time.time() - start_time
        
        score = evaluate_response(solution, task['expected_solution'])
        
        return {
            'task_id': task['id'],
            'score': score,
            'time': solve_time,
            'solution': solution
        }
    
    def _calculate_transfer_efficiency(self, base_result, transfer_result):
        """Calculate how efficiently knowledge transferred from base to transfer task."""
        # A simple metric: ratio of scores adjusted by time
        if base_result['score'] == 0:
            return 0
        
        # Higher score in less time indicates good transfer
        score_ratio = transfer_result['score'] / base_result['score']
        time_ratio = base_result['time'] / max(transfer_result['time'], 0.001)  # Avoid division by zero
        
        return score_ratio * time_ratio