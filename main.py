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
        return self.variables.get(GLOBAL_SCOPE, {}).get(nombre, None) is not None

    def insertar_funcion(self, nombre, tipoRetorno):
        if nombre in self.funciones:
            print(f"Error - Función '{nombre}' redefinida.")
        else:
            self.funciones[nombre] = tipoRetorno

    def buscarFuncion(self, nombre):
        return self.funciones.get(nombre, None)

    def getParametros(self, ambito):
        return self.variables[ambito].items()

    def __str__(self):
        return f"Symbol Table:\n\nVariables:\n{self.variables}\n\nFunctions:\n{self.funciones}"


def split_parenthesis(linea):
    tokens = []
    palabra = ''
    operadores = ['(', ')', '{', '}', ',', '+', '-', '==', '!=', '<', '>', '<=', '>=']

    for char in linea:
        if char in operadores:
            if palabra:
                tokens.append(palabra)
                palabra = ''
            tokens.append(char)
        elif char == ' ':
            if palabra:
                tokens.append(palabra)
                palabra = ''
        else:
            if char != '\t' and char != '\n':
                palabra += char

    if palabra:
        tokens.append(palabra)

    return tokens


def validarDato(tipo_variable, valor_de_variable, tabla_simbolos, funcion):
    # Revisa si la variable está en la tabla de símbolos
    if tabla_simbolos is not None:
        tipo_existente = tabla_simbolos.buscarVariable(valor_de_variable, funcion)
        if tipo_existente is not None:
            if tipo_existente != tipo_variable:
                return False

            # El tipo de variable es válido de acuerdo a la tabla de símbolos
            return True

        # Si no se encuentra en el ámbito de la función, verificar en el ámbito global
        tipo_existente_global = tabla_simbolos.buscarVariable(valor_de_variable, GLOBAL_SCOPE)
        if tipo_existente_global is not None:
            if tipo_existente_global != tipo_variable:
                return False
            return True

    # Revisa si el valor de la variable puede ser convertido
    if tipo_variable == 'int':
        if convertir_int(valor_de_variable):
            return True

    elif tipo_variable == 'float':
        if convertir_float(valor_de_variable):
            return True

    elif tipo_variable == 'string':
        subcadena = '"'
        if subcadena in valor_de_variable:
            return True
    # El tipo de variable no es válido
    return False


def convertir_int(valor_de_variable):
    try:
        int(valor_de_variable)
        return True
    except:
        return False


def convertir_float(valor_de_variable):
    try:
        float(valor_de_variable)
        return True
    except:
        return False


def convertir_string(valor_de_variable):
    subcadena = """"""
    if subcadena in valor_de_variable:
        return True


GLOBAL_SCOPE = 'global'
CONDICION_SCOPE = 'condicion'


def guardar_en_tabla_simbolos(file_path):
    tabla_simbolos = TablaSimbolos()
    errores = []
    cant_par = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

    funcion = None

    for numero_linea, line in enumerate(lines, start=1):
        tokens = split_parenthesis(line)

        if len(tokens) > 0:
            keyword = tokens[0]

            if '}' in tokens:
                cant_par -= 1

                continue

            if '{' in tokens:
                cant_par += 1

            if cant_par == 0:
                funcion = GLOBAL_SCOPE
                ambito = GLOBAL_SCOPE
            elif cant_par == 1:
                ambito = funcion
            else:
                ambito = 'condicion'

            if keyword in ['int', 'float', 'string', 'void']:
                # Declarar función con parámetros
                if len(tokens) > 2 and tokens[2] == '(':
                    nombre_funcion = tokens[1]
                    return_type = tokens[0]
                    funcion = nombre_funcion

                    tabla_simbolos.insertar_funcion(nombre_funcion, return_type)

                    # Guardar parámetros
                    i = 4  # Empieza a contar los parámetros
                    while i < len(tokens) and tokens[i] != '{':
                        if tokens[i - 1] in ['int', 'float', 'string', 'void']:
                            tabla_simbolos.insertar_variable(tokens[i], tokens[i - 1], nombre_funcion)
                            i += 3  # Siguiente variable
                else:
                    variable_name = tokens[1]
                    variable_type = tokens[0]

                    if len(tokens) > 3:
                        nombre_funcion = tabla_simbolos.buscarFuncion(tokens[3])
                        if nombre_funcion is not None:
                            variable_value = tokens[3]

                            if not variable_type == nombre_funcion:
                                errores.append(
                                    f"Error en línea {numero_linea}: El valor '{variable_value}' no es compatible con el tipo '{variable_type}' para la "
                                    f"variable '{tokens[0]}'")
                            else:
                                actuales = tokens[3:]
                                k = 2
                                parametros = tabla_simbolos.getParametros(variable_value)
                                try:
                                    for nombre, tipo in parametros:
                                        variable = tabla_simbolos.buscarVariable(actuales[k], funcion)
                                        if tipo == variable:
                                            k += 2
                                        elif variable is None:
                                            print(funcion)
                                            if not validarDato(tipo, actuales[k], tabla_simbolos, funcion):
                                                errores.append(
                                                    f"Error - Línea {numero_linea}: '{actuales[k]}' Argumento incompatible con parametro de tipo {tipo} ")
                                            else:
                                                errores.append(
                                                    f"Error - Línea {numero_linea}: '{actuales[k]}' Identificador no definido")
                                            break
                                        else:
                                            errores.append(
                                                f"Error en línea {numero_linea}: No existe una funcion de conversion adecuada de {tablaSimbolos.buscarVariable(actuales[k], current_function)} a {tipo} ")
                                            break

                                except:
                                    errores.append(
                                        f"Error - Línea {numero_linea}: 'Muy pocos argumentos en la funcion llamada ")
                                tabla_simbolos.insertar_variable(variable_name, variable_type, funcion)
                        else:
                            # Declare variable with type checking
                            i = 3
                            correcto = True
                            while i < len(tokens) and correcto:
                                operator = tokens[i - 1]  # que verifique los operadores
                                variable_value = tokens[i]
                                if not validarDato(variable_type, variable_value, tabla_simbolos, ambito):
                                    errores.append(
                                        f"Error en línea {numero_linea}: El valor '{variable_value}' no es compatible con el tipo '{variable_type}' para la "
                                        f"variable '{variable_name}'")
                                    correcto = False
                                i += 2
                            if correcto and ambito == funcion:
                                tabla_simbolos.insertar_variable(variable_name, variable_type, funcion)
                            elif correcto and ambito == 'condicion':
                                tabla_simbolos.insertar_variable(tokens[1], variable_type, funcion)
                            elif correcto:
                                tabla_simbolos.insertar_variable(tokens[1], variable_type, "global")
                    else:
                        if ambito == funcion:
                            tabla_simbolos.insertar_variable(variable_name, variable_type, funcion)
                        elif ambito == 'condicion':
                            tabla_simbolos.insertar_variable(variable_name, variable_type, funcion)
                        else:
                            tabla_simbolos.insertar_variable(variable_name, variable_type, "global")

            elif keyword in ['if', 'while']:
                i = 4
                salir = True
                while i < len(tokens) and tokens[i] != '{' and salir:
                    v1 = tokens[i]
                    v2 = tokens[i - 1]
                    v3 = tokens[i - 2]

                    # Validar que v1, v2, v3 sean variables
                    if not v1 not in ['(', ')', '{', '}']:
                        errores.append(f"Error - Línea {numero_linea}: '{v1}' no es una variable válida.")
                    if not v2 not in ['(', ')', '{', '}']:
                        errores.append(f"Error - Línea {numero_linea}: '{v2}' no es una variable válida.")
                    if not v3 not in ['(', ')', '{', '}']:
                        errores.append(f"Error - Línea {numero_linea}: '{v3}' no es una variable válida.")

                    variable1_tipo = tabla_simbolos.buscarVariable(tokens[i - 2], funcion)

                    if not tokens[i - 1] in ['==', '!=', '<', '>', '<=', '>=']:
                        salir = False
                        continue

                    if variable1_tipo is None:
                        variable1_tipo = tabla_simbolos.buscarVariable(tokens[i - 2], funcion)
                        if variable1_tipo is None:
                            variable1_tipo = tabla_simbolos.buscarVariable(tokens[i - 2], GLOBAL_SCOPE)
                            if variable1_tipo is None:
                                salir = False
                                errores.append(
                                    f"Error - Línea {numero_linea}: {tokens[i - 2]} Identificador no definido")
                                continue

                    if not validarDato(variable1_tipo, tokens[i], tabla_simbolos, ambito):
                        errores.append(
                            f"Error - Línea {numero_linea}: Los tipos de operandos son incompatibles")

                    if tokens[i + 1] not in ['and', 'or'] and tokens[i + 1] != ')':
                        errores.append(
                            f"Error - Línea {numero_linea}: Identificador no definido")
                    i += 4

                    if cant_par == 1:
                        funcion = tokens[i]
            elif keyword == 'return':
                if ambito == 'global':
                    errores.append(
                        f"Error - Línea {numero_linea}: '{tokens[0]}' Identificador no definido")
                    continue

                if len(tokens) > 1:
                    tipo_return_esperado = tabla_simbolos.buscarFuncion(funcion)
                    variable1_tipo = tabla_simbolos.buscarVariable(tokens[1], funcion)
                    if variable1_tipo is None:
                        variable1_tipo = tabla_simbolos.buscarVariable(tokens[1], GLOBAL_SCOPE)
                    if variable1_tipo is None:
                        errores.append(
                            f"Error - Línea {numero_linea}: {tokens[1]} No está declarada.")
                        continue
                    if tipo_return_esperado and len(tokens) >= 2 and variable1_tipo != tipo_return_esperado:
                        errores.append(
                            f"Error - Línea {numero_linea}: El tipo de valor devuelto no coincide con el tipo de función")
                else:
                    errores.append(
                        f"Error - Línea {numero_linea + 1}: Se espera una expresión")
            elif tabla_simbolos.buscarVariable(keyword, funcion) is not None:
                if len(tokens) > 0:
                    variable_value = tokens[2]
                    variable_type = tabla_simbolos.buscarVariable(keyword, funcion)
                    funcionN = tabla_simbolos.buscarFuncion(variable_value)
                    correcto = True
                    if funcionN is not None:
                        if not variable_type == funcionN:
                            errores.append(
                                f"Error en línea {numero_linea}: El valor '{variable_value}' no es compatible con el tipo '{variable_type}' para la "
                                f"variable '{tokens[0]}'")
                        else:
                            actuales = tokens[2:]
                            k = 2
                            parametros = tabla_simbolos.getParametros(variable_value)
                            try:
                                for nombre, tipo in parametros:
                                    variable = tabla_simbolos.buscarVariable(actuales[k], funcion)
                                    if tipo == variable:
                                        k += 2
                                    elif variable is None:
                                        if not validarDato(tipo, actuales[k], tabla_simbolos, funcion):
                                            errores.append(
                                                f"Error - Línea {numero_linea}: '{actuales[k]}' Argumento incompatible con parametro de tipo {tipo} ")
                                        break
                                    else:
                                        errores.append(
                                            f"Error en línea {numero_linea}: No existe una funcion de conversion adecuada de {tabla_simbolos.buscarVariable(actuales[k], funcion)} a {tipo} ")
                                        break
                            except:
                                errores.append(
                                    f"Error - Línea {numero_linea}: 'Muy pocos argumentos en la funcion llamada ")

                    else:
                        i = 2
                        correcto = True
                        while i < len(tokens) and correcto:
                            operator = tokens[i - 1]  # que verifique los operadores
                            variable_value = tokens[i]
                            if not validarDato(variable_type, variable_value, tabla_simbolos, funcion):
                                errores.append(
                                    f"Error en línea {numero_linea}: El valor '{variable_value}' no es compatible con el tipo '{variable_type}' para la "
                                    f"variable '{tokens[0]}'")
                                correcto = False
                            i += 2

            elif not tabla_simbolos.comprobarVariableG(tokens[0]):
                print(funcion)
                errores.append(
                    f"Error - Línea {numero_linea}: '{tokens[0]}' No está declarado")

    if errores:
        for error in errores:
            print(error)
    else:
        print("El código fuente es correcto.")

    return tabla_simbolos


# Ejemplo de uso
file_path = '../codigo_fuente.txt'
print(guardar_en_tabla_simbolos(file_path))
