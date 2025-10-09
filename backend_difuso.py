# backend_difuso.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Base de datos con las propiedades de cada ingrediente
INGREDIENT_PROPERTIES = {
    # Ingredientes del Refrigerador
    "Helado": {"dulzura": 8, "acidez": 0, "cremosidad": 9, "rareza": 0},
    "Hielo": {"dulzura": 0, "acidez": 0, "cremosidad": 1, "rareza": 0},
    "Carne": {"dulzura": 0, "acidez": 0, "cremosidad": 1, "rareza": 10},
    "Chocolate": {"dulzura": 7, "acidez": 0, "cremosidad": 6, "rareza": 0},
    "Refresco": {"dulzura": 9, "acidez": 3, "cremosidad": 0, "rareza": 3},
    "Yogurt": {"dulzura": 3, "acidez": 4, "cremosidad": 8, "rareza": 0},
    "Agua": {"dulzura": 0, "acidez": 0, "cremosidad": 0, "rareza": 0},
    "Leche": {"dulzura": 2, "acidez": 0, "cremosidad": 7, "rareza": 0},
    "Fresa": {"dulzura": 6, "acidez": 3, "cremosidad": 2, "rareza": 0},

    # Ingredientes de la Alacena
    "Limón": {"dulzura": 1, "acidez": 9, "cremosidad": 0, "rareza": 1},
    "Mango": {"dulzura": 8, "acidez": 2, "cremosidad": 3, "rareza": 0},
    "Plátano": {"dulzura": 7, "acidez": 0, "cremosidad": 5, "rareza": 0},
    "Azúcar": {"dulzura": 10, "acidez": 0, "cremosidad": 0, "rareza": 0},
    "Miel": {"dulzura": 9, "acidez": 0, "cremosidad": 2, "rareza": 0},
    "Café": {"dulzura": 1, "acidez": 2, "cremosidad": 1, "rareza": 0},
    "Picante": {"dulzura": 1, "acidez": 4, "cremosidad": 0, "rareza": 9},
    "Mayonesa": {"dulzura": 0, "acidez": 2, "cremosidad": 4, "rareza": 10},
    "Mostaza": {"dulzura": 0, "acidez": 5, "cremosidad": 0, "rareza": 10},
}


class SistemaDifusoMalteada:
    def __init__(self):
        # 1. Definir las variables de entrada (Antecedentes) y salida (Consecuente)
        self.dulzura = ctrl.Antecedent(np.arange(0, 11, 1), 'dulzura')
        self.acidez = ctrl.Antecedent(np.arange(0, 11, 1), 'acidez')
        self.cremosidad = ctrl.Antecedent(np.arange(0, 11, 1), 'cremosidad')
        self.rareza = ctrl.Antecedent(np.arange(0, 11, 1), 'rareza')
        self.calidad = ctrl.Consequent(np.arange(0, 101, 1), 'calidad')

        # 2. Definir las funciones de membresía
        self.dulzura.automf(names=['baja', 'media', 'alta'])
        self.acidez.automf(names=['baja', 'media', 'alta'])
        self.cremosidad.automf(names=['baja', 'media', 'alta'])

        self.rareza['baja'] = fuzz.trimf(self.rareza.universe, [0, 0, 4])
        self.rareza['alta'] = fuzz.trimf(self.rareza.universe, [2, 10, 10])

        self.calidad['muy_mala'] = fuzz.trimf(self.calidad.universe, [0, 0, 25])
        self.calidad['mala'] = fuzz.trimf(self.calidad.universe, [15, 35, 50])
        self.calidad['regular'] = fuzz.trimf(self.calidad.universe, [40, 55, 70])
        self.calidad['buena'] = fuzz.trimf(self.calidad.universe, [60, 75, 90])
        self.calidad['excelente'] = fuzz.trimf(self.calidad.universe, [80, 100, 100])

        # 3. Definir las reglas difusas
        regla1 = ctrl.Rule(self.dulzura['alta'] & self.cremosidad['alta'] & self.rareza['baja'],
                           self.calidad['excelente'])
        regla2 = ctrl.Rule(self.dulzura['media'] & self.cremosidad['alta'] & self.rareza['baja'], self.calidad['buena'])
        regla3 = ctrl.Rule(self.dulzura['alta'] & self.cremosidad['media'] & self.rareza['baja'], self.calidad['buena'])
        regla4 = ctrl.Rule(self.dulzura['media'] & self.cremosidad['media'] & self.rareza['baja'],
                           self.calidad['regular'])
        regla5 = ctrl.Rule(self.dulzura['baja'] & self.cremosidad['alta'], self.calidad['regular'])
        regla6 = ctrl.Rule(self.acidez['alta'], self.calidad['mala'])
        regla7 = ctrl.Rule(self.dulzura['baja'] & self.cremosidad['baja'], self.calidad['mala'])
        regla_vomito1 = ctrl.Rule(self.rareza['alta'], self.calidad['muy_mala'])
        regla_vomito2 = ctrl.Rule(self.acidez['alta'] & self.cremosidad['alta'], self.calidad['muy_mala'])

        # 4. Crear el sistema de control
        sistema_control = ctrl.ControlSystem(
            [regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla_vomito1, regla_vomito2])
        self.simulacion = ctrl.ControlSystemSimulation(sistema_control)

    def calcular_calidad(self, ingredientes_seleccionados):
        if not ingredientes_seleccionados:
            return 0

        total_dulzura = sum(INGREDIENT_PROPERTIES[ing]['dulzura'] for ing in ingredientes_seleccionados)
        total_acidez = sum(INGREDIENT_PROPERTIES[ing]['acidez'] for ing in ingredientes_seleccionados)
        total_cremosidad = sum(INGREDIENT_PROPERTIES[ing]['cremosidad'] for ing in ingredientes_seleccionados)
        total_rareza = sum(INGREDIENT_PROPERTIES[ing]['rareza'] for ing in ingredientes_seleccionados)

        num_ingredientes = len(ingredientes_seleccionados)

        self.simulacion.input['dulzura'] = total_dulzura / num_ingredientes
        self.simulacion.input['acidez'] = total_acidez / num_ingredientes
        self.simulacion.input['cremosidad'] = total_cremosidad / num_ingredientes
        self.simulacion.input['rareza'] = total_rareza / num_ingredientes

        self.simulacion.compute()

        return self.simulacion.output['calidad']