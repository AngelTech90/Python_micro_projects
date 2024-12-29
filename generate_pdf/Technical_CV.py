# print("PDF generado con éxito: estructura_calendario.pdf")
from fpdf import FPDF
import textwrap
from datetime import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)  # Set header font to Arial Bold
        self.cell(0, 10, 'Technical Experience & Project Analysis', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)  # Set footer font to Arial Italic
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)  # Set chapter title font to Arial Bold
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)  # Set body font to Arial Regular
        # Replace bullet points with asterisks or remove them
        text = text.replace('•', '*')  # Replace bullet with asterisk
        lines = textwrap.wrap(text, width=85)
        for line in lines:
            self.multi_cell(0, 6, line)
        self.ln(5)

def create_technical_report():
    pdf = CustomPDF()
    pdf.add_page()

    # Open Source & Integrations Section
    pdf.chapter_title("1. Open-Source & Integrations Experience")
    open_source_text = """In my Dashboard_project (https://github.com/AngelTech90/Dashboard_project), I demonstrated extensive 
    experience with open-source tools and integrations. I handled versioning challenges by implementing semantic versioning 
    and maintaining detailed dependency documentation. The project showcases integration with various open-source libraries 
    and frameworks, particularly in React and Node.js environments."""
    pdf.chapter_body(open_source_text)

    # Chrome Extensions Section
    pdf.chapter_title("2. Chrome Extensions Development")
    chrome_ext_text = """While my GitHub portfolio doesn't specifically showcase Chrome extensions, my experience with 
    JavaScript and React in projects like Buscadis-new (https://github.com/AngelTech90/Buscadis-new) provides a strong 
    foundation for browser extension development. I understand the Chrome Extension API and have worked with similar 
    client-side technologies."""
    pdf.chapter_body(chrome_ext_text)

    # AI & Automations Section
    pdf.chapter_title("3. AI & Automations Implementation")
    ai_text = """I have extensively worked with AI tools in my Mokepon_AI-2 project (https://github.com/AngelTech90/Mokepon_AI-2), 
    implementing Vercel SDK for AI features. I regularly use GitHub Copilot and ChatGPT to enhance development efficiency. 
    My Notion documentation demonstrates how I leverage AI for improving documentation quality and maintaining best practices."""
    pdf.chapter_body(ai_text)

    # Server Setup & DevOps Section
    pdf.chapter_title("4. Server Setup & DevOps Experience")
    devops_text = """My experience with Docker and container-based deployments is evident in my Dashboard_project, where 
    I implemented containerized environments for consistent development and deployment. I utilize Docker Compose for 
    managing multi-container applications and implement CI/CD pipelines for automated testing and deployment."""
    pdf.chapter_body(devops_text)

    # Unique Project Example
    pdf.chapter_title("5. Unique Project Highlight")
    project_text = """The Mokepon_AI-2 project stands out as a particularly challenging implementation. It combines game 
    development with AI integration using Vercel SDK. The project required solving complex problems in real-time game 
    mechanics while maintaining optimal performance and user experience."""
    pdf.chapter_body(project_text)

    # HubSpot Experience
    pdf.chapter_title("6. HubSpot Experience")
    hubspot_text = """My experience with HubSpot includes working with its automation tools and CRM integration. In the 
    Dashboard_project, I implemented CRM functionalities similar to HubSpot's approach, focusing on workflow automation 
    and customer data management. I understand HubSpot's automation capabilities and how to leverage them for business 
    process optimization."""
    pdf.chapter_body(hubspot_text)

    # Bash Automation Skills Section
    pdf.chapter_title("7. Bash Automation Skills")
    bash_text = """I have developed various Bash scripts to automate repetitive tasks, enhancing efficiency and productivity. 
    My repository, Practice_Bash_Script (https://github.com/AngelTech90/Practice_Bash_Script), showcases my ability to create 
    scripts that streamline processes, manage system resources, and automate backups. These scripts demonstrate my proficiency 
    in using Bash for task automation and system management."""
    pdf.chapter_body(bash_text)

    # PowerShell Automation Skills Section
    pdf.chapter_title("8. PowerShell Automation Skills")
    powershell_text = """In addition to Bash, I have experience with PowerShell scripting for automation on Windows systems. 
    My repository, Practice_PowerShell (https://github.com/AngelTech90/Practice_PowerShell), highlights my skills in creating 
    scripts that automate administrative tasks, manage system configurations, and enhance workflow efficiency. I leverage 
    PowerShell's capabilities to improve productivity and streamline operations."""
    pdf.chapter_body(powershell_text)

    # Portfolio Section
    pdf.chapter_title("9. Portfolio")
    portfolio_text = """You can view my portfolio at the following link: https://angeltech90.github.io/Prove_Gmail_templates/first_template.html. 
    It showcases my work, including various projects and templates that demonstrate my skills in web development and automation. 
    This portfolio reflects my commitment to quality and my ability to deliver effective solutions."""
    pdf.chapter_body(portfolio_text)

    # Additional Skills & Technologies
    pdf.add_page()
    pdf.chapter_title("Technical Skills Overview")
    skills_text = """
    * Frontend: React.js, JavaScript, HTML5, CSS3
    * Backend: Node.js, Express.js, Python
    * DevOps: Docker, CI/CD, Git
    * AI Integration: Vercel SDK, OpenAI API
    * Documentation: Notion, Technical Writing
    * Testing: Postman, API Testing"""
    pdf.chapter_body(skills_text)

    # Save the PDF
    filename = f"technical_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

if __name__ == "__main__":
    try:
        output_file = create_technical_report()
        print(f"PDF report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")