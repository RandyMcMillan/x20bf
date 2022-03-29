FROM centos:8 as user
USER ${HOST_USER}
RUN dnf -y install dnf-plugins-core rsync

