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

RUN mkdir /root/scm_result

WORKDIR $HOME

#setup grpc proxy
RUN wget -O grpc-proxy https://github.com/improbable-eng/grpc-web/releases/download/0.6.3/grpcwebproxy-0.6.3-linux-x86_64
RUN chmod 755 grpc-proxy

# Setup Directories
ENV CODE $HOME/mozi_annotation_service
RUN mkdir $CODE

COPY requirements.txt $CODE/requirements.txt

WORKDIR $CODE
RUN pip install -r requirements.txt

WORKDIR $HOME
COPY install.sh $HOME/install
RUN chmod 755 install && ./install


EXPOSE 3000