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


def validarDatoEnTabla(tablaSimbolos, variable_type, variable_value, current_function):
    existing_type = tablaSimbolos.buscarVariable(variable_value, current_function)
    if existing_type is not None and existing_type != variable_type:
        # Try converting the variable_value to the expected type
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
    else:
        return True


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
                return True
            except:
                return True
        except:
            return False


def guardarEnTablaSimbolos(file_path):
    tablaSimbolos = TablaSimbolos()
    errors = []
    enFuncion = False
    enCondicion = False
    cantPar = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_function = None

    for line_num, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 0:
            keyword = tokens[0]

            if '}' in tokens:
                cantPar -= 1
                continue

            if '{' in tokens:
                cantPar += 1

            if cantPar == 0:
                ambito = "global"
            elif cantPar == 1:
                ambito = current_function
            else:
                ambito = 'condicion'

            if keyword == 'int' or keyword == 'float' or keyword == 'string' or keyword == 'void':
                # Declarar funcion con parametros
                if len(tokens) > 2 and tokens[2] == '(':
                    function_name = tokens[1]
                    return_type = tokens[0]
                    current_function = function_name

                    tablaSimbolos.insertar_funcion(function_name, return_type)

                    # Guardar parametros

                    i = 4  # Empieza a contar los parametros
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i - 1] == 'int' or tokens[i - 1] == 'float' or tokens[i - 1] == 'string' or tokens[i - 1] == 'void':
                            tablaSimbolos.insertar_variable(tokens[i], tokens[i - 1], function_name)
                            i += 3  # Siguiente variable
                else:
                    # Declare variable with type checking
                    variable_name = tokens[1]
                    variable_type = tokens[0]
                    if len(tokens) > 2:
                        variable_value = tokens[3]
                        if validarDato(variable_type, variable_value) or validarDatoEnTabla(tablaSimbolos, variable_type, variable_value, current_function):
                            if ambito == current_function:
                                tablaSimbolos.insertar_variable(tokens[1], tokens[0], current_function)
                            elif ambito == 'condicion':
                                tablaSimbolos.insertar_variable(tokens[1], tokens[0], current_function)
                            else:
                                tablaSimbolos.insertar_variable(tokens[1], tokens[0], "global")
                        else:
                            errors.append(
                                f"Error en línea {line_num}: El valor '{variable_value}' no es compatible con el tipo '{variable_type}' para la "
                                f"variable '{variable_name}'")
                    else:
                        if ambito == current_function:
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], current_function)
                        elif ambito == 'condicion':
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], "condicion")
                        else:
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], "global")

            elif keyword == 'if' or keyword == 'while':
                enCondicion = True
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

                    if not tokens[i - 1] in ['==', '!=', '<', '>', '<=', '>=']:
                        salir = False
                        continue

                    if variable1_type is None:
                        variable1_type = tablaSimbolos.buscarVariable(tokens[i - 2], "condicion")
                        if variable1_type is None:
                            variable1_type = tablaSimbolos.buscarVariable(tokens[i - 2], "global")
                            if variable1_type is None:
                                salir = False
                                continue

                    if not validarDato(variable1_type, tokens[i]) or not validarDatoEnTabla(tablaSimbolos,
                                                                                            variable1_type, tokens[i],
                                                                                            current_function):
                        errors.append(
                            f"Error - Línea {line_num}: Los tipos de operandos son incompatibles")

                    if tokens[i + 1] not in ['and', 'or'] and tokens[i + 1] != ')':
                        errors.append(
                            f"Error - Línea {line_num}: Identificador no definido")
                    i += 4
                    enCondicion = False
            elif keyword == 'return':
                if ambito == 'global':
                    errors.append(
                        f"Error - Línea {line_num}: '{tokens[0]}' Identificador no definido")
                    continue
                # Check return type
                expected_return_type = tablaSimbolos.buscarFuncion(current_function)
                variable1_type = tablaSimbolos.buscarVariable(tokens[1], current_function)
                if variable1_type is None:
                    variable1_type = tablaSimbolos.buscarVariable(tokens[1], "global")
                    if variable1_type is None:
                        errors.append(
                            f"Error - Línea {line_num}: {tokens[1]} No esta declarada.")
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
