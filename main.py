class TablaSimbolos:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def insertar_variable(self, nombre, tipo):
        if nombre in self.variables:
            print(f"Error - Variable '{nombre}' redefinida.")
        else:
            self.variables[nombre] = tipo

    def buscarVariable(self, nombre):
        return self.variables.get(nombre, None)

    def insertar_funcion(self, nombre, tipoRetorno):
        if nombre in self.funciones:
            print(f"Error - Función '{nombre}' redefinida.")
        else:
            self.funciones[nombre] = tipoRetorno

    def buscarFuncion(self, name):
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
            if char != '\t' and char != '\n' and char != '"':
                palabra += char

    if palabra:
        tokens.append(palabra)

    return tokens


def validarDato(variable_type, variable_value):
    if variable_type == 'int':
        try:
            int(variable_value)
            return True
        except:
            return False
    elif variable_type == 'float':
        try:
            float(variable_value)
            return True
        except:
            return False
    elif variable_type == 'string':
        try:
            str(variable_value)
            return True
        except:
            return False


def guardarEnTablaSimbolos(file_path):
    tablaSimbolos = TablaSimbolos()
    errors = []

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

                    tablaSimbolos.insertar_funcion(function_name, return_type)

                    # Guardar parametros

                    i = 4  # Primer parametro despues de (
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i] == ',':
                            tablaSimbolos.insertar_variable(tokens[i - 1], tokens[i - 2])
                            i += 2  # Siguiente variable
                        else:
                            tablaSimbolos.insertar_variable(tokens[i], tokens[i - 1])
                            i += 3  # Siguiente variable
                else:
                    # Declare variable with type checking
                    variable_name = tokens[1]
                    variable_type = tokens[0]
                    variable_value = tokens[3]

                    if validarDato(variable_type, variable_value):
                        tablaSimbolos.insertar_variable(tokens[1], tokens[0])
                    else:
                        errors.append(f"Error en línea {line_num}: El valor '{variable_value}' no es una cadena para la variable '{variable_name}'")
            elif keyword in tablaSimbolos:
                i = 0
                variable_name = tokens[1]
                variable_type = tokens[0]
                while i < len(tokens):

    return tablaSimbolos





def analizar(file_path):
    symbol_table = guardarEnTablaSimbolos(file_path)
    errors = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 1:
            keyword = tokens[0]
            last = tokens[-1]


def analyze_code(file_path):
    symbol_table = guardarEnTablaSimbolos(file_path)
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
                    print("sd")
            else:
                print(f"Error - Línea {line_num}: Declaración de variable '{tokens[1]}' invalida.")

            # comprueba declaraciones de funciones
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

            # revisa que el retorno sea correcto
            elif current_function:
                # Inside a function
                if keyword == 'return':
                    # Check return type
                    expected_return_type = symbol_table.buscarFuncion(current_function)
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
