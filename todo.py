from flask import render_template_string
import jinja2
template = jinja2.Template('{{ name }} is {{ age }} years old.')
rendered = template.render(name='Ginger', age=10)

class TodoListView:
    def __init__(self, items):
        self.items = items
    def render(self):
        template = jinja2.Template("""<ul class="todo-list">{% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}</ul>""")
        context = {'items': self.items}
        return template.render(context)

