ARG DEBIAN_VERSION=${DEBIAN_VERSION}
FROM debian:${DEBIAN_VERSION} as user
RUN apt install -y apt
RUN apt-get -y upgrade
RUN apt-get -y update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
	apt-utils \
	adduser automake \
    bash bash-completion binutils bsdmainutils build-essential \
    ca-certificates cmake curl doxygen \
    # g++-multilib \
    git \
    #libffi6 \
    libtool libffi-dev lbzip2 libssl-dev \
    make nsis \
	openssh-client openssh-server \
    patch pkg-config \
    python3 python3-pip \
    python3-setuptools \
    vim virtualenv \
    xz-utils \
	quilt parted qemu-user-static debootstrap zerofree zip dosfstools libcap2-bin libarchive-tools rsync kmod bc qemu-utils kpartx libssl-dev sudo
RUN apt-get install debconf --reinstall
ARG PASSWORD=${PASSWORD}
ENV GIT_DISABLE_UNTRACKED_CACHE=true
ARG HOST_UID=${HOST_UID:-4000}
ARG HOST_USER=${HOST_USER:-nodummy}
USER root
RUN chmod 640 /etc/shadow
RUN chmod 4511 /usr/bin/passwd
RUN mkdir -p /var/cache/debconf

RUN mkdir -p /home/${HOST_USER}

RUN /bin/bash [[ "string1" == "string2" ]] && echo "Equal" || echo "Not equal"
RUN [[  "${HOST_UID}" == "0"  ]] && echo "${HOST_UID}" || adduser --system --disabled-password --ingroup sudo --home /home/${HOST_USER} --uid ${HOST_UID} ${HOST_USER}
RUN echo root:${PASSWORD} | chpasswd
RUN echo ${HOST_USER}:${PASSWORD} | chpasswd
RUN echo "Set disable_coredump false" >> /etc/sudo.conf

RUN mkdir -p /home/${HOST_USER}/.ssh &&  chmod 700 /home/${HOST_USER}/.ssh
RUN touch  /home/${HOST_USER}/.ssh/id_rsa
RUN echo -n ${SSH_PRIVATE_KEY} | base64 --decode >  /home/${HOST_USER}/.ssh/id_rsa
RUN  chown -R "${HOST_UID}:${HOST_UID}" /home/${HOST_USER}/.ssh
RUN chmod 600 /home/${HOST_USER}/.ssh/id_rsa

USER ${HOST_USER}
WORKDIR /home/${HOST_USER}
