from jinja2 import Template


notification_template = Template(
"""
AzuraClient Notifier
[{{ name }}]({{ url }})

Now:
{{ title }} by {{ artist }}
""")
