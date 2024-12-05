from fpdf import FPDF

# Crear una clase que herede de FPDF
class PDF(FPDF):
    def header(self):
        # Establecer fuente
        self.set_font('Arial', 'B', 12)
        # Título
        self.cell(0, 10, 'Cambios Realizados', 0, 1, 'C')

    def footer(self):
        # Posicionar a 1.5 cm del final
        self.set_y(-15)
        # Establecer fuente
        self.set_font('Arial', 'I', 8)
        # Número de página
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Crear un objeto PDF
pdf = PDF()
pdf.add_page()

# Establecer fuente
pdf.set_font('Arial', '', 12)

# Contenido del PDF
content = [
    "Corrección de Nombres de Funciones:",
    "Cambié los nombres de las funciones a inglés para mantener la consistencia y claridad, pero puedes mantenerlos en español si lo prefieres.",
    "",
    "Arreglo de Meses:",
    "Se agregó un arreglo monthNames dentro de la función printMonth para imprimir los nombres de los meses correctamente.",
    "",
    "Lógica de Impresión:",
    "Se corrigió la lógica para imprimir el calendario, asegurando que se muestre el mes y el año correctamente.",
    "",
    "Mensajes Claros:",
    "Se mejoraron los mensajes de salida para que sean más claros y descriptivos.",
    "",
    "Este programa ahora debería funcionar correctamente y mostrar el calendario para el año que el usuario ingrese. ¡Prueba ejecutarlo y verás cómo imprime el calendario!"
]

# Agregar contenido al PDF
for line in content:
    pdf.multi_cell(0, 10, line)

# Guardar el PDF
pdf.output('cambios_realizados.pdf')

print("PDF generado con éxito: cambios_realizados.pdf")