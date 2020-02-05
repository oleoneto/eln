from jinja2 import Template

slack_message = Template("""
{
  "text": "Kast Notifier",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":radio: <{{ url }}|{{ radio }}> is currently playing: \\n{{ title }} _by_ {{ artist }}"
      }
    },
    {% if history %}
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":clock2: *Play history*: {% for track in history %}\\n• {{ track['title'] }} ({{ track['artist'] }}){% endfor -%}"
      }
    },
    {% endif %}
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Brought to you by our team @ <https://repaus.com|repaus.com/api/nowplaying>"
        }
      ]
    }
  ]
}
""")
