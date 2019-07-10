

To display screenshot in HTTP server
edit /etc/nginx/site-enabled/default

        root /home/pytester/WWW;
        location / {
                autoindex on;
        }

cd /home/pystesr/WWW
ln -s your-screenshots-dir .
