class TablaSimbolos:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def insertar_variable(self, nombre, tipo, ambito):
        if ambito not in self.variables:  # Verifica si el ámbito existe en el diccionario
            self.variables[ambito] = {}  # Si no existe, inicialízalo como un diccionario vacío

        if nombre in self.variables[ambito]:
            print(f"Error - Variable '{nombre}' redefinida.")
        else:
            self.variables[ambito][nombre] = tipo

    def buscarVariable(self, nombre, ambito):
        return self.variables[ambito].get(nombre, None)

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
    enFuncion = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

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

                    tablaSimbolos.insertar_funcion(function_name, return_type)

                    # Guardar parametros

                    i = 4  # Empieza a contar los parametros
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i - 1] == 'int' or tokens[i - 1] == 'float' or tokens[i - 1] == 'string' or tokens[i - 1]:
                            tablaSimbolos.insertar_variable(tokens[i], tokens[i - 1], "funcion")
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
                                f"Error en línea {line_num}: El valor '{variable_value}' no es una cadena para la variable '{variable_name}'")
                    else:
                        if enFuncion:
                            tablaSimbolos.insertar_variable(tokens[1], tokens[0], "funcion")
                        tablaSimbolos.insertar_variable(tokens[1], tokens[0], "global")
            elif keyword == 'if' or keyword == 'while':
                condition_tokens = tokens[2:]

                if len(condition_tokens) != 3:
                    continue

                variable1 = condition_tokens[0]
                operator = condition_tokens[1]
                variable2 = condition_tokens[2]

                if operator not in ['==', '!=', '<', '>', '<=', '>=']:
                    continue

                variable1_type = tablaSimbolos.buscarVariable(variable1, "F")
                variable2_type = tablaSimbolos.buscarVariable(variable2, "F")

                if variable1_type is None or variable2_type is None:
                    continue

                if variable1_type != variable2_type:
                    errors.append(
                        f"Error - Línea {line_num}: Los tipos de las variables '{variable1}' y '{variable2}' deben ser iguales para la condición.")
    if errors:
        for error in errors:
            print(error)
    else:
        print("El código fuente es correcto.")

    return tablaSimbolos


# Ejemplo de uso
file_path = '../codigo_fuente.txt'
print(guardarEnTablaSimbolos(file_path))
