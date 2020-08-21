FROM ubuntu:20.04
MAINTAINER Abdulrahman Semrie <xabush@singularitynet.io>

#Run apt-get in NONINTERACTIVE mode
ENV DEBIAN_FRONTEND noninteractive

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update

RUN apt-get install -y git ssh libssl-dev libboost-all-dev cython dh-autoreconf unzip gdb vim

##Install latest cmake - grpc complains for old cmake versions
RUN cd /tmp && wget -O cmake.sh https://github.com/Kitware/CMake/releases/download/v3.18.1/cmake-3.18.1-Linux-x86_64.sh && \
    sh ./cmake.sh --prefix=/usr/local --skip-license

RUN cmake --version

#Install Guile dependecies
RUN apt-get install -y libgmp-dev libltdl-dev libunistring-dev libffi-dev libgc-dev flex texinfo  libreadline-dev pkg-config

ENV HOME /root

#Install guile-3.x
RUN cd /tmp && wget https://ftp.gnu.org/gnu/guile/guile-3.0.2.tar.gz  && \
         tar -xvzf guile-3.0.2.tar.gz && cd guile-3.0.2 && \
         autoreconf -vif && \
         ./configure && \
         make -j4 && make install

##Install grpc cpp
RUN cd /tmp &&  git clone -b v1.31.0 https://github.com/grpc/grpc && \
    cd grpc && git submodule update --init && \
    mkdir build && cd build && \
    cmake .. && make -j4 && make install && \
    ldconfig

##Install nlohmann json
RUN mkdir -p /usr/local/include/nlohmann && wget -O /usr/local/include/nlohmann/json.hpp https://github.com/nlohmann/json/releases/download/v3.9.1/json.hpp

RUN cd /tmp && git clone https://github.com/opencog/cogutil.git && \
    cd cogutil && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

#Install atomspace
RUN cd /tmp && git clone https://github.com/opencog/atomspace.git && \
    cd atomspace && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog


RUN cd /tmp && git clone https://github.com/aconchillo/guile-json && \
    cd guile-json && \
    autoreconf -vif && \
    ./configure  && \
    make && \
    make install



RUN cd /tmp && git clone https://github.com/wingo/fibers && \
    cd fibers && \
    autoreconf -vif && \
    ./configure  && \
    make && \
    make install

#Install agi-bio
RUN cd /tmp && git clone https://github.com/opencog/agi-bio.git && \
    cd agi-bio && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

RUN cd /tmp && git clone https://github.com/Habush/atomspace-rpc && \
    cd atomspace-rpc && mkdir build && cd build && \
    cmake .. && make && make install && \
    ldconfig

WORKDIR $HOME

#create scheme result page
RUN mkdir /root/scm_result
RUN mkdir /root/csv_result

ENV CODE $HOME/annotation_service
RUN mkdir $CODE

WORKDIR $CODE

#Install snet daemon
ENV SNET_DAEMON_V 4.0.0
RUN mkdir snet-daemon-v$SNET_DAEMON_V
RUN wget https://github.com/singnet/snet-daemon/releases/download/v$SNET_DAEMON_V/snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz
RUN tar -xzf snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz -C snet-daemon-v$SNET_DAEMON_V --strip-components 1
RUN ln snet-daemon-v$SNET_DAEMON_V/snetd snetd
RUN rm snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz

#Install grpc proxy
RUN wget -O grpc-proxy.zip https://github.com/improbable-eng/grpc-web/releases/download/v0.9.5/grpcwebproxy-v0.9.5-linux-x86_64.zip
RUN unzip grpc-proxy.zip && mv dist/grpcwebproxy-v0.9.5-linux-x86_64 ./grpc-proxy
RUN chmod 755 grpc-proxy

# Setup Directories
RUN apt-get install -y python3-pip

RUN pip3 install --upgrade pip && \
       pip3 install grpcio --no-binary grpcio
COPY requirements.txt $CODE/requirements.txt
RUN pip3 install -r requirements.txt

COPY . $CODE

WORKDIR $CODE/scheme
RUN autoreconf -vif && \
    ./configure  && \
    make && \
    make install

WORKDIR $CODE

RUN chmod 755 ./install.sh && ./install.sh
