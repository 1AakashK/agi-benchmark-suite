def evaluate_response(response, expected, metric='exact_match'):
    """Evaluate a response against an expected answer.
    
    Args:
        response: The agent's response
        expected: The expected correct response
        metric: The evaluation metric to use
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if metric == 'exact_match':
        return 1.0 if response == expected else 0.0
    elif metric == 'token_overlap':
        # Simple token overlap for text responses
        response_tokens = set(response.lower().split())
        expected_tokens = set(expected.lower().split())
        if not expected_tokens:
            return 0.0
        return len(response_tokens.intersection(expected_tokens)) / len(expected_tokens)
    elif metric == 'execution_result':
        # For code, evaluate based on execution results
        # Implementation would execute code and compare outputs
        pass
    else:
        raise ValueError(f"Unknown evaluation metric: {metric}")