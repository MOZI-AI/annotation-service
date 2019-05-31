FROM backend-deps:beta-v1.1
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

# Setup Directories
COPY requirements.txt $CODE/requirements.txt
RUN pip install -r requirements.txt

COPY . $CODE
COPY install.sh $CODE/install
RUN chmod 755 install && ./install


EXPOSE 3000
