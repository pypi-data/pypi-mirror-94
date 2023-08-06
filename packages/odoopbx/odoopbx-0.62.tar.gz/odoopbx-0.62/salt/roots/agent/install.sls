{% from "agent/map.jinja" import agent with context %}

agent-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: agent-install

agent-install:
  pkg.installed:
    - pkgs: {{ agent.pkgs }}
    - refresh: true
  pip.installed:
    - pkgs:
      - jsonrpcserver
      - aiorun
      - ipsetpy
      - odoopbx
      - OdooRPC
      - https://github.com/litnimax/panoramisk/archive/master.zip
      - pastebin
      - setproctitle
      - terminado
      - tornado-httpclient-session
    - require:
      - pkg: agent-install
    - retry: True
    - reload_modules: True

agent-locale:
  locale.present:
    - name: en_US.UTF-8

{% if grains.get('virtual') != "container" and grains.get('virtual_subtype') != "Docker" %}
agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
    - template: jinja
    - unless: file.exists /etc/systemd/system/odoopbx-agent.service
  service:
    - running
    - name: odoopbx-agent
    - enable: True
    - require:
      - pip: agent-install
      - pkg: agent-install
      - file: agent-service
{% endif %}

agent-logrotate:
  file:
    - managed
    - name: /etc/logrotate.d/odoopbx-agent
    - contents:
      - "/var/log/odoopbx/minion {"
      - "   rotate 15"
      - "   weekly"
      - "   compress"
      - "   delaycompress"
      - "   postrotate"
      - "       odoopbx stop agent"
      - "       odoopbx start agent"
      - "   endscript"
      - "}"
