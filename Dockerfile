FROM moziai/backend-deps:beta-v1.3
MAINTAINER Enkusellasie Wendwosen <enku@singularitynet.io>

#Run apt-get in NONINTERACTIVE mode
ENV DEBIAN_FRONTEND noninteractive

WORKDIR $HOME
#create scheme result page
RUN mkdir /root/scm_result
RUN mkdir /root/csv_result

ENV CODE $HOME/mozi_annotation_service
RUN mkdir $CODE
WORKDIR $CODE

#Download Datasets
RUN mkdir datasets
RUN wget -r --no-parent https://mozi.ai/datasets/
RUN mv mozi.ai/datasets/* datasets && rm -rf mozi.ai
RUN rm datasets/index.html

WORKDIR $CODE
ENV SNET_DAEMON_V 0.1.8
RUN mkdir snet-daemon-v$SNET_DAEMON_V
RUN wget https://github.com/singnet/snet-daemon/releases/download/v$SNET_DAEMON_V/snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz
RUN tar -xzf snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz -C snet-daemon-v$SNET_DAEMON_V --strip-components 1
RUN ln snet-daemon-v$SNET_DAEMON_V/snetd snetd
RUN rm snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz

# Setup Directories
COPY requirements.txt $CODE/requirements.txt
RUN pip install -r requirements.txt

COPY . $CODE
COPY install.sh $CODE/install
RUN chmod 755 install && ./install


EXPOSE 3000
