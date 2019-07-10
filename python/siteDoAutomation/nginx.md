
docker build -t "pytestbox" .

docker run -it --name pytestbox -p 8888:80 -u pytester pytestbox /bin/bash



ToDo...

To display screenshot in HTTP server
edit /etc/nginx/site-enabled/default

        root /home/pytester/WWW;
        location / {
                autoindex on;
        }

cd /home/pystesr/WWW

ln -s your-screenshots-dir .

/etc/init.d/nginx restart
