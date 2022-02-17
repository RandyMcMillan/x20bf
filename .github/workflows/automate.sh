#!/usr/bin/env bash
#ENV VARS
OS=$(uname)
OS_VERSION=$(uname -r)
UNAME_M=$(uname -m)
ARCH=$(uname -m)
export OS
export OS_VERSION
export UNAME_M
export ARCH
report() {
echo OS:
echo "$OS" | awk '{print tolower($0)}'
echo OS_VERSION:
echo "$OS_VERSION" | awk '{print tolower($0)}'
echo UNAME_M:
echo "$UNAME_M" | awk '{print tolower($0)}'
echo ARCH:
echo "$ARCH" | awk '{print tolower($0)}'
echo OSTYPE:
echo "$OSTYPE" | awk '{print tolower($0)}'
}
nuke-docker() {
echo "start nuke-docker"
echo "start nuke-docker"
echo "start nuke-docker"
echo "start nuke-docker"
echo "start nuke-docker"
echo "start nuke-docker"
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo systemctl stop docker
    sudo apt-get purge docker-ce docker-ce-cli containerd.io moby-engine moby-cli
    sudo rm -rf /var/lib/docker
    curl -fsSL https://get.docker.com | sudo sh
    docker --version
    sudo rm -rf /etc/docker/daemon.json
    echo '{"experimental": true}' | sudo tee -a /etc/docker/daemon.json
    sudo systemctl restart docker
fi
echo "end nuke-docker"
echo "end nuke-docker"
echo "end nuke-docker"
echo "end nuke-docker"
echo "end nuke-docker"
echo "end nuke-docker"
}
checkbrew() {
    if hash brew 2>/dev/null; then
        if ! hash "$AWK" 2>/dev/null; then
            brew install "$AWK"
        fi
        if ! hash git 2>/dev/null; then
            brew install git
        fi
        if ! hash pandoc 2>/dev/null; then
            brew install pandoc
        fi
        #legit depends
        brew install golang rust docker-compose gcc
        #brew install --build-from-source docker
        brew install --cask docker
    else
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        checkbrew
    fi
}
checkraspi(){
    echo 'Checking Raspi'
    if [ -e /etc/rpi-issue ]; then
    echo "- Original Installation"
    cat /etc/rpi-issue
    fi
    if [ -e /usr/bin/lsb_release ]; then
    echo "- Current OS"
    lsb_release -irdc
    fi
    echo "- Kernel"
    uname -r
    echo "- Model"
    cat /proc/device-tree/model && echo
    echo "- hostname"
    hostname
    echo "- Firmware"
    /opt/vc/bin/vcgencmd version
}
if [[ "$OSTYPE" == "linux"* ]]; then
    #CHECK APT
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        PACKAGE_MANAGER=apt
        export PACKAGE_MANAGER
        INSTALL=install
        export INSTALL
        AWK=gawk
        export AWK
        if hash apt 2>/dev/null; then
            sudo $PACKAGE_MANAGER $INSTALL $AWK pandoc gcc
            report
        fi
        nuke-docker
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    fi
    if [[ "$OSTYPE" == "linux-musl" ]]; then
        PACKAGE_MANAGER=apk
        export PACKAGE_MANAGER
        INSTALL=install
        export INSTALL
        AWK=gawk
        export AWK
        if hash apk 2>/dev/null; then
            $PACKAGE_MANAGER $INSTALL $AWK
            report
        fi
    fi
    if [[ "$OSTYPE" == "linux-arm"* ]]; then
        PACKAGE_MANAGER=apt
        export PACKAGE_MANAGER
        INSTALL=install
        export INSTALL
        AWK=gawk
        echo $AWK
        export AWK
        checkraspi
        if hash apt 2>/dev/null; then
            $PACKAGE_MANAGER $INSTALL $AWK
            report
        fi
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
        report
        PACKAGE_MANAGER=brew
        export PACKAGE_MANAGER
        INSTALL=install
        export INSTALL
        AWK=$(awk)
        export AWK
        checkbrew
elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo TODO add support for "$OSTYPE"
elif [[ "$OSTYPE" == "msys" ]]; then
    echo TODO add support for "$OSTYPE"
elif [[ "$OSTYPE" == "win32" ]]; then
    echo TODO add support for "$OSTYPE"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    echo TODO add support for "$OSTYPE"
else
    echo TODO add support for "$OSTYPE"
fi

legit(){
echo "start legit"
echo "start legit"
echo "start legit"
echo "start legit"
echo "start legit"
echo "start legit"
git clone https://github.com/RandyMcMillan/legit.git ~/legit && \
cd ~/legit && sudo ./make-legit.sh
echo "end legit"
echo "end legit"
echo "end legit"
echo "end legit"
echo "end legit"
echo "end legit"
}
legit
statoshi(){
echo "start statoshi"
echo "start statoshi"
echo "start statoshi"
echo "start statoshi"
echo "start statoshi"
echo "start statoshi"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
brew install docker docker-compose make && \
git clone https://github.com/bitcoincore-dev/statoshi.git ~/statoshi && \
cd ~/statoshi && make init run
echo "end statoshi"
echo "end statoshi"
echo "end statoshi"
echo "end statoshi"
echo "end statoshi"
echo "end statoshi"
}
statoshi
statoshi-host(){
echo "start statoshi-host"
echo "start statoshi-host"
echo "start statoshi-host"
echo "start statoshi-host"
echo "start statoshi-host"
echo "start statoshi-host"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
brew install docker docker-compose make && \
git clone https://github.com/bitcoincore-dev/statoshi.host.git ~/statoshi.host && \
cd ~/statoshi.host && make init run user=root port=80
echo "end statoshi-host"
echo "end statoshi-host"
echo "end statoshi-host"
echo "end statoshi-host"
echo "end statoshi-host"
echo "end statoshi-host"
}
statoshi-host
docker-shell(){
echo "start docker-shell"
echo "start docker-shell"
echo "start docker-shell"
echo "start docker-shell"
echo "start docker-shell"
echo "start docker-shell"
git clone https://github.com/RandyMcMillan/docker.shell.git ~/docker.shell && \
cd ~/docker.shell && \
make alpine user=root
make alpine user=root cmd="curl -fsSL https://get.docker.com | sudo sh"
echo "end docker-shell"
echo "end docker-shell"
echo "end docker-shell"
echo "end docker-shell"
echo "end docker-shell"
echo "end docker-shell"
}
docker-shell
py-in-bash(){
#!/bin/bash
echo "start py-in-bash"
echo "start py-in-bash"
echo "start py-in-bash"
echo "start py-in-bash"
echo "start py-in-bash"
echo "start py-in-bash"

# PS4='Line ${LINENO}: ' bash -x pyinbash.sh

PYTHON_BIN=/usr/bin/python
if [ -x $PYTHON_BIN ]; then
    $PYTHON_BIN -c "print('Hello, world')"
else
PYTHON_BIN=/usr/bin/local/python
    if [ -x $PYTHON_BIN ]; then
        $PYTHON_BIN -c "print('Hello, world')"
    else
        echo 'else else Hello World'
    fi
echo 'else Hello World'
fi

echo "Executing a bash statement"
export bashvar=100

cat << EOF > ~/pyscript.py
#!/usr/bin/python
import subprocess

print('Hello python')
subprocess.call(["echo","$bashvar"])

EOF

chmod 755 ~/pyscript.py

python ~/pyscript.py

MYSTRING="Do something in bash"
echo "$MYSTRING"

python - << EOF
myPyString = "Do something on python"
print(myPyString)

EOF

echo "Back to bash"
####################
echo "end py-in-bash"
echo "end py-in-bash"
echo "end py-in-bash"
echo "end py-in-bash"
echo "end py-in-bash"
echo "end py-in-bash"
}
py-in-bash
