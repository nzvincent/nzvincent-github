#### Building Alpine NFS Docker image and start up container


**Step 1. Build docker container**

```
  export CONTAINERIMAGE=alpine-nfs:v1
  
  docker build -t $CONTAINERIMAGE .
  
```
**Step 2. Start docker container**

```
  export CONTAINERNAME=nfs-server
  export PORT1=111:111/udp
  export PORT2=2049:2049/tcp
  export CUR_DIR=`pwd`  
  export VOLUME_DATA=$CUR_DIR/EXPORT-DATA:/EXPORT-DATA
  export CONFIG_EXPORTS=$CUR_DIR/CONFIG/exports:/etc/exports

  docker run -d -p $PORT2 -v $CONFIG_EXPORTS -v $VOLUME_DATA --privileged --name $CONTAINERIMAGE -h $CONTAINERIMAGE

```
