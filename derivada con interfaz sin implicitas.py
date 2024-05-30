import tkinter as tk
from tkinter import messagebox
from sympy import sympify, symbols, diff, Function, Eq, solve, latex
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Clase para el teclado matemático
class TecladoMatematico:
    _teclado_abierto = False

    def __init__(self, parent, entry):
        if not TecladoMatematico._teclado_abierto:
            self.parent = parent
            self.entry = entry
            self.teclado = tk.Toplevel(parent)  # Ventana secundaria para el teclado
            self.teclado.title("Teclado Matemático")
            self.teclado.attributes('-topmost', 'true')  # Asegura que la ventana esté arriba
            self.teclado.protocol("WM_DELETE_WINDOW", self.cerrar_teclado)
            TecladoMatematico._teclado_abierto = True

            # Definición de los botones del teclado
            botones = [
                ('π', lambda: self.insertar_texto('pi')),
                ('√()', lambda: self.insertar_texto('sqrt()')),
                ('^', lambda: self.insertar_texto('^')),
                ('Limpiar', self.limpiar_entrada),
                ('⌫', self.eliminar_ultimo_caracter),
                ('sen()', lambda: self.insertar_texto('sin()')),
                ('cos()', lambda: self.insertar_texto('cos()')),
                ('tan()', lambda: self.insertar_texto('tan()')),
                ('(', lambda: self.insertar_texto('(')),
                (')', lambda: self.insertar_texto(')')),
                ('sec()', lambda: self.insertar_texto('sec()')),
                ('csc()', lambda: self.insertar_texto('csc()')),
                ('cot()', lambda: self.insertar_texto('cot()')),
                ('ln()', lambda: self.insertar_texto('ln()')),
                ('e^()', lambda: self.insertar_texto('exp()')),
                ('7', lambda: self.insertar_texto('7')),
                ('8', lambda: self.insertar_texto('8')),
                ('9', lambda: self.insertar_texto('9')),
                ('/', lambda: self.insertar_texto('/')),
                ('*', lambda: self.insertar_texto('*')),
                ('4', lambda: self.insertar_texto('4')),
                ('5', lambda: self.insertar_texto('5')),
                ('6', lambda: self.insertar_texto('6')),
                ('-', lambda: self.insertar_texto('-')),
                ('+', lambda: self.insertar_texto('+')),
                ('1', lambda: self.insertar_texto('1')),
                ('2', lambda: self.insertar_texto('2')),
                ('3', lambda: self.insertar_texto('3')),
                ('x', lambda: self.insertar_texto('x')),
                ('y', lambda: self.insertar_texto('y')),
                ('0', lambda: self.insertar_texto('0')),
                ('.', lambda: self.insertar_texto('.')),
                ('1/x', lambda: self.insertar_texto('1/')),
                ('Cerrar', self.cerrar_teclado)
            ]

            # Posicionamiento de los botones en la ventana del teclado
            fila = 0
            col = 0
            for (texto, comando) in botones:
                boton = tk.Button(self.teclado, text=texto, width=5, height=2, command=comando)
                boton.grid(row=fila, column=col, padx=5, pady=5)
                col += 1
                if col > 4:
                    col = 0
                    fila += 1
        else:
            messagebox.showinfo("Info", "¡Ya hay un teclado abierto!")

    # Método para insertar texto en la entrada principal
    def insertar_texto(self, texto):
        self.entry.insert(tk.END, texto)

    # Método para eliminar el último carácter de la entrada principal
    def eliminar_ultimo_caracter(self):
        texto_entrada = self.entry.get()
        if texto_entrada:
            self.entry.delete(len(texto_entrada) - 1)

    # Método para limpiar completamente la entrada principal
    def limpiar_entrada(self):
        self.entry.delete(0, tk.END)

    # Método para cerrar la ventana del teclado
    def cerrar_teclado(self):
        self.teclado.destroy()
        TecladoMatematico._teclado_abierto = False

# Función para calcular la derivada según la opción seleccionada
def calcular_derivada(expr_input, var_input, orden_input, opcion):
    try:
        expr = sympify(expr_input)
        var = symbols(var_input)

        resultado = ""

        if opcion == 1: # Derivada de función compuesta
            derivada = diff(expr, var)
            resultado += f"La derivada de ${latex(expr)}$ con respecto a ${latex(var)}$ es: ${latex(derivada)}$\n"
        elif opcion == 2: # Derivada de orden superior
            orden = int(orden_input)
            derivada = expr
            for _ in range(orden):
                derivada = diff(derivada, var)
            resultado += f"Paso 1: Derivada de orden {orden} de ${latex(expr)}$ con respecto a ${latex(var)}$: ${latex(derivada)}$\n"
        elif opcion == 3: # Derivada implícita
            y = Function('y')(var)
            derivada = diff(expr, var)
            implicita = solve(Eq(derivada, y.diff(var)), y.diff(var))
            resultado += "Pasos para derivada implícita:\n" \
                         f"1. Identificar la función a derivar implícitamente: ${latex(expr)}$\n" \
                         f"2. Identificar la variable de derivación: ${latex(var)}$\n" \
                         f"3. Diferenciar ambos lados de la ecuación con respecto a ${latex(var)}$\n" \
                         f"4. Aplicar la regla de la cadena\n" \
                         f"5. Resolver para la derivada implícita\n" \
                         f"6. La derivada implícita de ${latex(expr)}$ con respecto a ${latex(var)}$ es: ${latex(implicita[0])}$\n"

        mostrar_resultados(resultado)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función para mostrar el resultado de la derivada en una ventana
def mostrar_resultados(resultado):
    ventana = tk.Toplevel()
    ventana.title("Resultado de la Derivada")

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.text(0.5, 0.5, resultado, fontsize=12, ha='center', va='center', wrap=True)

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

    boton = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton.pack()

# Función principal que crea la ventana principal y maneja la interfaz
def principal():
    ventana = tk.Tk()
    ventana.title("Calculadora de Derivadas")

    opcion_seleccionada = tk.IntVar()

    # Creación de etiquetas y entradas para la expresión, la variable y la opción de derivada
    etiqueta_expr = tk.Label(ventana, text="Expresión:")
    etiqueta_expr.grid(row=0, column=0, pady=5)
    entrada_expr = tk.Entry(ventana, width=30, font=('Arial', 12))
    entrada_expr.grid(row=0, column=1, pady=5)

    etiqueta_var = tk.Label(ventana, text="Variable:")
    etiqueta_var.grid(row=1, column=0, pady=5)
    entrada_var = tk.Entry(ventana, width=30, font=('Arial', 12))
    entrada_var.grid(row=1, column=1, pady=5)

    etiqueta_orden = tk.Label(ventana, text="Orden (opción 2):")
    etiqueta_orden.grid(row=2, column=0, pady=5)
    entrada_orden = tk.Entry(ventana, width=30, font=('Arial', 12))
    entrada_orden.grid(row=2, column=1, pady=5)

    # Creación de radio botones para seleccionar la opción de derivada
    radio_btn_1 = tk.Radiobutton(ventana, text="Derivada de Función Compuesta", variable=opcion_seleccionada, value=1, font=('Arial', 12))
    radio_btn_1.grid(row=3, column=0, sticky="w", pady=5)

    radio_btn_2 = tk.Radiobutton(ventana, text="Derivada de Orden Superior", variable=opcion_seleccionada, value=2, font=('Arial', 12))
    radio_btn_2.grid(row=4, column=0, sticky="w", pady=5)

#    radio_btn_3 = tk.Radiobutton(ventana, text="Derivada Implícita", variable=opcion_seleccionada, value=3, font=('Arial', 12))
#    radio_btn_3.grid(row=5, column=0, sticky="w", pady=5)

    # Función para mostrar el teclado al hacer clic en el cuadro de expresión
    def mostrar_teclado(event):
        if not hasattr(ventana, 'teclado'):
            ventana.teclado = TecladoMatematico(ventana, entrada_expr)

    entrada_expr.bind("<Button-1>", mostrar_teclado)

    # Función para calcular la derivada cuando se hace clic en el botón "Resolver"
    def resolver():
        expr = entrada_expr.get()
        var = entrada_var.get()
        orden = entrada_orden.get()
        opcion = opcion_seleccionada.get()
        calcular_derivada(expr, var, orden, opcion)

    boton_resolver = tk.Button(ventana, text="Resolver", command=resolver)
    boton_resolver.grid(row=6, columnspan=2, pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    principal()
