class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, transitions, initial_state, accept_state, reject_state):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.current_state = initial_state
        self.tape = []
        self.head_position = 0

    def reset(self, input_word):
        self.tape = list(input_word) + ['_']
        self.head_position = 0
        self.current_state = self.initial_state

    def step(self):
        current_symbol = self.tape[self.head_position]

        if (self.current_state, current_symbol) in self.transitions:
            next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol
            if direction == 'R':
                self.head_position += 1
                if self.head_position >= len(self.tape):
                    self.tape.append('_')
            elif direction == 'L':
                self.head_position = max(0, self.head_position - 1)
            self.current_state = next_state
        else:
            self.current_state = self.reject_state

    def simulate(self, word):
        current_state = self.initial_state
        tape = list(word) + [' ']  # Adiciona um espaço em branco ao final da fita
        head_position = 0

        while current_state != self.accept_state and current_state != self.reject_state:
            if head_position < 0 or head_position >= len(tape):
                return "rejeitada"  # Se a cabeça sair da fita, rejeita

            symbol = tape[head_position]
            if (current_state, symbol) not in self.transitions:
                return "rejeitada"

            next_state, write_symbol, direction = self.transitions[(current_state, symbol)]
            tape[head_position] = write_symbol
            current_state = next_state
            if direction == 'L':
                head_position -= 1
            elif direction == 'R':
                head_position += 1
            else:
                return "rejeitada"

        return "aceita" if current_state == self.accept_state else "rejeitada"