class PushdownAutomaton:
    def __init__(self, input_file):
        # Initialization
        # Initialize automaton components and parse configuration file
        self.states = set()
        self.input_symbols = set()
        self.stack_symbols = set()
        self.start_state = None
        self.accept_states = set()
        self.transitions = {}
        self._load_from_file(input_file)

    def _load_from_file(self, input_file):
        # Configuration Loading
        # Load configuration from a file and set automaton parameters
        with open(input_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("states:"):
                self.states = set(line.split(":")[1].split(","))
            elif line.startswith("input_symbols:"):
                self.input_symbols = set(line.split(":")[1].split(","))
            elif line.startswith("stack_symbols:"):
                self.stack_symbols = set(line.split(":")[1].split(","))
            elif line.startswith("start_state:"):
                self.start_state = line.split(":")[1].strip()
            elif line.startswith("accept_states:"):
                self.accept_states = set(line.split(":")[1].split(","))
            elif line.startswith("transitions:"):
                continue
            elif "->" in line:
                left, right = line.split("->")
                left_parts = left.strip().split()
                right_parts = right.strip().split()

                # Transition parsing
                # Extract transition details from the line
                current_state = left_parts[0]
                input_symbol = left_parts[1]
                stack_top = left_parts[2]
                next_state = right_parts[0]
                stack_action = right_parts[1] if len(right_parts) > 1 else "λ"

                self.transitions[(current_state, input_symbol, stack_top)] = (next_state, stack_action)

    def process_string(self, input_string):
        # String Processing
        # Process an input string and determine acceptance based on transitions
        stack = ['']
        current_state = self.start_state
        steps = []

        for char in input_string:
            steps.append((current_state, char, ''.join(stack)))
            found_transition = False

            for (state, symbol, stack_sym), (next_state, stack_action) in self.transitions.items():
                # Transition matching
                # Check if a transition matches the current state, input, and stack top
                if state == current_state and (symbol == char or symbol == "λ"):
                    top = stack[-1] if stack else ""
                    if stack_sym == top or stack_sym == "λ":
                        found_transition = True
                        current_state = next_state
                        if stack and stack_sym != "λ":
                            stack.pop()
                        if stack_action != "λ":
                            stack.extend(stack_action)
                        break

            if not found_transition:
                steps.append(f"Rejected at state {current_state} with input symbol {char} and stack {''.join(stack)}")
                return False, steps

        steps.append((current_state, "end", ''.join(stack)))
        is_accepted = current_state in self.accept_states
        return is_accepted, steps

if __name__ == "__main__":
    # Main Execution
    # Main execution block to test multiple expressions
    input_file = "input.txt"
    pda = PushdownAutomaton(input_file)

    test_cases = [
        "1*(4+6)$",
        "4+3$",
        "5*(1+2)$",
        "1+4*7$",
        "(9+1)(2-5)$",  # should be rejected
        "4$",
        "*7*(8+9)$",  # should be rejected
        "1/(5+5)$",
        "(1+4)/(7+9)$",
        "9+1$"
    ]
    
    print("\nTesting multiple expressions:")
    for test_expr in test_cases:
        print(f"\nTesting: {test_expr}")
        accepted, steps = pda.process_string(test_expr)
        
        print("Result:", "Accepted" if accepted else "Rejected")
        
        if accepted:
            print("Trace:")
            for step in steps:
                print(step)