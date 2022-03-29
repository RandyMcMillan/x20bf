## docker.shell [![automate](https://github.com/RandyMcMillan/docker.shell/actions/workflows/automate.yml/badge.svg)](https://github.com/RandyMcMillan/docker.shell/actions/workflows/automate.yml) [![docker.shell](https://github.com/RandyMcMillan/docker.shell/actions/workflows/docker.shell.yml/badge.svg)](https://github.com/RandyMcMillan/docker.shell/actions/workflows/docker.shell.yml)

##### wrap your $HOME in a dockerized alpine shell

---

### Install [docker](https://docs.docker.com/get-docker/)
### Install [make](https://www.gnu.org/software/make/)

---

## Linux

```shell
apt install docker.io docker-compose
```
## macOS
```shell
brew install make docker docker-compose
```

## git

```shell
git clone https://github.com/RandyMcMillan/docker.shell.git ~/docker.shell && \
cd docker.shell && \
make shell user=root
```

## centos

```shell
make centos user=root
```
## centos7

```shell
make centos7 user=root
```
## fedora33

```shell
make fedora33 user=root
```
## fedora34

```shell
make fedora34 user=root
```
