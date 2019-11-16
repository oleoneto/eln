from jinja2 import Template


articles_template = Template("""{{ index }}. {{ title }}
\tAuthor: {{ author }}
\tPublished on: {{ publication_date }}
\tSource: {{ url }}
""")
