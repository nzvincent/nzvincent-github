#### Building Alpine NFS Docker image and start up container


**Step 1. Build docker container**

```
  export CONTAINER_IMAGE=alpine-nfs:v1
  
  docker build -t $CONTAINER_IMAGE .
  
```
**Step 2. Start docker container**

```
  export CONTAINER_NAME=nfs-server
  export PORT1=111:111/udp
  export PORT2=2049:2049/tcp
  export CUR_DIR=`pwd`  
  export VOLUME_DATA=$CUR_DIR/DATA-EXPORTS:/DATA-EXPORTS
  export CONFIG_EXPORTS=$CUR_DIR/CONFIG/exports:/etc/exports
  # Worked for some Linux
  export TIMEZONE=/etc/timezone:/etc/timezone
  export LOCALTIME=/etc/localtime:/etc/localtime
  export CPU=
  export MEM=

  docker run -d -p $PORT2 \
  --name $CONTAINER_NAME -h $CONTAINER_NAME \
  -v $CONFIG_EXPORTS -v $VOLUME_DATA \
  -v $TIMEZONE -v $LOCALTIME -v $CPU $MEM \
  --privileged \
  $CONTAINER_IMAGE

```
