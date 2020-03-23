FROM ubuntu:latest
MAINTAINER Abdulrahman Semrie <xabush@singularitynet.io>

#Run apt-get in NONINTERACTIVE mode
ENV DEBIAN_FRONTEND noninteractive

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update

RUN apt-get install -y git ssh cmake libboost-all-dev guile-2.2-dev cython dh-autoreconf unzip gdb vim

ENV HOME /root

RUN cd /tmp && git clone https://github.com/opencog/cogutil.git && \
    cd cogutil && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

#Install atomspace
RUN cd /tmp && git clone https://github.com/ngeiswei/atomspace.git && \
    cd atomspace && git checkout bio-as-xp && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

#Install agi-bio
RUN cd /tmp && git clone https://github.com/opencog/agi-bio.git && \
    cd agi-bio && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

WORKDIR $HOME

#create scheme result page
RUN mkdir /root/scm_result
RUN mkdir /root/csv_result

ENV CODE $HOME/annotation_service
RUN mkdir $CODE

WORKDIR $CODE

#Install snet daemon
ENV SNET_DAEMON_V 2.0.2
RUN mkdir snet-daemon-v$SNET_DAEMON_V
RUN wget https://github.com/singnet/snet-daemon/releases/download/v$SNET_DAEMON_V/snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz
RUN tar -xzf snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz -C snet-daemon-v$SNET_DAEMON_V --strip-components 1
RUN ln snet-daemon-v$SNET_DAEMON_V/snetd snetd
RUN rm snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz

#Install grpc proxy
RUN wget -O grpc-proxy.zip https://github.com/improbable-eng/grpc-web/releases/download/v0.9.5/grpcwebproxy-v0.9.5-linux-x86_64.zip
RUN unzip grpc-proxy.zip && mv dist/grpcwebproxy-v0.9.5-linux-x86_64 ./grpc-proxy
RUN chmod 755 grpc-proxy
COPY install.sh $CODE/install
RUN chmod 755 install && ./install

# Setup Directories
RUN apt-get install -y python3-pip

RUN pip3 install --upgrade pip && \
       pip3 install grpcio --no-binary grpcio
COPY requirements.txt $CODE/requirements.txt
RUN pip3 install -r requirements.txt

COPY . $CODE
# Install the annotation scheme dependencies

WORKDIR $HOME
RUN git clone https://github.com/aconchillo/guile-json && \
    cd guile-json && \
    autoreconf -vif && \
    ./configure --prefix=/usr GUILE=$(which guile)  && \
    make && \
    make install

WORKDIR $CODE/scheme
RUN autoreconf -vif && \
    ./configure --prefix=/usr GUILE=$(which guile)  && \
    make && \
    make install

WORKDIR $CODE
