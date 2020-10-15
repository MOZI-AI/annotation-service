FROM ubuntu:20.04
MAINTAINER Abdulrahman Semrie <xabush@singularitynet.io>

#Run apt-get in NONINTERACTIVE mode
ENV DEBIAN_FRONTEND noninteractive

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update

RUN apt-get install -y git ssh libssl-dev libboost-all-dev cython dh-autoreconf coinor-clp unzip gdb vim

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

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/root/miniconda3/bin:${PATH}"

RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict
 


RUN cd /tmp && git clone https://github.com/singnet/cogutil.git && \
    cd cogutil && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib/opencog

#Install atomspace
RUN cd /tmp && git clone https://github.com/singnet/atomspace.git && \
    cd atomspace && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make  && \
    make install && \
    ldconfig /usr/local/lib/opencog

#Downlaod rapid json
RUN wget -O rapidjson.tar.gz https://github.com/Tencent/rapidjson/archive/v1.1.0.tar.gz && \
    tar -xvzf rapidjson.tar.gz &&  mv rapidjson-1.1.0/include/rapidjson /usr/local/include


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
RUN cd /tmp && git clone https://github.com/singnet/agi-bio.git && \
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

#Install OGF
RUN cd /tmp && wget https://ogdf.uos.de/wp-content/uploads/2020/02/ogdf.v2020.02.zip && \
    unzip ogdf.v2020.02.zip && cd OGDF && \ 
    mkdir build && cd build && \
    cmake -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS_INIT} -fPIC" .. && \
    make -j && make install



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

#Install grpcwebproxy
RUN wget -O grpcwebproxy.zip https://github.com/improbable-eng/grpc-web/releases/download/v0.9.5/grpcwebproxy-v0.9.5-linux-x86_64.zip
RUN unzip grpcwebproxy.zip && mv dist/grpcwebproxy-v0.9.5-linux-x86_64 ./grpcwebproxy
RUN chmod 755 grpcwebproxy && mv grpcwebproxy /usr/local/bin

# Setup Directories
RUN conda install grpcio 
COPY requirements.txt $CODE/requirements.txt

RUN conda install --yes --file requirements.txt

COPY . $CODE

WORKDIR ${CODE}/utils/annotation_graph
RUN mkdir build && cd build && \
    cmake .. && \
    make -j4 && make install

WORKDIR $CODE/scheme
RUN autoreconf -vif && \
    ./configure  && \
    make && \
    make install

ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

WORKDIR $CODE

RUN chmod 755 ./install.sh && ./install.sh
