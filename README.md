# Sistema Integral de Gestión - Software FJ

**Universidad Nacional Abierta y a Distancia (UNAD)**
**Curso:** Programación (213023)
**Fase:** 4 - Prácticas Simuladas
**Programa:** Ingeniería de Sistemas

## 📝 Descripción del Proyecto
Este proyecto consiste en el desarrollo de un sistema integral orientado a objetos (sin uso de bases de datos) para la empresa **Software FJ**. El sistema gestiona clientes, servicios (reservas de salas, alquiler de equipos y asesorías) y reservas, garantizando estabilidad, modularidad y un manejo robusto de errores.

## 🚀 Características Implementadas
*   **Programación Orientada a Objetos (POO):**
    *   **Abstracción:** Uso de clases abstractas (`Entidad`, `Servicio`).
    *   **Herencia:** Clases derivadas como `Cliente`, `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
    *   **Polimorfismo:** Sobrescritura del método `calcular_costo` en cada tipo de servicio.
    *   **Encapsulación:** Validación estricta de datos en la clase `Cliente` (ej. formato de correo).
*   **Manejo Avanzado de Excepciones:**
    *   Excepciones personalizadas: `ErrorValidacion` y `ServicioNoDisponible`.
    *   Uso completo de bloques `try`, `except`, `else`, `finally`.
    *   **Encadenamiento de excepciones** (`raise ... from ...`) para rastrear fallos de red.
*   **Registro de Eventos (Logging):** Todos los eventos, errores y transacciones se registran automáticamente en el archivo `sistema_fj.log`.
*   **Estabilidad:** El sistema ejecuta 10 simulaciones (válidas e inválidas) sin detenerse ante errores.

## 👥 Integrantes del Equipo (5)
*   **Cristian Camilo Silva Graciano** - Lógica base, POO y Excepciones.
*   **Integrante 2** - Validación de datos y Encapsulación.
*   **Integrante 3** - Polimorfismo y Cálculo de Costos.
*   **Integrante 4** - Documentación y Configuración de Logs.
*   **Integrante 5** - Pruebas de Estabilidad y Simulaciones.
*(Nota: Reemplaza los nombres de los integrantes 2 al 5 si tienes los nombres reales de tus compañeros).*

## ⚙️ Instrucciones de Ejecución
1. Clonar el repositorio o descargar los archivos.
2. Abrir la terminal en la carpeta del proyecto.
3. Ejecutar el comando:
   ```bash
   python sistema_fj.py