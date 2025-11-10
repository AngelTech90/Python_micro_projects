from fpdf import FPDF
import textwrap
from datetime import datetime
import os


class MokeponReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Title
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Informe Detallado: Desarrollo de Mokepon World', 0, 1, 'C')
        self.set_font('Arial', 'I', 9)
        self.cell(0, 5, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        # Line
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, num, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(235, 245, 255)
        self.cell(0, 9, f'{num}. {title}', 0, 1, 'L', True)
        self.ln(4)
        
    def section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(2)
        
    def chapter_body(self, text):
        self.set_font('Arial', '', 10)
        lines = textwrap.wrap(text, width=95)
        for line in lines:
            self.cell(0, 5, line, 0, 1)
        self.ln(3)
        
    def bullet_point(self, text, indent=0):
        self.set_font('Arial', '', 10)
        self.cell(indent, 5, '', 0, 0)
        self.cell(4, 5, '-', 0, 0)  # Changed from bullet point to dash
        
        # Wrap the text with appropriate width considering the indent
        effective_width = 95 - indent - 4
        lines = textwrap.wrap(text, width=effective_width)
        
        if lines:
            self.cell(0, 5, lines[0], 0, 1)
            for line in lines[1:]:
                self.cell(indent + 4, 5, '', 0, 0)
                self.cell(0, 5, line, 0, 1)
        self.ln(1)

    def code_section(self, code, language="JavaScript"):
        self.set_font('Courier', '', 8)
        self.set_fill_color(247, 247, 247)
        
        # Language header
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, language, 0, 1, 'L')
        
        # Code box
        self.set_draw_color(230, 230, 230)
        self.rect(10, self.get_y(), 190, 5 + 4 * len(code.split('\n')), 'DF')
        
        # Code content
        self.set_font('Courier', '', 8)
        y_position = self.get_y() + 2
        
        for line in code.split('\n'):
            self.set_xy(12, y_position)
            self.cell(0, 4, line, 0, 1, 'L')
            y_position += 4
            
        self.set_y(y_position + 2)
        self.ln(3)


def create_mokepon_report():
    try:
        pdf = MokeponReportPDF()
        # Set encoding to UTF-8
        pdf.set_title("Informe Mokepon World")
        
        # Cover Page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 40, '', 0, 1)
        pdf.cell(0, 20, 'MOKEPON WORLD', 0, 1, 'C')
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Informe de Desarrollo y Analisis', 0, 1, 'C')
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, 'Un juego inspirado en Pokemon', 0, 1, 'C')
        pdf.set_y(-50)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Generado el {datetime.now().strftime('%d de %B, %Y')}", 0, 1, 'C')
        
        # Table of Contents
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Tabla de Contenidos', 0, 1, 'L')
        pdf.ln(5)
        
        toc_items = [
            "1. Introduccion", 
            "2. Metodologia en Cascada", 
            "3. Analisis del Proyecto Mokepon World",
            "4. Estructura del Codigo",
            "5. Patrones de Diseno Implementados",
            "6. Optimizaciones Recomendadas",
            "7. Conclusion"
        ]
        
        for item in toc_items:
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, item, 0, 1, 'L')
            pdf.ln(2)
        
        # Section 1: Introduccion
        pdf.add_page()
        pdf.chapter_title("1", "Introduccion")
        intro_text = """Mokepon World es un juego inspirado en Pokemon que combina elementos de estrategia, combate por turnos y exploracion de mapas. Este informe detalla el analisis tecnico del proyecto, junto con una explicacion de la metodologia en cascada (Waterfall) que se aplica al desarrollo.

El juego permite a los jugadores explorar diferentes mapas, capturar criaturas llamadas "Mokepons" y participar en batallas contra entrenadores controlados por la IA. Cada Mokepon tiene tipos especificos y ataques unicos, creando un sistema de combate estrategico con ventajas y desventajas de tipo.

Este documento examina la estructura actual del codigo, los patrones de diseno implementados y propone optimizaciones para mejorar tanto el rendimiento como la mantenibilidad del codigo."""
        pdf.chapter_body(intro_text)
        
        # Section 2: Metodologia en Cascada
        pdf.add_page()
        pdf.chapter_title("2", "Metodologia en Cascada")
        
        pdf.section_title("Definicion y Etapas")
        waterfall_text = """La metodologia en cascada (Waterfall) es un proceso de desarrollo secuencial que avanza a traves de fases distintas con resultados especificos en cada etapa. Es especialmente adecuada para proyectos con requisitos bien definidos y pocos cambios esperados durante el desarrollo."""
        pdf.chapter_body(waterfall_text)
        
        pdf.section_title("Etapas de la Metodologia")
        
        pdf.bullet_point("Recopilacion y analisis de requisitos: Se identifican y documentan todas las necesidades del cliente y alcance del proyecto.", 4)
        pdf.bullet_point("Diseno del sistema: Se crea un diseno detallado incluyendo arquitectura, componentes y flujos de datos.", 4)
        pdf.bullet_point("Implementacion: Se desarrolla el codigo basado en las especificaciones de diseno.", 4)
        pdf.bullet_point("Verificacion: Se realizan pruebas exhaustivas para garantizar que el software cumple con los requisitos.", 4)
        pdf.bullet_point("Despliegue: El sistema se entrega al cliente y se implementa en el entorno de produccion.", 4)
        pdf.bullet_point("Mantenimiento: Se realizan actualizaciones, correcciones y mejoras segun sea necesario.", 4)
        pdf.ln(5)
        
        pdf.section_title("Ventajas de la Metodologia en Cascada para Mokepon World")
        pdf.bullet_point("Estructura clara: Proporciona un marco organizado para el desarrollo del juego.", 4)
        pdf.bullet_point("Documentacion completa: Facilita la comprension del proyecto para nuevos desarrolladores.", 4)
        pdf.bullet_point("Planificacion eficiente: Permite estimar tiempos y recursos con mayor precision.", 4)
        pdf.bullet_point("Definicion temprana: Los elementos del juego (mokepons, ataques, mapas) pueden definirse claramente desde el inicio.", 4)
        
        # Section 3: Analisis del Proyecto
        pdf.add_page()
        pdf.chapter_title("3", "Analisis del Proyecto Mokepon World")
        
        pdf.section_title("Vision General")
        overview_text = """Mokepon World es un proyecto de juego que combina HTML, CSS y JavaScript para crear una experiencia interactiva basada en navegador. El juego implementa una estructura de objetos orientada a clases para representar entidades del juego, sistemas de animacion para los enemigos, y una interfaz de usuario para navegacion entre mapas."""
        pdf.chapter_body(overview_text)
        
        pdf.section_title("Componentes Principales")
        pdf.bullet_point("Interfaz de usuario: Pagina principal con seleccion de mapas y sistema de navegacion.", 4)
        pdf.bullet_point("Sistema de animacion: Mecanismo para mover enemigos en patrones predefinidos.", 4)
        pdf.bullet_point("Sistema de clases: Definicion de Mokepons y ataques usando programacion orientada a objetos.", 4)
        pdf.bullet_point("Logica de combate: Sistema para determinar resultados de batallas basado en tipos y estadisticas.", 4)
        
        pdf.section_title("Interfaz de Usuario")
        ui_text = """La interfaz principal presenta un diseno de cuadricula con seis mapas seleccionables. Cada opcion de mapa muestra una imagen representativa, un titulo y un boton de acceso. La navegacion superior incluye un titulo del juego y espacio para opciones adicionales."""
        pdf.chapter_body(ui_text)
        
        # Section 4: Estructura del Codigo
        pdf.add_page()
        pdf.chapter_title("4", "Estructura del Codigo")
        
        pdf.section_title("Clases Principales")
        
        # Mokepon Class
        pdf.bullet_point("Clase Mokepon:", 4)
        mokepon_class_desc = """Define las criaturas del juego con propiedades como imagen, ataques, posicion, dimensiones e identificador unico."""
        lines = textwrap.wrap(mokepon_class_desc, width=80)
        for line in lines:
            pdf.cell(10, 5, '', 0, 0)
            pdf.cell(0, 5, line, 0, 1)
        
        mokepon_code = """class Mokepon {
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
}"""
        pdf.code_section(mokepon_code, "JavaScript - Clase Mokepon")
        
        # Attack Class
        pdf.bullet_point("Clase Atack:", 4)
        attack_class_desc = """Define los ataques disponibles para los Mokepons, incluyendo nombre, ID, clase CSS, color e identificador de ataque."""
        lines = textwrap.wrap(attack_class_desc, width=80)
        for line in lines:
            pdf.cell(10, 5, '', 0, 0)
            pdf.cell(0, 5, line, 0, 1)
            
        attack_code = """class Atack {
    constructor(atkName, id, classMk, color, atackId) {
        this.atkName = atkName;
        this.id = id;
        this.classMk = classMk;
        this.color = color;
        this.atackId = atackId;
    }
}"""
        pdf.code_section(attack_code, "JavaScript - Clase Atack")
        
        # Section: Sistema de Animacion
        pdf.add_page()
        pdf.section_title("Sistema de Animacion de Enemigos")
        animation_desc = """El juego implementa un sofisticado sistema de animacion para mover enemigos en patrones lineales predefinidos. Cada enemigo tiene funciones especificas que controlan su movimiento usando setInterval y setTimeout para crear ciclos de animacion continuos."""
        pdf.chapter_body(animation_desc)
        
        animation_code = """function moveEnemies1() {
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
}"""
        pdf.code_section(animation_code, "JavaScript - Sistema de Animacion")
        
        rendering_desc = """Cada enemigo tiene una funcion especifica para renderizarlo en el canvas del mapa, utilizando su imagen y posicion actual:"""
        pdf.chapter_body(rendering_desc)
        
        rendering_code = """function mapEnemySetter1() {
    enemyImage.src = enemyCrabster.image;
    mapDimension.drawImage(
        enemyImage,
        enemyCrabster.x, 
        enemyCrabster.y, 
        enemyCrabster.width,
        enemyCrabster.height
    );
}"""
        pdf.code_section(rendering_code, "JavaScript - Renderizado de Enemigos")
        
        # Section 5: Patrones de Diseno
        pdf.add_page()
        pdf.chapter_title("5", "Patrones de Diseno Implementados")
        
        pdf.section_title("Patron Constructor")
        constructor_text = """El proyecto utiliza el patron Constructor a traves de clases JavaScript para crear instancias de Mokepons y Ataques. Este patron permite la creacion estandarizada de objetos con propiedades consistentes."""
        pdf.chapter_body(constructor_text)
        
        pdf.section_title("Patron de Modulo")
        module_text = """El codigo esta organizado en funciones modulares que encapsulan comportamientos especificos, como la animacion de enemigos y la renderizacion de elementos en el mapa."""
        pdf.chapter_body(module_text)
        
        pdf.section_title("Patron de Estado")
        state_text = """Las animaciones de los enemigos implementan un patron de estado simple donde cada enemigo alterna entre dos estados (movimiento normal y movimiento inverso) basado en temporizadores."""
        pdf.chapter_body(state_text)
        
        # Section 6: Optimizaciones Recomendadas
        pdf.add_page()
        pdf.chapter_title("6", "Optimizaciones Recomendadas")
        
        pdf.section_title("Refactorizacion del Sistema de Animacion")
        animation_refactor = """El sistema actual de animacion de enemigos contiene codigo repetitivo. Se recomienda implementar una funcion generica que pueda manejar las animaciones para todos los enemigos:"""
        pdf.chapter_body(animation_refactor)
        
        refactored_code = """function createEnemyAnimation(enemy, property, direction, duration) {
    const intervalId = setInterval(() => {
        enemy[property] += speedEnemy * direction;
        checkEnemyColisions();
    }, 50);
    
    setTimeout(() => {
        clearInterval(intervalId);
        createEnemyAnimation(enemy, property, -direction, duration);
    }, duration);
    
    return intervalId;
}

// Uso:
function startAnimations() {
    intervalsIdList.enemy1 = createEnemyAnimation(mapEnemies[0], 'x', 1, 2200);
    intervalsIdList.enemy2 = createEnemyAnimation(mapEnemies[1], 'x', -1, 2400);
    // etc.
}"""
        pdf.code_section(refactored_code, "JavaScript - Animacion Refactorizada")
        
        pdf.section_title("Mejora del Sistema de Renderizado")
        render_refactor = """Similar al sistema de animacion, las funciones de renderizado pueden consolidarse en una unica funcion generica:"""
        pdf.chapter_body(render_refactor)
        
        render_code = """function renderEnemy(enemy) {
    enemyImage.src = enemy.image;
    mapDimension.drawImage(
        enemyImage,
        enemy.x,
        enemy.y,
        enemy.width,
        enemy.height
    );
}

function renderAllEnemies() {
    mapEnemies.forEach(renderEnemy);
    // Render copied enemies too
    renderEnemy(copiedEnemyRaykiou);
    renderEnemy(copiedEnemyJoka);
    // etc.
}"""
        pdf.code_section(render_code, "JavaScript - Renderizado Refactorizado")
        
        pdf.section_title("Mejoras a la Pagina Principal")
        ui_improvements = """La interfaz de usuario principal puede mejorarse con las siguientes adiciones:
- Imagenes reales para las miniaturas de los mapas
- Enlaces funcionales para cada mapa
- Opciones de navegacion completas en la barra superior
- Estilos CSS mejorados para mayor atractivo visual
- Implementacion de un diseno responsivo para diferentes dispositivos"""
        pdf.chapter_body(ui_improvements)

        pdf.section_title("Implementacion de un Sistema de Combate Mejorado")
        combat_improvements = """El sistema de combate podria mejorarse mediante:
- Tabla de ventajas/desventajas de tipo para simplificar la logica de combate
- Animaciones y efectos visuales durante las batallas
- Mecanicas de debilitamiento y curacion de Mokepons
- Sistema de experiencia y nivel para Mokepons capturados
- Mayor variedad de ataques con diferentes efectos"""
        pdf.chapter_body(combat_improvements)
        
        # Section 7: Conclusion
        pdf.add_page()
        pdf.chapter_title("7", "Conclusion")
        conclusion_text = """Mokepon World muestra un prometedor diseno de juego inspirado en Pokemon con mecanicas interesantes de combate y exploracion. El proyecto implementa conceptos importantes de programacion orientada a objetos y animacion basada en tiempo.

La aplicacion de la metodologia Waterfall beneficia al proyecto al proporcionar una estructura clara para el desarrollo, con fases bien definidas que permiten una planificacion eficiente y una documentacion completa.

Las optimizaciones propuestas pueden mejorar significativamente la mantenibilidad y escalabilidad del codigo:
1. La refactorizacion del sistema de animacion eliminara redundancias
2. La mejora del sistema de renderizado simplificara la adicion de nuevos enemigos
3. Las actualizaciones de la interfaz de usuario mejoraran la experiencia del jugador

Implementando estas mejoras, Mokepon World puede evolucionar en un juego mas robusto y atractivo, manteniendo al mismo tiempo una base de codigo limpia y eficiente que facilitara futuras expansiones."""
        pdf.chapter_body(conclusion_text)
        
        # Generate filename and save PDF
        filename = f"./generated_docs/Mokepon_World_Desarrollo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        return filename
        
    except Exception as e:
        print(f"Error al generar el PDF: {str(e)}")
        return None


if __name__ == "__main__":
    output_file = create_mokepon_report()
    if output_file:
        print(f"Informe generado exitosamente: {output_file}")
    else:
        print("Ocurrió un error al generar el informe.")
