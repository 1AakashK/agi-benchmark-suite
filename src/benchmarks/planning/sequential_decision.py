class SequentialDecisionBenchmark:
    """Benchmark for testing an agent's ability to plan and make sequential decisions.
    
    This benchmark evaluates how well an agent can formulate multi-step plans and
    adapt them as new information becomes available.
    """
    
    def __init__(self, config_path=None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        # Default configuration
        self.config.setdefault('environment_types', ['deterministic', 'stochastic'])
        self.config.setdefault('horizon_lengths', [5, 10, 20])  # Number of steps to plan ahead
        self.config.setdefault('complexity_levels', ['simple', 'complex'])
        
        self.tasks = self._generate_tasks()
    
    def _generate_tasks(self):
        """Generate planning tasks with different environments and horizons."""
        tasks = []
        # Implementation would create planning problems requiring multi-step reasoning
        return tasks
    
    def run(self, agent_interface):
        """Run the planning benchmark on the provided agent."""
        results = {
            'tasks': [],
            'overall_score': 0,
            'environment_scores': {env_type: 0 for env_type in self.config['environment_types']},
            'horizon_scores': {str(horizon): 0 for horizon in self.config['horizon_lengths']}
        }
        
        # Implementation would present planning problems and evaluate solutions
        
        return results