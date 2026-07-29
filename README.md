# Snake Game - Versión Terminal / Consola

Juego clásico de la serpiente desarrollado para consola/terminal enfocado en lógica algorítmica pura sin librerías gráficas externas.

## Aspectos Técnicos Destacados
* **Compatibilidad Multiplataforma (Cross-Platform):** Diseñado para ejecutarse nativamente en Windows y Linux (POSIX) detectando automáticamente el sistema operativo.
* **Lógica algorítmica pura:** Control de movimiento y generación de elementos sin dependencias de frameworks externos.
* **Manejo de entrada sin bloqueo (Non-blocking I/O):** Lectura de teclado en tiempo real adaptada tanto a la consola de Windows como a la terminal de Linux.
* **Estructuras de datos dinámicas:** Control de coordenadas mediante listas/vectores para representar el cuerpo de la serpiente y su crecimiento.

## Tecnologías
* Python 3
* Librerías nativas estándar (`os`, `sys`, `time`, `msvcrt` / `select`, `termios`)

## Cómo ejecutar
1. Para Windows:
   ```bash
   python snaketerminal.py
2. Para Linux:
   ```bash
   python3 snaketerminal.py
