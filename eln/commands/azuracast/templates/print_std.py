from jinja2 import Template


tracks_template = Template(
    """{{ divider }}
Backend: {{ backend }}
Frontend: {{ frontend }}
Listeners: {{ listeners }}
URL: {{ url }}

Now:
\t{{ main_title}}
\tby {{ main_artist}}

Before:
{% if title_0 %}\t{{ title_0}} (by {{ artist_0 }}){% endif %}
{% if title_1 %}\t{{ title_1}} (by {{ artist_1 }}){% endif %}
{% if title_2 %}\t{{ title_2}} (by {{ artist_2 }}){% endif %}
{% if title_3 %}\t{{ title_3}} (by {{ artist_3 }}){% endif %}
{% if title_4 %}\t{{ title_4}} (by {{ artist_4 }}){% endif %}

""")

stations_template = Template(
    """{{ divider }}
{{ description }}
Shortcode: {{ short_code }}
Backend: {{ backend }}
Frontend: {{ frontend }}
URL: {{ url }}

""")
