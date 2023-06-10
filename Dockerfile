FROM miktex/miktex-build-ubuntu:focal

# Set the DEBIAN_FRONTEND environment variable to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
    gnupg2 wget

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 277A7293F59E4889
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
RUN echo "deb http://miktex.org/download/ubuntu jammy universe" | tee /etc/apt/sources.list.d/miktex.list

RUN apt-get install -y \
    pandoc \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-xetex \
    fonts-mplus

WORKDIR /opt/template

CMD ["/bin/bash"]
