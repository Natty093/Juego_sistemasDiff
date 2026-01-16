# 🥤 Fuzzy Shakes: El Sabor de la Lógica Difusa

> **¿Alguna vez te has preguntado a qué sabe una malteada de carne con chocolate?**
> Este simulador utiliza Inteligencia Artificial (Lógica Difusa) para determinar la calidad gastronómica de combinaciones imposibles.

<div align="center">
  <img src="https://img.shields.io/badge/Language-Python_3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Scikit--Fuzzy-ff69b4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Interface-Tkinter-green?style=for-the-badge" />
</div>

---

## 📖 Descripción del Proyecto

**Fuzzy Shakes** es una aplicación interactiva que simula la preparación de malteadas. A diferencia de la programación tradicional (donde una receta es "buena" o "mala"), este sistema utiliza **Lógica Difusa** para evaluar matices.

El usuario arrastra ingredientes desde un refrigerador o alacena a un vaso, y el sistema calcula un puntaje de calidad (0-100) basándose en propiedades químicas simuladas.

## 🧠 Arquitectura del Sistema Difuso

El "cerebro" del juego se encuentra en `backend_difuso.py` y opera en tres etapas:

### 1. Fuzzificación (Entradas)
Cada ingrediente tiene valores numéricos definidos. El sistema promedia estos valores y los convierte en variables lingüísticas:

| Variable | Etiquetas Lingüísticas | Ejemplo de Ingredientes |
| :--- | :--- | :--- |
| **🍬 Dulzura** | Baja, Media, Alta | Azúcar (10), Refresco (9) |
| **🍋 Acidez** | Baja, Media, Alta | Limón (9), Mostaza (5) |
| **🥛 Cremosidad** | Baja, Media, Alta | Helado (9), Yogurt (8) |
| **🦄 Rareza** | Baja, Alta | Carne (10), Mayonesa (10) |

### 2. Base de Reglas (Inferencia)
El sistema evalúa la combinación usando reglas lógicas diseñadas para imitar el gusto humano. Ejemplos reales del código:

* **La Malteada Perfecta:** `IF Dulzura IS Alta AND Cremosidad IS Alta AND Rareza IS Baja THEN Calidad IS Excelente`.
* **La Regla del "Vómito":** `IF Rareza IS Alta THEN Calidad IS Muy Mala` (Evita que pongas carne o picante en el postre).
* **Combinación Ácida:** `IF Acidez IS Alta THEN Calidad IS Mala`.

### 3. Defuzzificación (Salida)
El sistema utiliza el método del **Centroide** para convertir la inferencia difusa en un número concreto del 0 al 100, que se traduce en la interfaz gráfica:

* **0 - 15:** 🤮 Horrible (Emoji Vómito)
* **60 - 78:** 👍 Refrescante (Pulgar Arriba)
* **88 - 100:** 💖 Obra Maestra (Corazón)

---

## 🕹️ Cómo Jugar

1.  **Explora:** Tienes un refrigerador (Helado, Leche, Carne...) y una alacena (Limón, Café, Picante...).
2.  **Arrastra:** Selecciona entre 3 y 7 ingredientes y suéltalos en el vaso.
3.  **Mezcla:** Presiona el botón "Mezclar".
4.  **Descubre:** El sistema difuso te juzgará con un emoji y una descripción.

---

## 🛠️ Instalación y Ejecución

Para correr este proyecto en tu computadora, necesitas tener Python instalado.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Natty093/Juego_sistemasDiff.git](https://github.com/Natty093/Juego_sistemasDiff.git)
    cd Juego_sistemasDiff
    ```

2.  **Instalar dependencias:**
    Este proyecto utiliza `numpy`, `scikit-fuzzy` y `Pillow`.
    ```bash
    pip install numpy scikit-fuzzy Pillow
    ```

3.  **Ejecutar el juego:**
    ```bash
    python juego_malteadas_frontend.py
    ```

---

## 📂 Estructura del Código

* `backend_difuso.py`: Contiene la clase `SistemaDifusoMalteada`, la configuración de `skfuzzy`, las funciones de membresía y la base de datos de ingredientes.
* `juego_malteadas_frontend.py`: Interfaz gráfica hecha con `Tkinter`. Maneja el Drag & Drop, las animaciones del refrigerador y la visualización de resultados.

---
Hecho con 💜 por **Natalie** 
