import re


class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def insert_variable(self, name, data_type):
        if name in self.variables:
            print(f"Error - Variable '{name}' redefinida.")
        else:
            self.variables[name] = data_type

    def lookup_variable(self, name):
        return self.variables.get(name, None)

    def insert_function(self, name, return_type):
        if name in self.functions:
            print(f"Error - Función '{name}' redefinida.")
        else:
            self.functions[name] = return_type

    def lookup_function(self, name):
        return self.functions.get(name, None)

    def __str__(self):
        return f"Symbol Table:\n\nVariables:\n{self.variables}\n\nFunctions:\n{self.functions}"


def split_parenthesis(linea):
    tokens = []
    current_word = ''
    inside_parentheses = False

    for char in linea:
        if char == '(':
            if current_word:
                tokens.append(current_word)
                current_word = ''
            tokens.append('(')
        elif char == ')':
            if current_word:
                tokens.append(current_word)
                current_word = ''
            tokens.append(')')
        elif char == ' ':
            if current_word:
                tokens.append(current_word)
                current_word = ''
        elif char == ',':
            if current_word:
                tokens.append(current_word)
                current_word = ''
            tokens.append(',')
        else:
            if char != '\t':
                current_word += char

    if current_word:
        tokens.append(current_word)

    if tokens[-1].endswith('\n'):
        tokens[-1] = tokens[-1].rstrip('\n')

    return tokens

def guardarEnTablaSimbolos(file_path):

    symbol_table = SymbolTable()
    errors = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 1:
            keyword = tokens[0]

            if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                # Function declaration with parameters
                if tokens[2] == '(':
                    function_name = tokens[1]
                    return_type = tokens[0]

                    symbol_table.insert_function(function_name, return_type)

                    # Extract and save function parameters

                    i = 4  # Index of first parameter
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i] == ',':
                            symbol_table.insert_variable(tokens[i-1], tokens[i-2])
                            i += 2  # Move to next parameter
                        else:
                            symbol_table.insert_variable(tokens[i], tokens[i-1])
                            i += 3  # Move to next parameter
                else:
                    # Variable declaration
                    symbol_table.insert_variable(tokens[1], tokens[0])
    return symbol_table

def analyze_code(file_path):
    symbol_table = SymbolTable()
    errors = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 1:
            keyword = tokens[0]
            last = tokens[-1]

            # comprueba declaraciones de variables solas
            if last != '{':
                if keyword == 'int' or keyword == 'float' or keyword == 'string':
                        symbol_table.insert_variable(tokens[1], tokens[0])
                else:
                    print(f"Error - Línea {line_num}: Declaración de variable '{tokens[1]}' invalida.")

            # comprueba declaraciones de funciones
            if last == '{':
                if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                    # Function declaration
                    if len(tokens) >= 4:
                        function_name = tokens[1]
                        return_type = tokens[0]
                        symbol_table.insert_function(function_name, return_type)
                        current_function = function_name
                    else:
                        errors.append(f"Error - Línea {line_num}: Declaración de función incompleta.")

            elif keyword == '}':
                # End of function scope
                current_function = None

            # revisa que el retorno sea correcto
            elif current_function:
                # Inside a function
                if keyword == 'return':
                    # Check return type
                    expected_return_type = symbol_table.lookup_function(current_function)
                    if expected_return_type and len(tokens) >= 2 and tokens[1] != expected_return_type:
                        errors.append(
                            f"Error - Línea {line_num}: Tipo de retorno incorrecto para la función '{current_function}'.")

                elif keyword == 'if' or keyword == 'while':
                    # Add your code to handle if/while statements inside functions
                    pass

                # else:
            # Assignment or other statements inside a function
            # Add your code to handle assignments and other statements

            else:
                errors.append(f"Error - Línea {line_num}: Uso de la palabra clave '{keyword}' fuera de una función.")

    # Print errors
    if errors:
        for error in errors:
            print(error)
    else:
        print("El código fuente es correcto.")


# Ejemplo de uso
file_path = '../codigo_fuente.txt'
print(guardarEnTablaSimbolos(file_path))