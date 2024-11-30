import xlsxwriter

# Crear un nuevo archivo Excel y agregar una hoja
workbook = xlsxwriter.Workbook('./generated_files/comisiones.xlsx')
worksheet = workbook.add_worksheet()

# Definir los encabezados de la tabla
headers = ['Vendedor', 'Ventas', 'Porcentaje de Comisión', 'Comisión Total']
worksheet.write_row('A1', headers)

# Datos de prueba
vendedores = ['Juan', 'María', 'Pedro']
ventas = [1000, 1500, 800]
porcentaje_comision = 0.05  # 5%

# Escribir los datos en las celdas
for i in range(len(vendedores)):
    worksheet.write(i + 1, 0, vendedores[i])  # Columna A
    worksheet.write(i + 1, 1, ventas[i])       # Columna B

# Escribir el porcentaje de comisión en C1
worksheet.write('C1', porcentaje_comision)

# Calcular la Comisión Total en la columna D
for i in range(len(vendedores)):
    worksheet.write_formula(i + 1, 3, f'B{i + 2}*C$1')  # Columna D

# Cerrar el archivo
workbook.close()


#* Archivo 2

# Crear un nuevo archivo Excel y agregar una hoja
workbook = xlsxwriter.Workbook('./generated_files/productos.xlsx')
worksheet = workbook.add_worksheet()

# Definir los encabezados de la tabla
headers = ['Producto', 'Precio Original', 'Descuento (%)', 'Precio Final']
worksheet.write_row('A1', headers)

# Datos de prueba
productos = ['Producto A', 'Producto B', 'Producto C']
precios_originales = [100, 250, 180]
descuento = 0.10  # 10%

# Escribir los datos en las celdas
for i in range(len(productos)):
    worksheet.write(i + 1, 0, productos[i])  # Columna A
    worksheet.write(i + 1, 1, precios_originales[i])  # Columna B

# Escribir el descuento en C1
worksheet.write('C1', descuento)

# Calcular el Precio Final en la columna D
for i in range(len(productos)):
    worksheet.write_formula(i + 1, 3, f'B{i + 2}*(1-C$1)')  # Columna D

# Cerrar el archivo
workbook.close()


#*Archivo 3:

# Crear un nuevo archivo Excel y agregar una hoja
workbook = xlsxwriter.Workbook('./generated_files/costos_impuestos.xlsx')
worksheet = workbook.add_worksheet()

# Definir los encabezados de la tabla
worksheet.write('A1', 'Costo')
worksheet.write('B1', 'Impuesto')
worksheet.write('C1', 'Costo total')

# Escribir un costo de producto y un valor de impuesto
worksheet.write('A2', 100)  # Costo del producto
worksheet.write('B2', 0.18)   # Impuesto (18%)

# Escribir la fórmula en C2
worksheet.write_formula('C2', '=A2 + (A2 * $B$2)')

# Cerrar el archivo
workbook.close()


#*Archivo 4

# Crear un nuevo archivo Excel y agregar una hoja
workbook = xlsxwriter.Workbook('./generated_files/bonificaciones_empleados.xlsx')
worksheet = workbook.add_worksheet()

# Definir los encabezados de la tabla
worksheet.write('A1', 'Empleado')
worksheet.write('A2', 'Salario Base')
worksheet.write('A3', 'Porcentaje de Bonificación')

# Nombres de empleados
empleados = ['Empleado 1', 'Empleado 2', 'Empleado 3']
salarios = [3000, 4500, 5000]

# Escribir nombres de empleados en A4, A5, A6
for i in range(len(empleados)):
    worksheet.write(i + 3, 0, empleados[i])  # Columna A (A4, A5, A6)
    worksheet.write(i + 3, 1, salarios[i])    # Columna B (B4, B5, B6)

# Escribir el porcentaje de bonificación en C2
worksheet.write('C2', 0.10)  # 10%

# Definir encabezado para Bonificación
worksheet.write('D1', 'Bonificación')

# Escribir la fórmula en D4 para calcular la bonificación
worksheet.write_formula('D4', '=B4*$C$2')

# Copiar la fórmula hacia abajo
worksheet.write_formula('D5', '=B5*$C$2')
worksheet.write_formula('D6', '=B6*$C$2')

# Cerrar el archivo
workbook.close()


#* Archivo 5

# Crear un nuevo archivo Excel y agregar una hoja
workbook = xlsxwriter.Workbook('./generated_files/gastos_presupuesto.xlsx')
worksheet = workbook.add_worksheet()

# Definir los encabezados de la tabla
worksheet.write('A1', 'Categoría')
worksheet.write('B1', 'Gasto Mensual')
worksheet.write('C1', 'Presupuesto Anual')
worksheet.write('D1', 'Porcentaje del Presupuesto')

# Datos de prueba
categorias = ['Comida', 'Transporte']
gastos_mensuales = [300, 150]

# Escribir los datos en las celdas
for i in range(len(categorias)):
    worksheet.write(i + 1, 0, categorias[i])  # Columna A (A2, A3)
    worksheet.write(i + 1, 1, gastos_mensuales[i])  # Columna B (B2, B3)

# Escribir el presupuesto anual en C1
worksheet.write('C1', 6000)  # Presupuesto Anual

# Calcular el Porcentaje del Presupuesto en D2
worksheet.write_formula('D2', '=B2*12/C$1')
worksheet.write_formula('D3', '=B3*12/C$1')

# Cerrar el archivo
workbook.close()