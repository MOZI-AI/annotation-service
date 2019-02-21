FROM opencog/opencog-dev:cli
MAINTAINER Enkusellasie Wendwosen <enku@singularitynet.io>

#Run apt-get in NONINTERACTIVE mode
ENV DEBIAN_FRONTEND noninteractive

ENV HOME /root
WORKDIR $HOME

#Install pyenv and use it for managing python version
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.5.2
RUN pyenv virtualenv 3.5.2 general
RUN pyenv global general

ENV PYTHONPATH /usr/local/lib/python3.5/dist-packages:$PYTHONPATH

RUN git clone https://github.com/enku-io/agi-bio.git
WORKDIR agi-bio
RUN mkdir build
WORKDIR build
RUN \
    cmake .. && \
    make && \
    make install

WORKDIR $HOME
RUN git clone https://github.com/Habush/guile-json.git
WORKDIR guile-json
RUN \
    apt-get install -y dh-autoreconf && \
    autoreconf -vif && \
    ./configure  && \
    make && \
    make install

WORKDIR $HOME
#create scheme result page
RUN mkdir /root/scm_result

#setup grpc proxy
RUN wget -O grpc-proxy https://github.com/improbable-eng/grpc-web/releases/download/0.6.3/grpcwebproxy-0.6.3-linux-x86_64
RUN chmod 755 grpc-proxy

#Download Datasets
RUN mkdir datasets
RUN wget -r --no-parent https://mozi.ai/datasets/
RUN mv mozi.ai/datasets/* datasets && rm -rf mozi.ai
RUN rm datasets/index.html

#Install snet daemon
WORKDIR $HOME
ENV SNET_DAEMON_V 0.1.6
RUN mkdir snet-daemon-v$SNET_DAEMON_V
RUN wget https://github.com/singnet/snet-daemon/releases/download/v$SNET_DAEMON_V/snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz
RUN tar -xzf snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz -C snet-daemon-v$SNET_DAEMON_V --strip-components 1
RUN ln snet-daemon-v$SNET_DAEMON_V/snetd snetd
RUN rm snet-daemon-v$SNET_DAEMON_V-linux-amd64.tar.gz

# Setup Directories
ENV CODE $HOME/mozi_annotation_service
RUN mkdir $CODE

WORKDIR $CODE
COPY requirements.txt $CODE/requirements.txt
RUN pip install -r requirements.txt

COPY . $CODE
COPY install.sh $CODE/install
RUN chmod 755 install && ./install


EXPOSE 3000