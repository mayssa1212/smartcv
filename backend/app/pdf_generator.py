import pdfkit
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_pdf_template(template_name, context, output_path):
    template = env.get_template(template_name)
    html_content = template.render(context)
    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }
    pdfkit.from_string(html_content, output_path, options=options)