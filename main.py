import csv
import sys
import tkinter as tk
from tkinter import messagebox


class AhorcadoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        self.root.geometry("650x820")
        self.root.minsize(600, 750)
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")

        # Variables del juego
        self.palabra = ""
        self.palabra_esp = ""
        self.palabra_mostrada = []
        self.intentos = 6
        self.letra_a_encontrar = 0
        self.indice_palabra = 0
        self.ayudas_usadas = 0

        # Marcador
        self.aciertos = 0
        self.fallos = 0

        self.palabras_ingles = []
        self.palabras_español = []

        self._crear_interfaz()
        self._cargar_vocabulario()
        self._nueva_partida()

    def _crear_interfaz(self):
        self.canvas = tk.Canvas(self.root, width=420, height=360, bg="white",
                                highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=(12, 8))

        self.label_palabra = tk.Label(
            self.root, text="", font=("Arial", 26, "bold"),
            bg="#f5f5f5", fg="#222"
        )
        self.label_palabra.pack(pady=5)

        self.label_palabra_esp = tk.Label(
            self.root, text="", font=("Arial", 15),
            bg="#f5f5f5", fg="#0066cc"
        )
        self.label_palabra_esp.pack(pady=2)

        self.label_intentos = tk.Label(
            self.root, text="", font=("Arial", 14),
            bg="#f5f5f5"
        )
        self.label_intentos.pack(pady=4)

        self.label_marcador = tk.Label(
            self.root, text="", font=("Arial", 13, "bold"),
            bg="#f5f5f5", fg="#333"
        )
        self.label_marcador.pack(pady=4)

        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(pady=10)

        tk.Label(frame, text="Letra:", font=("Arial", 13), bg="#f5f5f5").pack(side=tk.LEFT)

        self.entry_letra = tk.Entry(frame, width=4, font=("Arial", 16), justify="center")
        self.entry_letra.pack(side=tk.LEFT, padx=7)
        self.entry_letra.bind("<Return>", lambda e: self.adivinar())

        tk.Button(
            frame, text="Adivinar", font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white", padx=10, pady=3,
            command=self.adivinar
        ).pack(side=tk.LEFT, padx=5)

        self.boton_ayuda = tk.Button(
            frame, text="Ayuda (2)", font=("Arial", 12, "bold"),
            bg="#2196F3", fg="white", padx=10, pady=3,
            command=self.usar_ayuda
        )
        self.boton_ayuda.pack(side=tk.LEFT, padx=5)

        self.entry_letra.focus_set()

    def _cargar_vocabulario(self):
        try:
            with open("vocabulario.csv", "r", encoding="utf-8") as f:
                lector = csv.reader(f, delimiter=";")
                for fila in lector:
                    if len(fila) != 2:
                        raise ValueError("Cada línea debe tener dos palabras separadas por ;")
                    eng = fila[0].strip().lower()
                    esp = fila[1].strip().lower()
                    if eng and esp:
                        self.palabras_ingles.append(eng)
                        self.palabras_español.append(esp)

            if not self.palabras_ingles:
                raise ValueError("El archivo está vacío")
            if len(self.palabras_ingles) != len(self.palabras_español):
                raise ValueError("Número diferente de palabras en inglés y español")

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'vocabulario.csv'")
            self.root.destroy()
            sys.exit(1)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.root.destroy()
            sys.exit(1)

    def _nueva_partida(self):
        # Si ya hemos terminado todas las palabras
        if self.indice_palabra == 0 and (self.aciertos + self.fallos) > 0:
            respuesta = messagebox.askyesno(
                "Fin del vocabulario",
                f"Has terminado todas las palabras.\n\n"
                f"Aciertos: {self.aciertos}   |   Fallos: {self.fallos}\n\n"
                "¿Quieres volver a jugarlas otra vez?"
            )
            if not respuesta:
                messagebox.showinfo("Fin del juego", "¡Gracias por jugar!")
                self.root.destroy()
                return
            else:
                # Reiniciar marcador si vuelve a empezar
                self.aciertos = 0
                self.fallos = 0

        self.palabra = self.palabras_ingles[self.indice_palabra]
        self.palabra_esp = self.palabras_español[self.indice_palabra]
        self.palabra_mostrada = ["_"] * len(self.palabra)
        self.intentos = 6
        self.letra_a_encontrar = 0
        self.ayudas_usadas = 0

        self.indice_palabra = (self.indice_palabra + 1) % len(self.palabras_ingles)
        self._actualizar_interfaz()

    def _actualizar_interfaz(self):
        self.label_palabra.config(text="  ".join(self.palabra_mostrada))
        self.label_palabra_esp.config(text=f"Español: {self.palabra_esp}")
        self.label_intentos.config(text=f"Intentos restantes: {self.intentos}")
        self.label_marcador.config(text=f"Aciertos: {self.aciertos}    |    Fallos: {self.fallos}")
        self.boton_ayuda.config(text=f"Ayuda ({2 - self.ayudas_usadas})")
        self._dibujar_ahorcado()

    def _dibujar_ahorcado(self):
        self.canvas.delete("all")

        self.canvas.create_line(60, 330, 360, 330, width=4)
        self.canvas.create_line(180, 330, 180, 40, width=4)
        self.canvas.create_line(180, 40, 280, 40, width=4)
        self.canvas.create_line(280, 40, 280, 80, width=3)

        if self.intentos < 6:
            self.canvas.create_oval(255, 80, 305, 130, width=2)
        if self.intentos < 5:
            self.canvas.create_line(280, 130, 280, 210, width=2)
        if self.intentos < 4:
            self.canvas.create_line(280, 150, 245, 180, width=2)
        if self.intentos < 3:
            self.canvas.create_line(280, 150, 315, 180, width=2)
        if self.intentos < 2:
            self.canvas.create_line(280, 210, 245, 260, width=2)
        if self.intentos < 1:
            self.canvas.create_line(280, 210, 315, 260, width=2)

    def usar_ayuda(self):
        if self.ayudas_usadas >= 2:
            messagebox.showinfo("Ayuda", "Ya has usado las 2 ayudas de esta palabra.")
            return

        if self.letra_a_encontrar >= len(self.palabra):
            return

        letra = self.palabra[self.letra_a_encontrar]
        self.palabra_mostrada[self.letra_a_encontrar] = letra
        self.letra_a_encontrar += 1
        self.ayudas_usadas += 1

        self._actualizar_interfaz()

        if "_" not in self.palabra_mostrada:
            self.aciertos += 1
            messagebox.showinfo("¡Ganaste!", f"¡Felicidades!\nLa palabra era: {self.palabra}")
            self._nueva_partida()

    def adivinar(self):
        letra = self.entry_letra.get().strip().lower()
        self.entry_letra.delete(0, tk.END)

        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Entrada inválida", "Introduce solo una letra.")
            return

        if (self.letra_a_encontrar < len(self.palabra) and
                self.palabra[self.letra_a_encontrar] == letra and
                self.palabra_mostrada[self.letra_a_encontrar] == "_"):
            self.palabra_mostrada[self.letra_a_encontrar] = letra
            self.letra_a_encontrar += 1
        else:
            self.intentos -= 1

        self._actualizar_interfaz()

        if "_" not in self.palabra_mostrada:
            self.aciertos += 1
            messagebox.showinfo("¡Ganaste!", f"¡Felicidades!\nLa palabra era: {self.palabra}")
            self._nueva_partida()
        elif self.intentos <= 0:
            self.fallos += 1
            messagebox.showinfo("Perdiste", f"Has perdido.\nLa palabra era: {self.palabra}")
            self._nueva_partida()


def main():
    root = tk.Tk()
    app = AhorcadoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()