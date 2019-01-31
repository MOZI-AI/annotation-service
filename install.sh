#!/bin/bash

#Download the dataset files
if [ ! -d ./datasets ]; then
    mkdir datasets
    wget -r --no-parent http://46.4.115.181/datasets/
    mv 46.4.115.181/datasets/* datasets && rm -rf 46.4.115.181

else
    echo "Datasets folder exists"
fi

snet_daemon_v=0.1.5

# apt install tar
if [ ! -d snet-daemon-v$snet_daemon_v ] ; then
    mkdir snet-daemon-v$snet_daemon_v
	echo "Downloading snet-daemon"
	wget https://github.com/singnet/snet-daemon/releases/download/v$snet_daemon_v/snet-daemon-v$snet_daemon_v-linux-amd64.tar.gz
	tar -xzf snet-daemon-v$snet_daemon_v-linux-amd64.tar.gz -C snet-daemon-v$snet_daemon_v --strip-components 1
	ln snet-daemon-v$snet_daemon_v/snetd snetd
	rm snet-daemon-v$snet_daemon_v-linux-amd64.tar.gz
else
	echo "SNET daemon exists"
fi

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service_specs/annotation.proto