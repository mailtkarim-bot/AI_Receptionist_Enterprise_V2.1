#!/bin/bash
# Initialize Let's Encrypt certificates
domains=(app.aireceptionist.example.com)
rsa_key_size=4096
data_path="./infra/certbot"
email="admin@aireceptionist.example.com"

if [ ! -d "$data_path" ]; then
    mkdir -p "$data_path/conf/live/$domains"
fi

docker compose -f infra/docker-compose.prod.yml run --rm --entrypoint "
  rm -Rf /etc/letsencrypt/live/$domains &&   rm -Rf /etc/letsencrypt/archive/$domains &&   certbot certonly --webroot -w /etc/nginx/ssl     --register-unsafely-without-email     $staging_arg     $domain_args     --rsa-key-size $rsa_key_size     --agree-tos     --force-renewal" certbot
