class TablaSimbolos:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def insertar_variable(self, nombre, tipo, ambito):
        if ambito not in self.variables:
            self.variables[ambito] = {}

        if nombre in self.variables[ambito]:
            print(f"Error - Variable '{nombre}' redefinida.")
        else:
            self.variables[ambito][nombre] = tipo

    def buscarVariable(self, nombre, ambito):
        return self.variables.get(ambito, {}).get(nombre, None)

    def comprobarVariableG(self, nombre):
        return self.variables.get("global", {}).get(nombre, None) is not None

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
            # Check if variable_value can be converted to string
            str(variable_value)

            try:
                int(variable_value)
                float(variable_value)

            except:
                return True
        except:
            return False


def guardarEnTablaSimbolos(file_path):
    tablaSimbolos = TablaSimbolos()
    errors = []
    enFuncion = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if '}' in tokens:
            enFuncion = False

        if len(tokens) > 1:
            keyword = tokens[0]

            if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                # Declarar funcion con parametros
                if len(tokens) > 2 and tokens[2] == '(':
                    enFuncion = True
                    function_name = tokens[1]
                    return_type = tokens[0]
                    current_function = function_name

                    tablaSimbolos.insertar_funcion(function_name, return_type)

                    # Guardar parametros

                    i = 4  # Empieza a contar los parametros
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i - 1] == 'int' or tokens[i - 1] == 'float' or tokens[i - 1] == 'string' or tokens[
                            i - 1]:
                            tablaSimbolos.insertar_variable(tokens[i], tokens[i - 1], function_name)
                            i += 3  # Siguiente variable
                else:
                    # Declare variable with type checking
                    variable_name = tokens[1]
                    variable_type = tokens[0]
                    if len(tokens) > 2:
                        variable_value = tokens[3]
                        if validarDato(variable_type, variable_value):
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], "global")
                        else:
                            errors.append(
                                f"Error en línea {line_num}: El valor '{variable_value}' no es una cadena para la "
                                f"variable '{variable_name}'")
                    else:
                        if enFuncion:
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], current_function)
                        else:
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], "global")

            elif keyword == 'if' or keyword == 'while':
                i = 4
                salir = True
                while i < len(tokens) and tokens[i] != '{' and salir == True:
                    v1 = tokens[i]
                    v2 = tokens[i - 1]
                    v3 = tokens[i - 2]

                    # Validar que v1, v2, v3 sean variables
                    if not v1 not in ['(', ')', '{', '}']:
                        errors.append(f"Error - Línea {line_num}: '{v1}' no es una variable válida.")
                    if not v2 not in ['(', ')', '{', '}']:
                        errors.append(f"Error - Línea {line_num}: '{v2}' no es una variable válida.")
                    if not v3 not in ['(', ')', '{', '}']:
                        errors.append(f"Error - Línea {line_num}: '{v3}' no es una variable válida.")

                    variable1_type = tablaSimbolos.buscarVariable(tokens[i - 2], current_function)
                    # variable1_type2 = tablaSimbolos.buscarVariable(tokens[i], current_function)

                    if not tokens[i - 1] in ['==', '!=', '<', '>', '<=', '>=']:
                        salir = False
                        continue

                    if variable1_type is None:
                        variable1_type = tablaSimbolos.buscarVariable(tokens[i - 2], "global")
                        if variable1_type is None:
                            salir = False
                            continue

                    if not validarDato(variable1_type, tokens[i]):
                        errors.append(
                            f"Error - Línea {line_num}: Los tipos de operandos son incompatibles")

                    i += 4
            elif keyword == 'return':
                # Check return type
                expected_return_type = tablaSimbolos.buscarFuncion(current_function)
                variable1_type = tablaSimbolos.buscarVariable(tokens[1], current_function)
                if variable1_type is None:
                    variable1_type = tablaSimbolos.buscarVariable(tokens[1], "global")
                    if variable1_type is None:
                        continue
                if expected_return_type and len(tokens) >= 2 and variable1_type != expected_return_type:
                    errors.append(
                        f"Error - Línea {line_num}: Tipo de retorno incorrecto para la función '{current_function}'.")

            elif not tablaSimbolos.comprobarVariableG(tokens[0]):
                errors.append(
                    f"Error - Línea {line_num}: '{tokens[0]}' No esta declarado")

    if errors:
        for error in errors:
            print(error)
    else:
        print("El código fuente es correcto.")

    return tablaSimbolos


# Ejemplo de uso
file_path = '../codigo_fuente.txt'
print(guardarEnTablaSimbolos(file_path))
