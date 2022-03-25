FROM centos:7 as user
USER ${HOST_USER}
RUN yum -y update && yum -y install \
    rsync \
    #autoconf \
    #automake \
    #bzip2 \
    #cmake \
    #curl \
    #gcc-c++ \
    #git \
    #libtool \
    #make \
    #patch \
    #pkgconfig \
    python3

