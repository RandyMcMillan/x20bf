ARG ALPINE_VERSION=${ALPINE_VERSION}
FROM pandoc/alpine:${ALPINE_VERSION} as base
ARG NO_CACHE=${NO_CACHE}
ARG VERBOSE=${VERBOSE}
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        py3-pyside2
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        libgcc \
        libshiboken2 \
        libstdc++ \
        musl \
        py3-shiboken2
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        alpine-sdk \
        util-linux
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        sudo bash-completion \
        git vim curl shadow openssh-client
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        python3-dev py3-pip py3-virtualenv
RUN apk update \
    && apk add ${VERBOSE} ${NO_CACHE} \
        gmp libffi-dbg libffi-dev \
        zlib autoconf automake libtool texinfo
# WORKDIR /tmp
# RUN git clone https://github.com/0x20bf-org/libffi.git && \
# cd libffi && git checkout f9ea41683444ebe11cfa45b05223899764df28fb && ./autogen.sh && \
# ./configure --prefix=/usr --disable-static && make -j"$(nproc)" && make check && make install && cd .. && rm -rf libffi

# if fail try mirror: http://uk.alpinelinux.org/alpine/
# https://mirrors.alpinelinux.org
RUN apk add pre-commit   --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing
# RUN apk add py3-pypandoc --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing
# RUN apk add pandoc       --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing

FROM scratch as user
COPY --from=base . .

ARG HOST_UID=${HOST_UID:-4000}
ARG HOST_USER=${HOST_USER:-nodummy}

RUN [ "${HOST_USER}" == "root" ] || \
    (adduser -h /home/${HOST_USER} -D -u ${HOST_UID} ${HOST_USER} \
    && chown -R "${HOST_UID}:${HOST_UID}" /home/${HOST_USER})

RUN for u in $(ls /home); do for g in disk lp floppy audio cdrom dialout video netdev games users; do addgroup $u $g; done;done

ARG PASSWORD=${PASSWORD}
RUN echo ${HOST_USER}:${PASSWORD} | chpasswd
RUN echo root:${PASSWORD} | chpasswd
RUN echo "${HOST_USER} ALL=(ALL) ALL" >> /etc/sudoers
RUN echo "root ALL=(ALL) ALL" >> /etc/sudoers
RUN echo "Set disable_coredump false" >> /etc/sudo.conf

# USER ${HOST_USER}
WORKDIR /home/${HOST_USER}
RUN touch /home/${HOST_USER}/.bash_profile

ENV SSH_PRIVATE_KEY=${SSH_PRIVATE_KEY}
RUN mkdir -p /home/${HOST_USER}/.ssh &&  chmod 700 /home/${HOST_USER}/.ssh
CMD [ "eval", "`ssh-agent`" ]
#CMD [ "ssh-add", "/home/${HOST_USER}/.ssh/${SSH_PRIVATE_KEY}" ]
#CMD [ "chmod", "600", "/home/${HOST_USER}/.ssh/${SSH_PRIVATE_KEY}" ]
WORKDIR /home/${HOST_USER}/x20bf
# CMD [ "make", "-f", "GNUmakefile", "&&","make", "-f", "GNUmakefile","init" ]
CMD [ "make", "-f", "GNUmakefile" ]
CMD [ "make", "-f", "GNUmakefile", "init" ]
CMD [ "make", "-f", "GNUmakefile", "venv" ]
# RUN virtualenv venv && . venv/bin/activate
# ENTRYPOINT [ "make", "venv" ]


