ARG ALPINE_VERSION=${ALPINE_VERSION}
FROM alpine:${ALPINE_VERSION} as base
ARG NO_CACHE=${NO_CACHE}
ARG VERBOSE=${VERBOSE}
RUN apk update \
    && apk add  ${VERBOSE} ${NO_CACHE}   \
        musl \
        alpine-sdk util-linux sudo bash-completion git vim curl shadow openssh-client \
        python3-dev py3-pip py3-pyside2 libffi-dev libffi docker docker-compose \
        gmp zlib
# if fail try mirror: http://uk.alpinelinux.org/alpine/
# https://mirrors.alpinelinux.org
RUN apk add pre-commit --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing
RUN apk add pandoc     --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing

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

USER ${HOST_USER}
WORKDIR /home/${HOST_USER}
RUN touch .bash_profile

ENV SSH_PRIVATE_KEY=${SSH_PRIVATE_KEY}
RUN mkdir -p /home/${HOST_USER}/.ssh &&  chmod 700 /home/${HOST_USER}/.ssh
CMD [ "eval", "`ssh-agent`" ]
#CMD [ "ssh-add", "/home/${HOST_USER}/.ssh/${SSH_PRIVATE_KEY}" ]
#CMD [ "chmod", "600", "/home/${HOST_USER}/.ssh/${SSH_PRIVATE_KEY}" ]
WORKDIR /home/${HOST_USER}/x20bf
CMD [ "ssh-add" ]

