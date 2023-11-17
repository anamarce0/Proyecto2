class TablaSimbolos:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def insertar_variable(self, nombre, tipo):
        if nombre in self.variables:
            print(f"Error - Variable '{nombre}' redefinida.")
        else:
            self.variables[nombre] = tipo

    def buscar(self, nombre):
        return self.variables.get(nombre, None)

    def insertar_funcion(self, nombre, tipoRetorno):
        if nombre in self.funciones:
            print(f"Error - Función '{nombre}' redefinida.")
        else:
            self.funciones[nombre] = tipoRetorno

    def lookup_function(self, name):
        return self.funciones.get(name, None)

    def __str__(self):
        return f"Symbol Table:\n\nVariables:\n{self.variables}\n\nFunctions:\n{self.funciones}"


def split_parenthesis(linea):
    tokens = []
    palabra = ''

    for char in linea:
        if char == '(':
            if palabra:
                tokens.append(palabra)
                palabra = ''
            tokens.append('(')
        elif char == ')':
            if palabra:
                tokens.append(palabra)
                palabra = ''
            tokens.append(')')
        elif char == ' ':
            if palabra:
                tokens.append(palabra)
                palabra = ''
        elif char == ',':
            if palabra:
                tokens.append(palabra)
                palabra = ''
            tokens.append(',')
        else:
            if char != '\t' and char != '\n':
                palabra += char

    if palabra:
        tokens.append(palabra)

    return tokens

def guardarEnTablaSimbolos(file_path):
    tablaSimbolos = TablaSimbolos()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 1:
            keyword = tokens[0]

            if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                # Declarar funcion con parametros
                if tokens[2] == '(':
                    function_name = tokens[1]
                    return_type = tokens[0]

                    if tablaSimbolos.lookup_function(function_name):
                        print(f"Error - Línea {line_num}: Función '{function_name}' redefinida.")
                    else:
                        tablaSimbolos.insertar_funcion(function_name, return_type)

                    # Guardar parametros
                    i = 4  # Primer parametro después de (
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i] == ',':
                            tablaSimbolos.insertar_variable(tokens[i - 1], tokens[i - 2])
                            i += 2  # Siguiente variable
                        else:
                            tablaSimbolos.insertar_variable(tokens[i], tokens[i - 1])
                            i += 3  # Siguiente variable
                else:
                    # Declarar variable
                    tablaSimbolos.insertar_variable(tokens[1], tokens[0])

    return tablaSimbolos

def analyze_code(file_path, symbol_table):
    errors = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 1:
            keyword = tokens[0]
            last = tokens[-1]

            # Check if it's a variable declaration or assignment
            if '=' in tokens:
                variable_name = tokens[tokens.index('=') - 1]
                variable_type = symbol_table.buscar(variable_name)

                if variable_type is None:
                    errors.append(f"Error - Línea {line_num}: Uso de variable no declarada '{variable_name}'.")

            # Check declaraciones de variables
            elif last != '{':
                if keyword == 'int' or keyword == 'float' or keyword == 'string':
                    symbol_table.insertar_variable(tokens[1], tokens[0])
                else:
                    errors.append(f"Error - Línea {line_num}: Declaración de variable '{tokens[1]}' invalida.")

            # Check declaraciones de funciones
            if last == '{':
                if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                    # Function declaration
                    if len(tokens) >= 4:
                        function_name = tokens[1]
                        return_type = tokens[0]
                        symbol_table.insertar_funcion(function_name, return_type)
                        current_function = function_name
                    else:
                        errors.append(f"Error - Línea {line_num}: Declaración de función incompleta.")

            elif keyword == '}':
                # End of function scope
                current_function = None

            # Revisar que el retorno sea correcto
            elif current_function:
                # Inside a function
                if keyword == 'return':
                    # Check if the function has a return type
                    expected_return_type = symbol_table.lookup_function(current_function)
                    if not expected_return_type:
                        errors.append(
                            f"Error - Línea {line_num}: La función '{current_function}' no tiene tipo de retorno declarado.")
                    else:
                        # Check if the return type matches the expected return type
                        if len(tokens) >= 2:
                            returned_value_type = symbol_table.buscar(tokens[1])
                            if returned_value_type != expected_return_type:
                                errors.append(
                                    f"Error - Línea {line_num}: Tipo de retorno incorrecto para la función '{current_function}'.")
                        else:
                            errors.append(
                                f"Error - Línea {line_num}: Falta valor de retorno para la función '{current_function}'.")

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
file_path = 'codigo_fuente.txt'
symbol_table = guardarEnTablaSimbolos(file_path)
analyze_code(file_path, symbol_table)