from jinja2 import Environment, PackageLoader
import markdown

def setup_jinja_env():
    return Environment(loader=PackageLoader('oabiblio', 'templates'))

def generate(template_name, data):
    env = setup_jinja_env()
    template = env.get_template(template_name)
    return template.render(data, encoding="utf-8")

def convert_markdown(text):
    converter = markdown.Markdown()
    return converter.convert(text)
