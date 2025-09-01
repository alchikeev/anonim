# Deployment Guide

This guide describes how to configure the production server with HTTPS and
privacy-conscious logging.

## HTTPS with nginx and Let's Encrypt

1. Install nginx and certbot:
   ```bash
   sudo apt install nginx certbot python3-certbot-nginx
   ```
2. Configure your server block in `/etc/nginx/sites-available/anonim`:
   ```nginx
   server {
       listen 80;
       server_name example.com;
       location / {
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```
3. Enable the configuration and request a certificate:
   ```bash
   sudo ln -s /etc/nginx/sites-available/anonim /etc/nginx/sites-enabled/
   sudo certbot --nginx -d example.com
   ```
4. nginx and Certbot will automatically configure TLS and renew certificates.

## Disable IP address logging

To avoid collecting user IP addresses, disable `access_log` in the nginx
configuration or use a log format without the `$remote_addr` variable:

```nginx
server {
    # ... existing configuration ...
    access_log off;  # prevents storing client IP addresses
}
```

Document this policy in internal procedures to ensure that no middleware or
other server components capture IP addresses.
