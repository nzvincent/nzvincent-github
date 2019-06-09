#### Building Alpine NFS Docker image and start up container

```
# Step 1. Build docker container

docker build -t alpine-nfs:v1 .

# Step 2. Start docker container

  export CONTAINERNAME=nfs-server
  export CONTAINERIMAGE=alpine-nfs:v1
  export PORT1=111:111/udp
  export PORT2=2049:2049/tcp
  export CUR_DIR=`pwd`
  docker run -d -p $PORT2 -v $CUR_DIR/exports:/etc/exports --privileged --name  $CONTAINERIMAGE

```
