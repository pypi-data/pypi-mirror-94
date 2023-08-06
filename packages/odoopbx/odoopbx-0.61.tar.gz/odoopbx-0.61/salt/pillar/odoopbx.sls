security_ports_udp: 5060,65060
security_ports_tcp: 80,443,5038,5039,5060,5061,65060,8088,8089

letsencrypt:
  use_package: false
  config:
    email: webmaster@odoopbx.com
    authenticator: webroot
    webroot-path: /var/lib/www
  domainsets:
    www:
      - focal.asterisk.guru

nginx:
  install_from_repo: true
  package:
    opts: {}
  snippets:
    letsencrypt.conf:
      - location ^~ /.well-known/acme-challenge/:
          - root: /var/lib/www
          - default_type: "text/plain"
    proxy_params.conf:
      - proxy_set_header: X-Forwarded-Host $host
      - proxy_set_header: X-Forwarded-For $proxy_add_x_forwarded_for
      - proxy_set_header: X-Forwarded-Proto $scheme
      - proxy_set_header: X-Real-IP $remote_addr
      - proxy_http_version: 1.1
      - proxy_set_header: Upgrade $http_upgrade
      - proxy_set_header: Connection "upgrade"

  server:
    opts: {}
    config:
      worker_processes: 1
      events:
        worker_connections: 128
      http:
        sendfile: 'on'
        server_tokens: 'off'
        gzip: 'on'
        server_names_hash_bucket_size: 64
        include:
          - 'mime.types'
          - 'sites-enabled/*'
  servers:
    managed:
      odoopbx:
        enabled: true
        config:
          - server:
              - server_name: localhost
              - listen:
                  - '80 default_server'
                  - '443 ssl'
              - ssl_certificate: /etc/odoopbx/pki/odoopbx.crt
              - ssl_certificate_key: /etc/odoopbx/pki/odoopbx.key
              - include:
                  - 'snippets/letsencrypt.conf'
                  - 'snippets/proxy_params.conf'
              - location /:
                  - proxy_pass: http://localhost:8069
              - location /longpolling:
                  - proxy_pass: http://localhost:8072


