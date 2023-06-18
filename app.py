import streamlit as st
from string import ascii_letters, digits
import re

SPACE, TAB, NEWLINE = (' ', '\t', '\n')

class LexicalAnalyzer:
    def __init__(self):
        self.transitions = {}
        self.accepted_states = set()
        self.init_state = None
        self.current_state = None
        self.current_token = ''
        self.tokens = []
        self.token_types = []

    def add_init_state(self, state):
        self.init_state = state
    
    def add_transition(self, state, read, target_state):
        for char in read:
            self.transitions[(state, char)] = target_state

    def add_accepted_state(self, state):
        self.accepted_states.add(state)
    
    def analyze(self, input_str, verbose=False):
        if not input_str.endswith('#'):
            input_str = input_str + '#'

        cursor_pos = 0
        self.current_state = self.init_state
        self.current_token = ''

        while cursor_pos < len(input_str):
            is_accepted = self.current_state in self.accepted_states

            if verbose:
                print({
                    'current_state': self.current_state,
                    'current_token': self.current_token,
                    'input': input_str[cursor_pos],
                    'is_accepted': is_accepted
                })

            if is_accepted and input_str[cursor_pos] in [' ', '#', ':'] and self.current_token:
                self.tokens.append(self.current_token)
                self.current_token = ''

            if input_str[cursor_pos] not in [NEWLINE, TAB, SPACE]:
                self.current_token += input_str[cursor_pos]

            current_state = self.transitions.get((self.current_state, input_str[cursor_pos]))
            
            if not current_state:
                break
            
            self.current_state = current_state
            cursor_pos += 1
             
        return self.tokens, self.current_state, input_str[cursor_pos:-1]
  

with st.sidebar:
    st.title('Lexical Analyzer & Parser')
    st.subheader('''
by Kelompok 4 (IF-45-10)
1. Widya Yudha Patria (1301213015)
2. Nizam Abdullah (1301213232)
3. Rangga Aditya Pratama (1301213466)''')

lexical = LexicalAnalyzer()

# add init state
lexical.add_init_state('q0')

# handle newline at first line
lexical.add_transition('q0', NEWLINE, 'q0')

# handle for 'while' statement
lexical.add_transition('q0', 'w', 'q1')
lexical.add_transition('q1', 'h', 'q2')
lexical.add_transition('q2', 'i', 'q3')
lexical.add_transition('q3', 'l', 'q4')
lexical.add_transition('q4', 'e', 'q5')

# space or tab after 'while' statement
lexical.add_transition('q5', f'{SPACE}{TAB}', 'q5')

lexical.add_accepted_state('q5')

# Rule named variable python:
#     1. Variable name must start with a letter or the underscore character

# handle variable on while 'condition'
lexical.add_transition('q5', ascii_letters + '_', 'a1')
lexical.add_transition('a1', ascii_letters + digits + '_', 'a1')

lexical.add_accepted_state('a1')

# handle space or tab
lexical.add_transition('a1', f'{SPACE}{TAB}', 'a1')

# handle comparison operator '<, >, =, !'
lexical.add_transition('a1', '<>=!', 'a2')
lexical.add_accepted_state('a2')

# handle space or tab
lexical.add_transition('a2', f'{SPACE}{TAB}', 'a3')

# handle comparison operator '<=, >=, ==, !=', add '=' at after '<, >, =, !'
lexical.add_transition('a2', '=', 'a3')
lexical.add_accepted_state('a3')

# handle space or tab
lexical.add_transition('a3', f'{SPACE}{TAB}', 'a3')

# handle variable on while 'condition'
lexical.add_transition('a2', ascii_letters + '_', 'a4')
lexical.add_transition('a3', ascii_letters + '_', 'a4')
lexical.add_transition('a4', ascii_letters + digits + '_', 'a4')

# handle space or tab after variable
lexical.add_transition('a4', f'{SPACE}{TAB}', 'a5')
lexical.add_transition('a5', f'{SPACE}{TAB}', 'a5')

# accept state
lexical.add_accepted_state('a4')
lexical.add_accepted_state('a5')

# handle ':' after statement condition
lexical.add_transition('a4', ':', 'b0')
lexical.add_transition('a5', ':', 'b0')

# accept state
lexical.add_accepted_state('b0')

# handle space or tab ':'
lexical.add_transition('b0', f'{SPACE}{TAB}', 'b0')

# newline after statement
lexical.add_transition('b0', NEWLINE, 'b1')

lexical.add_accepted_state('b0')

# handle newline without action
lexical.add_transition('b1', NEWLINE, 'b1')

# start 'action' statement
lexical.add_transition('b1', f'{SPACE}', 'tab1')
lexical.add_transition('tab1', f'{SPACE}', 'tab2')
lexical.add_transition('tab2', f'{SPACE}', 'tab3')
lexical.add_transition('tab3', f'{SPACE}', 'tab4')

lexical.add_transition('b1', TAB, 'tab4')

# if 'action' statement is empty 
lexical.add_accepted_state('b1')

# handle variable on while 'condition'
lexical.add_transition('tab4', ascii_letters + '_', 'b2')
lexical.add_transition('b2', ascii_letters + digits + '_', 'b2')

lexical.add_accepted_state('b2')
lexical.add_transition('b2', '=', 'b4')

# handle space or tab after variable
lexical.add_transition('b2', f'{SPACE}{TAB}', 'b3')
lexical.add_transition('b3', f'{SPACE}{TAB}', 'b3')

# assignment operator '='
lexical.add_transition('b3', '=', 'b4')

lexical.add_accepted_state('b4')

# handle space or tab after assignment operator
lexical.add_transition('b4', f'{SPACE}{TAB}', 'b4')

# handle variable after assignment operator
lexical.add_transition('b4', ascii_letters + '_', 'b5')
lexical.add_transition('b5', ascii_letters + digits + '_', 'b5')

lexical.add_accepted_state('b5')

# handle space or tab after variable
lexical.add_transition('b5', f'{SPACE}{TAB}', 'b5')

# handle arithmetics operator '+, -, *'
lexical.add_transition('b5', '+-', 'b6')
lexical.add_transition('b6', f'{SPACE}{TAB}', 'b6')

# handle arithmetics operator '/, //'
lexical.add_transition('b5', '/', 'c1')
lexical.add_transition('c1', f'{SPACE}{TAB}', 'c1')

lexical.add_transition('c1', '/', 'b7')
lexical.add_transition('b7', f'{SPACE}{TAB}', 'b7')

# handle arithmetics operator '*, **'
lexical.add_transition('b5', '*', 'd1')
lexical.add_transition('d1', f'{SPACE}{TAB}', 'd1')

lexical.add_transition('d1', '*', 'b10')
lexical.add_transition('b10', f'{SPACE}{TAB}', 'b10')


lexical.add_accepted_state('b6')
lexical.add_accepted_state('b7')
lexical.add_accepted_state('b10')
lexical.add_accepted_state('c1')
lexical.add_accepted_state('d1')


# handle integer
lexical.add_transition('b6', digits, 'b9')
lexical.add_transition('b7', digits, 'b9')
lexical.add_transition('b10', digits, 'b9')
lexical.add_transition('c1', digits, 'b9')
lexical.add_transition('d1', digits, 'b9')

# loop integer
lexical.add_transition('b9', digits, 'b9')

# handle variable on while 'condition'
lexical.add_transition('b6', ascii_letters + '_', 'b8')
lexical.add_transition('b7', ascii_letters + '_', 'b8')
lexical.add_transition('b10', ascii_letters + '_', 'b8')
lexical.add_transition('c1', ascii_letters + '_', 'b8')
lexical.add_transition('d1', ascii_letters + '_', 'b8')
lexical.add_transition('b8', ascii_letters + digits + '_', 'b8')

lexical.add_transition('b8', f'{SPACE}{TAB}{NEWLINE}', 'b8') 
lexical.add_accepted_state('b8')

lexical.add_transition('b8', NEWLINE, 'b1')
lexical.add_transition('b8', '#', 'accept')

lexical.add_transition('b9', f'{SPACE}{TAB}', 'b9')
lexical.add_accepted_state('b9')

lexical.add_transition('b9', NEWLINE, 'b1')
lexical.add_transition('b9', '#', 'accept')

st.title("Python While Statement Lexer")
st.write("Example:")
st.code("""while x < y:
    x = x + y
    y = y + 1
        """, language="python")

code = st.text_area("Input Python Code", height=200)

grammar = ['WHILE', 'VARIABLE', 'COMPARISON_OPERATOR', 'VARIABLE', 'COLON', 
            'VARIABLE', 'ASSIGNMENT_OPERATOR', 'VARIABLE', 'ARITHMETICS_OPERATOR', ['VARIABLE', 'VALUE']]
grammar_pos = 0

if st.button("Analyze"):
    if not code:
        st.error("Please input your code! :rage:")
    else:
        tokens, final_state, inp = lexical.analyze(code, verbose = False)
        st.subheader("Lexical Analyzer Checker")
        if final_state == 'accept':
            st.success("Your code is valid! :slightly_smiling_face:")
        else:
            st.error(f"Your code is invalid! Error occurred at **{inp}** :weary: ")
            
        st.subheader("Token Analysis Result")
        for token in tokens:
            token_col, type_col = st.columns([8, 6])
            with token_col:
                st.info(f'Token: "{token}"')
            with type_col:
                token_type = grammar[grammar_pos]
                if isinstance(token_type, list):
                    if token.isdigit():
                        token_type = token_type[1]
                    else:
                        token_type = token_type[0]
                st.success(f'Type: {token_type}')
                grammar_pos += 1
                if grammar_pos >= len(grammar):
                    grammar_pos = 5
                