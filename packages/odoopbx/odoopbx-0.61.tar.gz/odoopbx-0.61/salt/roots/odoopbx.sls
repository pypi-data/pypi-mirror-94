{% if grains.os_family == "Debian" %}
include:
  - asterisk
  - postgres
  - odoo
  - agent
  - https
  - nginx
{% else %}
not-yet-supported:
  test.show_notification:
    - text: Sorry, {{ grains.os_family }} is not supported yet
{% endif %}
