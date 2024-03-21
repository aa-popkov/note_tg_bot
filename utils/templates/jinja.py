from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_render_page(template_name: str, render_content) -> str:
    path_to_file = Path(__file__).resolve().parent
    env = Environment(
        loader=FileSystemLoader(path_to_file),
        autoescape=select_autoescape(["xml"]),
    )
    html_template = env.get_template(f"{template_name}.html")

    rendered_page: str = html_template.render(
        content=render_content,
    )
    return rendered_page
