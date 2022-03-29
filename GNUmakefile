export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
export PKG_CONFIG_PATH="/usr/local/opt/openssl@1.1/lib/pkgconfig"
export PKG_CONFIG_PATH="/usr/local/opt/openssl@3/lib/pkgconfig"

SHELL                                   := /bin/bash
PWD                                     ?= pwd_unknown
TIME                                    := $(shell date +%s)
export TIME
HOST                                    := $(shell uname -n)
USER                                    := $(shell whoami)
GPGBINARY                               := $(shell which gpg)
export GPGBINARY
PYTHON                                  := $(shell which python)
export PYTHON
PYTHON2                                 := $(shell which python2)
export PYTHON2
PYTHON3                                 := $(shell which python3)
export PYTHON3

PIP                                     := $(notdir $(shell which pip))
PIP2                                    := $(notdir $(shell which pip2))
PIP3                                    := $(notdir $(shell which pip3))
export PIP
export PIP2
export PIP3

ifeq ($(OS),Windows_NT)
	CCFLAGS += -D WIN32
	ifeq ($(PROCESSOR_ARCHITEW6432),AMD64)

	else
		ifeq ($(PROCESSOR_ARCHITECTURE),AMD64)

		endif
		ifeq ($(PROCESSOR_ARCHITECTURE),x86)

		endif
	endif
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
	# ifeq ($(CFLAGS),)
	CFLAGS='-std=c++11'
	export CFLAGS
	# endif
	endif
	ifeq ($(UNAME_S),Darwin)
	# ifeq ($(CFLAGS),)
	CFLAGS:='-stdlib=libc++'
	export CFLAGS
	# endif
	endif
	UNAME_P := $(shell uname -p)
	ifeq ($(UNAME_P),x86_64)

	endif
	ifneq ($(filter %86,$(UNAME_P)),)

	endif
	ifneq ($(filter arm%,$(UNAME_P)),)

	endif
endif

ifeq ($(project),)
PROJECT_NAME                            := $(notdir $(PWD))
else
PROJECT_NAME                            := $(project)
endif
export PROJECT_NAME
PYTHONPATH=$(PWD)/$(PROJECT_NAME)
export PYTHONPATH
DEPENDSPATH=$(PWD)/$(PROJECT_NAME)/depends
export DEPENDSPATH
BUILDPATH=$(PWD)/build
export BUILDPATH
ifeq ($(port),)
PORT                                    := 8383
else
PORT                                    := $(port)
endif
export PORT

#GIT CONFIG
GIT_USER_NAME                           := $(shell git config user.name)
export GIT_USER_NAME
GH_USER_NAME                            := $(shell git config user.name)
export GIT_USER_NAME
GIT_USER_EMAIL                          := $(shell git config user.email)
export GIT_USER_EMAIL
GIT_SERVER                              := https://github.com
export GIT_SERVER
GIT_SSH_SERVER                          := git@github.com
export GIT_SSH_SERVER
GIT_PROFILE                             := $(shell git config user.name)
export GIT_PROFILE
GIT_BRANCH                              := $(shell git rev-parse --abbrev-ref HEAD)
export GIT_BRANCH
GIT_HASH                                := $(shell git rev-parse --short HEAD)
export GIT_HASH
GIT_REPO_ORIGIN                         := $(shell git remote get-url origin)
export GIT_REPO_ORIGIN
GIT_REPO_NAME                           := $(PROJECT_NAME)
export GIT_REPO_NAME
GIT_REPO_PATH                           := $(HOME)/$(GIT_REPO_NAME)
export GIT_REPO_PATH

ifeq ($(nocache),true)
NO_CACHE := --no-cache
export NO_CACHE
endif

# Force the user to explicitly select public - public=true
# export KB_PUBLIC=public && make keybase-public
ifeq ($(public),true)
KB_PUBLIC  := public
else
KB_PUBLIC  := private
endif
export KB_PUBLIC

ifeq ($(libs),)
LIBS  := ./libs
else
LIBS  := $(libs)
endif
export LIBS

BUILDDIR              = build

ifneq ($(shell id -u),0)
DASH_U:=-U
else
DASH_U:=
endif
export DASH_U

#
# Just in time handling of CI configs
# and misc ENV for docker/cross platform
#

ifneq ($(USER),runner)
USER_FLAG:=--user
PIP                                    := pip
else
USER_FLAG:=
endif
export PIP
export USER_FLAG

export # all env vars

.PHONY: - help
##:	COMMAND              SUMMARY
## :
##:	help
-: help

.PHONY: init initialize requirements
##	:
##:	report               environment args
##
##	:
##:	init                 initialize requirements
init:
	make initialize
	rm -rf rokeys/.gitignore || sudo -s rm -rf rokeys/.gitignore
	cat x20bf/scripts/pre-commit > .git/hooks/pre-commit
.PHONY: initialize
##:	initialize           run 0x020bf/scripts/initialize
initialize:
	./$(PROJECT_NAME)/scripts/initialize
.PHONY: requirements reqs

reqs: requirements
##
##:	requirements         pip install --user -r requirements.txt
##
requirements:
	$(PYTHON3) -m $(PIP) install $(DASH_U) --upgrade pip
	$(PYTHON3) -m $(PIP) install $(DASH_U) -r requirements.txt
.PHONY: poetry-build
##	:
##:	poetry-build
poetry-build:
	poetry build
.PHONY: poetry-install
##
##:	poetry-install
##
poetry-install:
	poetry install

.PHONY: venv
##	:
##:	venv                 create python3 virtual environment
venv:
	test -d .venv || virtualenv .venv
	( \
	   source .venv/bin/activate; pip install -r requirements.txt; \
	);
	@echo "To activate (venv)"
	@echo "try:"
	@echo ". .venv/bin/activate"
	@echo "or:"
	@echo "make test-venv"
##:	test-venv            python3 ./tests/test.py
test-venv:
	# insert test commands here
	test -d .venv || virtualenv .venv
	( \
	   source .venv/bin/activate; pip install -r requirements.txt; \
       python3 tests/test.py; \
    );
##:	test-venv-p2p        p2p  test battery
test-venv-p2p:
	# insert test commands here
	test -d .venv || virtualenv .venv
	( \
	   source .venv/bin/activate; pip install -r requirements.txt; \
       python3 $(PROJECT_NAME)/depends/p2p/setup.py build; \
       python3 $(PROJECT_NAME)/depends/p2p/setup.py install; \
       python3 tests/test_time_functions.py; \
       python3 tests/test_node_ping.py; \
       python3 tests/test_node_btc_time.py; \
       python3 tests/MyOwnPeer2PeerNode.py; \
       python3 tests/my_own_p2p_application.py; \
       python3 tests/my_own_p2p_application_callback.py; \
       python3 tests/my_own_p2p_application_using_dict.py; \
	);

##:	test-venv-p2ps       p2ps test battery
test-venv-p2ps:
	# insert test commands here
	test -d .venv || virtualenv .venv
	( \
	   source .venv/bin/activate; pip install -r requirements.txt; \
       python3 tests/test_secure_node_cli.py; \
	);

##:	test-depends         test-gnupg test-p2p test-fastapi
test-depends: test-gnupg test-p2p
##:	test-gnupg           python3 ./tests/depends/gnupg/test_gnupg.py
##:	test-p2p             python3 ./tests/depends/p2p/setup.py
##:	venv-clean           rm -rf venv rokeys test_gnupg.log
venv-clean:
	rm -rf .venv
	rm -rf rokeys
	rm -rf test_gnupg.log
test-gnupg: venv
	. .venv/bin/activate;
	python3 ./tests/depends/gnupg/setup.py install;
	python3 ./tests/depends/gnupg/test_gnupg.py;
##:	test-p2p             python3 ./tests/test.py
test-p2p:
	# insert test commands here
	test -d .venv || virtualenv .venv
	( \
	   source .venv/bin/activate; pip install -r requirements.txt; \
	   source .venv/bin/activate; pip install -r requirements.txt; \
       python3 tests/test_node_interface.py; \
	);
#test-fastapi: venv
#	. .venv/bin/activate;
#	pushd tests/depends/fastapi/tests && python3 test_application.py
##	:
clean-venv: venv-clean

.PHONY: build install dist
##:	PACKAGE:
##	:
##:	build                python3 setup.py build
build: depends
	python3 setup.py build
##:	install              python3 -m pip install -e .
install: build
	rm -rf dist
	$(PYTHON3) -m $(PIP) install -e .
##:	dist                 python3 setup.py bdist_egg sdist
##  :
dist: pre-commit build
	$(PYTHON3) setup.py bdist_egg sdist

ifneq ($(shell id -u),0)
# TODO: install          depends/p2p depends/gnupg
	$(PYTHON3) -m $(PIP) install $(DASH_U) -e .
else
	$(PYTHON3) -m $(PIP) install $(DASH_U) -e .
endif

.PHONY: help
help:
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: report
report:
	@echo ''
	@echo '	[ARGUMENTS]	'
	@echo '      args:'
	@echo '        - TIME=${TIME}'
	@echo '        - UNAME_S=${UNAME_S}'
	@echo '        - UNAME_N=${UNAME_N}'
	@echo '        - BASENAME=${BASENAME}'
	@echo '        - PROJECT_NAME=${PROJECT_NAME}'
	@echo '        - GPGBINARY=${GPGBINARY}'
	@echo '        - PYTHON3=${PYTHON3}'
	@echo '        - PIP=${PIP}'
	@echo '        - PIP3=${PIP3}'
	@echo '        - PYTHONPATH=${PYTHONPATH}'
	@echo '        - DEPENDSPATH=${DEPENDSPATH}'
	@echo '        - BUILDPATH=${BUILDPATH}'
	@echo '        - USER=${USER}'
	@echo '        - USER_FLAG=${USER_FLAG}'
	@echo '        - GIT_USER_NAME=${GIT_USER_NAME}'
	@echo '        - GIT_USER_EMAIL=${GIT_USER_EMAIL}'
	@echo '        - GIT_SERVER=${GIT_SERVER}'
	@echo '        - GIT_PROFILE=${GIT_PROFILE}'
	@echo '        - GIT_BRANCH=${GIT_BRANCH}'
	@echo '        - GIT_HASH=${GIT_HASH}'
	@echo '        - GIT_REPO_ORIGIN=${GIT_REPO_ORIGIN}'
	@echo '        - GIT_REPO_NAME=${GIT_REPO_NAME}'
	@echo '        - GIT_REPO_PATH=${GIT_REPO_PATH}'
	@echo ''

##:	SUB-PACKAGES
##	:
##:	        depends
##:	install-depends      install python <packages>
.PHONY: install-gnupg
##:	install-gnupg        install python gnupg
gnupg: install-gnupg
install-gnupg:
	pushd $(DEPENDSPATH)/gnupg && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/gnupg && $(PYTHON3) $(DEPENDSPATH)/gnupg/setup.py install && popd
.PHONY: install-p2p
##:	install-p2p          install python p2pnetwork
p2p: install-p2p
install-p2p:
	pushd $(DEPENDSPATH)/p2p && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/p2p && $(PYTHON3) $(DEPENDSPATH)/p2p/setup.py install && popd
.PHONY: install-fastapi fastapi
##:	install-fastapi      install python fastapi
fastapi: install-fastapi
install-fastapi:
	pushd $(DEPENDSPATH)/fastapi && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/fastapi && $(PYTHON3) -m $(PIP) install . && popd
.PHONY: install-git
##:	install-git          install python GitPython
install-git:
	pushd $(DEPENDSPATH)/git && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/git && $(PYTHON3) -m $(PIP) install . && popd
.PHONY: install-tor
##:	install-tor          install python torpy
install-tor:
	pushd $(DEPENDSPATH)/tor && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/tor && $(PYTHON3) -m $(PIP) install . && popd
.PHONY: install-cryptography
##	:
##:	install-crypto       install python cryptography
##	:
##:	                     The cryptography python lib
##:	                     requires rust to build.
##:	                     arch x86_64
##:	                     TODO arch64
##	:
##:	                     Try 'make init' or 'make install-rust'
##:	                     then retry 'make install-crypto'
##	:
##:	                     Try 'make reqs' to install
##:	                     the cryptography dependency
##:	                     without building.
##	:
install-crypto: install-cryptography
install-cryptography:
	pushd $(DEPENDSPATH)/cryptography && $(PYTHON3) -m $(PIP) check . && popd
	#REF: --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"
	pushd $(DEPENDSPATH)/cryptography && $(PYTHON3) -m $(PIP) install . --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include" && popd
.PHONY: install-rust install-rustup
##:	install-rustup       install rust toolchain
install-rust: install-rustup
install-rustup:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > sh.rustup.rs
	[ ! hash rustc 2>/dev/null ] && chmod +x sh.rustup.rs && ./sh.rustup.rs || echo "rustc is already installed."
.PHONY: depends
##
depends: install-gnupg install-fastapi install-p2p install-git
	@echo if install-crypto fails
	@echo try:
	@echo make install-rustup

.PHONY: git-add

git-add: remove
	@echo git-add

	git config advice.addIgnoredFile false
	#git add *

	git add --ignore-errors GNUmakefile
	git add --ignore-errors README.md
	git add --ignore-errors sources/*.md
	#git add --ignore-errors TIME
	#git add --ignore-errors GLOBAL
	git add --ignore-errors $(PROJECT_NAME)/*.py
	git add --ignore-errors index.html
	git add --ignore-errors .gitignore
	git add --ignore-errors .github
	git add --ignore-errors *.sh
	git add --ignore-errors *.yml
	#git add --ignore-errors BLOCK_TIP_HEIGHT
	#git add --ignore-errors DIFFICULTY
	#git add --ignore-errors TIME

.PHONY: pre-commit
## :
##:	pre-commit           pre-commit run -a
##:	                     install .git/hooks/pre-commit
## :
pre-commit:
	@echo "If fail use:"
	@echo "black ."
	@echo "git commit (--amend) --no-verify"
	@echo "NOTE:"
	@echo "isort . # manually - alot of conflicts with black TODO: fix"
	@echo "git commit (--amend) --no-verify"
	@echo "then:"
	@echo "git commit (--amend) --no-verify"
	@echo "to manually commit files."
	@echo "NOTE: make docs products are whitespace dependent for output formatting."
	# cat x20bf/scripts/pre-commit > .git/hooks/pre-commit
	# pre-commit run -a

.PHONY: docs
##:	docs                 build docs from sources/*.md
docs:
	@echo "##### [make](https://www.gnu.org/software/make/)" > $(PWD)/$(PROJECT_NAME)/sources/MAKE.md
	bash -c "make help >> $(PWD)/$(PROJECT_NAME)/sources/MAKE.md"
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/HEADER.md                >  $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/PROTOCOL.md              >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/COMMANDS.md              >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/GETTING_STARTED.md       >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/MAKE.md                  >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/CONTRIBUTING.md          >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/$(PROJECT_NAME)/sources/FOOTER.md                >> $(PWD)/README.md'
	ln -sf README.md 0x20bf.org.md
	#brew install pandoc
	bash -c "if hash pandoc 2>/dev/null; then echo; fi || brew install pandoc"
	# bash -c 'pandoc -s README.md -o index.html  --metadata title="$(BASENAME)" '
	bash -c 'pandoc -s 0x20bf.org.md -o 0x20bf.org.html  --metadata title="" '
	ln -sf 0x20bf.org.html index.html
	# bash -c 'pandoc -s README.md -o index.html'
	#bash -c "if hash open 2>/dev/null; then open README.md; fi || echo failed to open README.md"
	git add --ignore-errors $(PWD)/$(PROJECT_NAME)/sources/*.md
	git add --ignore-errors *.md
	git add --ignore-errors *.html
	git add --ignore-errors *makefile
	#git ls-files -co --exclude-standard | grep '\.md/$\' | xargs git

.PHONY: clean clean-venv
##:	clean                rm -rf build
clean:
	bash -c "rm -rf $(BUILDDIR)"
clean-venv: venv-clean


.PHONY: serve
##:	serve                serve repo on $(PORT)
serve: docs
#REF: https://docs.python.org/3/library/http.server.html
	# bash -c "$(PYTHON3) -m http.server $(PORT) --bind 127.0.0.1 -d $(PWD) || open http://127.0.0.1:$(PORT)"
	$(PYTHON3) -m http.server $(PORT) --bind 127.0.0.1 -d $(PWD) > /dev/null 2>&1 || open http://127.0.0.1:$(PORT)

.PHONY: failure
failure:
	@-/usr/bin/false && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"
.PHONY: success
success:
	@-/usr/bin/true && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"

.PHONY:
##	:
##:	gui
gui:
	pushd x20bf/gui && $(PYTHON3) mainwindow.py && popd
##	:
##:	make                 venv && . venv/bin/activate

.PHONY: docker docker-build
##	:
##:	docker               build an alpine docker container
docker: docker-build
docker-build:
	$(MAKE) -C docker build-alpine alpine
.PHONY: docker-test
##	:
##:	docker-test          build an alpine docker container
docker-test:
	$(MAKE) -C docker alpine-test user=$(user)

.PHONY: push-subtrees
##	:
##:	push-subtrees        push all subtrees to their repos
push-subtrees: pre-commit
	# git ls-subtrees
	git subtree push --prefix=x20bf/depends/cryptography                      git@github.com:0x20bf-org/cryptography $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/tor                               git@github.com:0x20bf-org/tor          $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/git/git/ext/gitdb/gitdb/ext/smmap git@github.com:0x20bf-org/smmap        $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/git/git/ext/gitdb                 git@github.com:0x20bf-org/gitdb        $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/git                               git@github.com:0x20bf-org/git          $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/gnupg                             git@github.com:0x20bf-org/gnupg        $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/fastapi                           git@github.com:0x20bf-org/fastapi      $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/p2p                               git@github.com:0x20bf-org/p2p          $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=x20bf/depends/git/git/ext/gitdb/gitdb/ext/smmap git@github.com:0x20bf-org/smmap.git    $(TIME)-$(shell git rev-parse --short HEAD)
	git subtree push --prefix=docker                                          git@github.com:0x20bf-org/docker.git   $(TIME)-$(shell git rev-parse --short HEAD)
