from fpdf import FPDF
import textwrap
from datetime import datetime
import os


class MokeponReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
        
    def header(self):
        # Logo
        try:
            self.image('mokepon_logo.png', 10, 8, 25)
        except:
            pass  # No logo available
        
        # Title with blue header
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(41, 128, 185)  # Blue header
        self.set_text_color(255, 255, 255)  # White text
        self.cell(0, 15, 'Informe Detallado: Desarrollo de Mokepon World', 0, 1, 'C', True)
        
        # Date
        self.set_font('Arial', 'I', 10)
        self.set_text_color(0, 0, 0)  # Black text
        self.cell(0, 10, f'Fecha: {datetime.now().strftime("%d-%m-%Y")}', 0, 1, 'R')
        
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(52, 152, 219)  # Light blue
        self.set_text_color(255, 255, 255)  # White text
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)  # Reset text color
        self.ln(5)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(41, 128, 185)  # Blue text
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_text_color(0, 0, 0)  # Reset text color
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        lines = textwrap.wrap(text, width=85)
        for line in lines:
            self.multi_cell(0, 6, line)
        self.ln(5)
        
    def bullet_point(self, text, level=1):
        indent = level * 5  # Indentation for each level
        self.set_font('Arial', '', 11)
        self.set_x(10 + indent)
        
        bullet = '•' if level == 1 else '○' if level == 2 else '▪'
        
        # Split text into lines if needed
        lines = textwrap.wrap(text, width=85 - indent // 2)
        
        # First line with bullet
        if lines:
            self.cell(5, 6, bullet, 0, 0)
            self.set_x(15 + indent)
            self.multi_cell(0, 6, lines[0])
            
            # Additional lines without bullet (if any)
            for line in lines[1:]:
                self.set_x(15 + indent)
                self.multi_cell(0, 6, line)
    
    def code_block(self, code, language="JavaScript"):
        self.set_fill_color(240, 240, 240)  # Light gray background
        self.set_font('Courier', '', 9)
        
        # Add language label
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, language, 0, 1, 'L')
        
        # Split code into lines
        code_lines = code.strip().split('\n')
        
        # Add some padding
        self.cell(0, 2, '', 0, 1, 'L', True)
        
        # Print each line with proper spacing
        for line in code_lines:
            # Check if we need a page break
            if self.get_y() > self.page_break_trigger:
                self.add_page()
                self.set_fill_color(240, 240, 240)  # Reset fill color after page break
                
            # Indent based on leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            indent = leading_spaces * 2  # 2mm per space
            
            self.set_x(10 + indent)
            self.cell(0, 5, line.lstrip(), 0, 1, 'L', True)
        
        # Add some padding
        self.cell(0, 2, '', 0, 1, 'L', True)
        self.set_font('Arial', '', 11)
        self.ln(3)
        
    def add_image(self, image_path, w=None, caption=None):
        try:
            if w:
                self.image(image_path, x=None, y=None, w=w)
            else:
                self.image(image_path, x=None, y=None, w=150)
                
            if caption:
                self.set_font('Arial', 'I', 9)
                self.cell(0, 5, caption, 0, 1, 'C')
                self.ln(3)
        except Exception as e:
            self.cell(0, 5, f"[Error loading image: {str(e)}]", 0, 1, 'C')


def create_mokepon_report():
    pdf = MokeponReportPDF()
    pdf.add_page()

    # Section 1: Introducción
    pdf.chapter_title("1. Introducción")
    intro_text = """Este informe detalla el análisis completo del proyecto Mokepon World, un juego inspirado en Pokémon, desarrollado como parte de un proyecto de programación. El documento incluye una explicación de la metodología en cascada (Waterfall) utilizada en el desarrollo, junto con un análisis detallado del código, la estructura del proyecto y recomendaciones específicas para mejorar y optimizar el desarrollo del juego.
    
    Mokepon World implementa mecánicas de combate por turnos, movimiento de personajes, animaciones de enemigos y un sistema de tipos similar a Pokémon donde cada criatura tiene ventajas y desventajas frente a otras."""
    pdf.chapter_body(intro_text)

    # Section 2: Metodología en Cascada
    pdf.chapter_title("2. Metodología en Cascada")
    
    pdf.section_title("2.1 Descripción General")
    waterfall_text = """La metodología en cascada (Waterfall) es un proceso de desarrollo secuencial lineal donde el progreso fluye constantemente hacia abajo (como una cascada) a través de las fases de concepción, iniciación, análisis, diseño, construcción, pruebas, implementación y mantenimiento. Este enfoque enfatiza la planificación completa en las etapas iniciales y la documentación exhaustiva."""
    pdf.chapter_body(waterfall_text)
    
    pdf.section_title("2.2 Etapas del Modelo Cascada")
    pdf.bullet_point("Recopilación y análisis de requisitos: Se identifican y documentan todas las necesidades del cliente de manera exhaustiva.")
    pdf.bullet_point("Diseño del sistema: Se crea un diseño detallado de la arquitectura del sistema y sus componentes.")
    pdf.bullet_point("Implementación (Codificación): Se desarrolla el sistema basado en las especificaciones de diseño.")
    pdf.bullet_point("Verificación/Pruebas: Se realizan pruebas exhaustivas para garantizar la calidad del software.")
    pdf.bullet_point("Despliegue: El sistema se entrega al cliente y se implementa en el entorno de producción.")
    pdf.bullet_point("Mantenimiento: Se realizan ajustes y actualizaciones después de la implementación según sea necesario.")
    
    pdf.ln(5)
    pdf.section_title("2.3 Ventajas y Desventajas")
    
    pdf.section_title("Ventajas:")
    pdf.bullet_point("Proceso simplificado y fácil de entender.")
    pdf.bullet_point("Fases bien definidas con entregables claros.")
    pdf.bullet_point("Facilita la planificación y asignación de recursos.")
    pdf.bullet_point("Adecuado para proyectos con requisitos bien definidos y estables.")
    
    pdf.section_title("Desventajas:")
    pdf.bullet_point("Poca flexibilidad para adaptarse a cambios una vez iniciado el proyecto.")
    pdf.bullet_point("Los usuarios finales no ven el producto hasta etapas avanzadas.")
    pdf.bullet_point("Los errores detectados en fases tardías son costosos de corregir.")
    pdf.bullet_point("No ideal para proyectos complejos o con requisitos cambiantes.")
    
    pdf.ln(5)
    pdf.section_title("2.4 Aplicación a Mokepon World")
    waterfall_application = """Para el desarrollo de Mokepon World, la metodología en cascada ha sido adecuada debido a la clara definición inicial de los requisitos del juego. Las mecánicas de combate por turnos, los tipos de Mokepon y las reglas del juego se establecieron desde el principio, permitiendo un diseño y planificación exhaustivos antes de comenzar la implementación."""
    pdf.chapter_body(waterfall_application)

    # Section 3: Análisis del Proyecto Mokepon World
    pdf.add_page()
    pdf.chapter_title("3. Análisis del Proyecto Mokepon World")
    
    pdf.section_title("3.1 Estructura del Proyecto")
    pdf.chapter_body("El proyecto Mokepon World está organizado con una estructura clara que separa los diferentes componentes del juego:")
    
    pdf.bullet_point("Frontend:")
    pdf.bullet_point("HTML: Define la estructura de la interfaz de usuario.", 2)
    pdf.bullet_point("CSS: Controla el estilo y la apariencia visual.", 2)
    pdf.bullet_point("Lógica del Juego:")
    pdf.bullet_point("Clases para Mokepon y ataques.", 2)
    pdf.bullet_point("Sistema de animación para enemigos.", 2)
    pdf.bullet_point("Funciones de detección de colisiones.", 2)
    pdf.bullet_point("Recursos:")
    pdf.bullet_point("Imágenes de personajes y enemigos.", 2)
    pdf.bullet_point("Mapas y fondos para diferentes escenarios.", 2)
    
    pdf.ln(5)
    pdf.section_title("3.2 Características Principales")
    
    pdf.bullet_point("Sistema de Combate por Turnos:")
    pdf.bullet_point("Los jugadores seleccionan ataques basados en los tipos de sus Mokepon.", 2)
    pdf.bullet_point("Las ventajas de tipo determinan la efectividad de los ataques.", 2)
    
    pdf.bullet_point("Movimiento en Mapa:")
    pdf.bullet_point("Los jugadores pueden mover sus Mokepon usando controles direccionales.", 2)
    pdf.bullet_point("El sistema detecta colisiones con enemigos para iniciar combates.", 2)
    
    pdf.bullet_point("Animaciones de Enemigos:")
    pdf.bullet_point("Los enemigos se mueven en patrones lineales utilizando intervalos temporizados.", 2)
    pdf.bullet_point("Cada enemigo tiene animaciones personalizadas con tiempos específicos.", 2)
    
    pdf.ln(5)
    
    # Section 4: Detalles del Código
    pdf.add_page()
    pdf.chapter_title("4. Detalles del Código")
    
    pdf.section_title("4.1 Clases Principales")
    pdf.chapter_body("El juego utiliza programación orientada a objetos para modelar las entidades principales:")
    
    pdf.section_title("Clase Mokepon")
    pdf.code_block("""class Mokepon {
    constructor(image, input, label, name, x, y, width, height, idMk) {
        this.image = image;
        this.input = input;
        this.atacks = [];
        this.label = label;
        this.name = name;
        this.type = [];
        this.x = x;
        this.y = y;
        this.width = 70;
        this.height = 70;
        this.idMk = randomMonster(1, 1000000);
    }
}""", "JavaScript")
    
    pdf.section_title("Clase Atack")
    pdf.code_block("""class Atack {
    constructor(atkName, id, classMk, color, atackId) {
        this.atkName = atkName;
        this.id = id;
        this.classMk = classMk;
        this.color = color;
        this.atackId = atackId;
    }
}""", "JavaScript")
    
    pdf.ln(3)
    pdf.section_title("4.2 Sistema de Animación de Enemigos")
    pdf.chapter_body("El sistema de animación utiliza funciones específicas para cada enemigo con temporizadores personalizados:")
    
    pdf.code_block("""function moveEnemies1() {
    intervalsIdList.repeaterLists = setInterval(() => {
        mapEnemies[0].x += speedEnemy;
        checkEnemyColisions();
    }, 50);

    setTimeout(() => {
        clearInterval(intervalsIdList.repeaterLists);
        requestAnimationFrame(moveEnemiesReverse1);
    }, 2200);
}

function moveEnemiesReverse1() {
    intervalsIdList.repeaterReverseLists = setInterval(() => {
        mapEnemies[0].x -= speedEnemy;
        checkEnemyColisions();
    }, 50);
    
    setTimeout(() => {
        clearInterval(intervalsIdList.repeaterReverseLists);
        requestAnimationFrame(moveEnemies1);
    }, 2200);
}""", "JavaScript")
    
    pdf.add_page()
    pdf.section_title("4.3 Renderizado de Enemigos")
    pdf.chapter_body("Cada enemigo tiene una función específica para renderizarlo en el canvas:")
    
    pdf.code_block("""function mapEnemySetter1() {
    enemyImage.src = enemyCrabster.image;
    mapDimension.drawImage(
        enemyImage,
        enemyCrabster.x, 
        enemyCrabster.y, 
        enemyCrabster.width,
        enemyCrabster.height
    );
}""", "JavaScript")
    
    # Section 5: Mejoras Propuestas
    pdf.add_page()
    pdf.chapter_title("5. Mejoras Propuestas")
    
    pdf.section_title("5.1 Refactorización del Sistema de Animación")
    pdf.chapter_body("El código actual contiene redundancias en el sistema de animación. Se propone una solución más modular:")
    
    pdf.code_block("""// Función genérica para crear animaciones de enemigos
function createEnemyAnimation(enemyObj, property, direction, duration) {
    const intervalKey = `enemy_${enemyObj.name}_${property}_${direction}`;
    
    intervalsIdList[intervalKey] = setInterval(() => {
        enemyObj[property] += speedEnemy * direction;
        checkEnemyColisions();
    }, 50);
    
    setTimeout(() => {
        clearInterval(intervalsIdList[intervalKey]);
        // Cambiar dirección para la animación inversa
        createEnemyAnimation(enemyObj, property, -direction, duration);
    }, duration);
}

// Ejemplo de uso
function initializeEnemyAnimations() {
    createEnemyAnimation(mapEnemies[0], 'x', 1, 2200);  // Mover horizontalmente
    createEnemyAnimation(mapEnemies[1], 'y', -1, 2400); // Mover verticalmente
    // Inicializar el resto de enemigos...
}""", "JavaScript")
    
    pdf.ln(3)
    pdf.section_title("5.2 Optimización del Renderizado")
    pdf.chapter_body("De manera similar, el renderizado de enemigos puede simplificarse:")
    
    pdf.code_block("""// Función genérica para renderizar enemigos
function renderEnemy(enemy) {
    enemyImage.src = enemy.image;
    mapDimension.drawImage(
        enemyImage,
        enemy.x,
        enemy.y,
        enemy.width,
        enemy.height
    );
}

// Función para renderizar todos los enemigos
function renderAllEnemies() {
    mapEnemies.forEach(enemy => renderEnemy(enemy));
    // Renderizar enemigos adicionales si es necesario
    renderEnemy(copiedEnemyRaykiou);
    renderEnemy(copiedEnemyJoka);
    // etc.
}""", "JavaScript")
    
    pdf.ln(3)
    pdf.section_title("5.3 Mejoras en la Interfaz de Usuario")
    pdf.chapter_body("La página principal puede optimizarse para mejorar la experiencia del usuario:")
    
    pdf.bullet_point("Completar los elementos de navegación con opciones relevantes.")
    pdf.bullet_point("Añadir imágenes de mapas para cada una de las opciones de mapa.")
    pdf.bullet_point("Implementar un sistema de información sobre cada mapa al pasar el cursor.")
    pdf.bullet_point("Añadir un pie de página con información del juego y enlaces útiles.")
    
    # Section 6: Conclusiones
    pdf.add_page()
    pdf.chapter_title("6. Conclusiones y Recomendaciones Finales")
    
    conclusion_text = """El proyecto Mokepon World demuestra una buena base de programación orientada a objetos y animación en JavaScript. La estructura del código muestra una comprensión adecuada de los conceptos fundamentales de desarrollo de juegos, aunque existen oportunidades claras para optimización y mejora.

Las principales fortalezas del proyecto incluyen:
• Una clara separación de responsabilidades entre clases
• Un sistema funcional de animación de enemigos
• Una interfaz básica pero funcional

Las áreas de mejora identificadas son:
• Reducción de la redundancia en el código de animación
• Optimización de las funciones de renderizado
• Mejora de la interfaz de usuario con elementos visuales completos
• Implementación de un sistema de gestión de estados para el juego

Siguiendo la metodología en cascada, se recomienda completar la fase de pruebas antes de implementar las mejoras sugeridas, asegurando que la funcionalidad básica del juego sea sólida antes de realizar refactorizaciones significativas.

Con estas mejoras, Mokepon World tiene el potencial de convertirse en un juego más robusto, mantenible y atractivo para los usuarios."""
    pdf.chapter_body(conclusion_text)
    
    # Save the PDF
    filename = f"Mokepon_World_Informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename


if __name__ == "__main__":
    try:
        output_file = create_mokepon_report()
        print(f"¡PDF generado con éxito!: {output_file}")
        print("El informe contiene un análisis detallado del proyecto Mokepon World,")
        print("incluyendo aspectos de la metodología Waterfall y recomendaciones técnicas.")
    except Exception as e:
        print(f"Error al generar el PDF: {str(e)}")