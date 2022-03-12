SHELL                                   := /bin/bash
PWD                                     ?= pwd_unknown
TIME                                    := $(shell date +%s)
export TIME

GPGBINARY                               := $(shell which gpg)
export GPGBINARY
PYTHON                                  := $(shell which python)
export PYTHON
PYTHON2                                 := $(shell which python2)
export PYTHON2
PYTHON3                                 := $(shell which python3)
export PYTHON3

PIP                                     := $(notdir $(shell which pip))
export PIP
PIP2                                    := $(notdir $(shell which pip2))
export PIP2
PIP3                                    := $(notdir $(shell which pip3))
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

	endif
	ifeq ($(UNAME_S),Darwin)

	endif
	UNAME_P := $(shell uname -p)
	ifeq ($(UNAME_P),x86_64)

	endif
	ifneq ($(filter %86,$(UNAME_P)),)

	endif
	ifneq ($(filter arm%,$(UNAME_P)),)

	endif
endif

ifeq ($(PYTHON3),/usr/local/bin/python3)
PIP                                    := pip
PIP3                                   := pip
export PIP
export PIP3
endif

ifeq ($(project),)
PROJECT_NAME                            := $(notdir $(PWD))
else
PROJECT_NAME                            := $(project)
endif
export PROJECT_NAME
PYTHONPATH=$(PWD)/0x20bf
export PYTHONPATH
DEPENDSPATH=$(PWD)/0x20bf/depends
export DEPENDSPATH
BUILDPATH=$(PWD)/build
export BUILDPATH
ifeq ($(port),)
PORT                                    := 0
else
PORT                                    := $(port)
endif
export PORT

#GIT CONFIG
GIT_USER_NAME                           := $(shell git config user.name)
export GIT_USER_NAME
ifneq ($(USER),runner)
USER:=--user
else
USER:=
endif
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

BASENAME := $(shell basename -s .git `git config --get remote.origin.url`)
export BASENAME

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

SPHINXOPTS            =
SPHINXBUILD           = sphinx-build
PAPER                 =
BUILDDIR              = _build
PRIVATE_BUILDDIR      = _private_build

# Internal variables.
PAPEROPT_a4           = -D latex_paper_size=a4
PAPEROPT_letter       = -D latex_paper_size=letter
ALLSPHINXOPTS         = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
PRIVATE_ALLSPHINXOPTS = -d $(PRIVATE_BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

ifneq ($(shell id -u),0)
DASH_U:=-U
else
DASH_U:=
endif
export DASH_U


.PHONY: - help
##	make:command
##	:
##	:help
-: help

.PHONY: init initialize requirements
##	:report              environment args
##	:init                initialize requirements
init: initialize requirements
	# remove this artifact from gnupg tests
	sudo rm -rf rokeys/.gitignore
.PHONY: initialize
##	:initialize          run 0x020bf/scripts/initialize
initialize:
	bash -c "./0x20bf/scripts/initialize"
.PHONY: requirements reqs

reqs: requirements
##	:requirements        pip install --user -r requirements.txt
requirements:
	$(PYTHON3) -m $(PIP) install $(DASH_U) --upgrade pip
	$(PYTHON3) -m $(PIP) install $(DASH_U) -r requirements.txt


.PHONY: venv
##	:
##	:venv                create python3 virtual environment
venv:
	test -d venv || virtualenv venv
	( \
	   source venv/bin/activate; pip install -r requirements.txt; \
	);
	@echo "To activate (venv)"
	@echo "try:"
	@echo ". venv/bin/activate"
	@echo "or:"
	@echo "make test-venv"
##	:test-venv           python3 ./tests/test.py
test-venv:
	# insert test commands here
	test -d venv || virtualenv venv --always-download
	( \
	   source venv/bin/activate; pip install -r requirements.txt; \
       python3 tests/test.py; \
       python3 tests/test_import.py; \
	);
test-venv-p2p:
	# insert test commands here
	test -d venv || virtualenv venv --always-download
	( \
	   source venv/bin/activate; pip install -r requirements.txt; \
       python3 0x20bf/depends/p2p/setup.py build; \
       python3 0x20bf/depends/p2p/setup.py install; \
       python3 tests/test_node_ping.py; \
	);
##	:tests-depends       test-gnupg test-p2p test-fastapi
test-depends: test-gnupg test-p2p test-fastapi
##	:test-gnupg          python3 ./tests/depends/gnupg/test_gnupg.py
##	:test-p2p            python3 ./tests/depends/p2p/setup.py
##	:test-fastapi        TODO:
##	:test-clean-venv     rm -rf venv
test-clean-venv:
	rm -rf venv
test-gnupg: venv
	. venv/bin/activate;
	$(PYTHON3) ./tests/depends/gnupg/setup.py install;
	$(PYTHON3) ./tests/depends/gnupg/test_gnupg.py;
test-p2p: venv
	. venv/bin/activate;
	pushd tests/depends/p2p && python3 setup.py install && python3 examples/my_own_p2p_application.py && popd
test-fastapi: venv
	. venv/bin/activate;
	pushd tests/depends/p2p && python3 setup.py install && python3 examples/my_own_p2p_application.py && popd
##	:


clean-venv:
	rm -rf venv

.PHONY: build install
##	:build               python3 setup.py build
build:
	python3 setup.py build
install:
##	:install             python3 -m pip install -e .
install: build
	$(PYTHON3) -m $(PIP) install -e .

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
	@echo '        - BASENAME=${BASENAME}'
	@echo '        - PROJECT_NAME=${PROJECT_NAME}'
	@echo '        - GPGBINARY=${GPGBINARY}'
	@echo '        - PYTHON3=${PYTHON3}'
	@echo '        - PIP=${PIP}'
	@echo '        - PYTHONPATH=${PYTHONPATH}'
	@echo '        - DEPENDSPATH=${DEPENDSPATH}'
	@echo '        - BUILDPATH=${BUILDPATH}'
	@echo '        - GIT_USER_NAME=${GIT_USER_NAME}'
	@echo '        - GIT_USER_EMAIL=${GIT_USER_EMAIL}'
	@echo '        - GIT_SERVER=${GIT_SERVER}'
	@echo '        - GIT_PROFILE=${GIT_PROFILE}'
	@echo '        - GIT_BRANCH=${GIT_BRANCH}'
	@echo '        - GIT_HASH=${GIT_HASH}'
	@echo '        - GIT_PREVIOUS_HASH=${GIT_PREVIOUS_HASH}'
	@echo '        - GIT_REPO_ORIGIN=${GIT_REPO_ORIGIN}'
	@echo '        - GIT_REPO_NAME=${GIT_REPO_NAME}'
	@echo '        - GIT_REPO_PATH=${GIT_REPO_PATH}'
	@echo ''

.PHONY: install-gnupg
##	:install-gnupg       install python gnupg on host
gnupg: install-gnupg
install-gnupg:
	pushd $(DEPENDSPATH)/gnupg && $(PYTHON3) $(DEPENDSPATH)/gnupg/setup.py install && popd
.PHONY: install-p2p
##	:install-p2p         install python p2p-network
p2p: install-p2p
install-p2p:
	pushd $(DEPENDSPATH)/p2p && $(PYTHON3) $(DEPENDSPATH)/p2p/setup.py install && popd

.PHONY: install-fastapi fastapi
##	:install-fastapi     install python fastapi
fastapi: install-fastapi
install-fastapi:
	pushd $(DEPENDSPATH)/fastapi && $(PYTHON3) -m $(PIP) check . && popd
	pushd $(DEPENDSPATH)/fastapi && $(PYTHON3) -m $(PIP) install . && popd




.PHONY: twitter-api


.PHONY: depends
##	:depends             build depends
depends: install-gnupg install-fastapi install-p2p

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
	git add --ignore-errors 0x20bf/*.py
	git add --ignore-errors index.html
	git add --ignore-errors .gitignore
	git add --ignore-errors .github
	git add --ignore-errors *.sh
	git add --ignore-errors *.yml
	#git add --ignore-errors BLOCK_TIP_HEIGHT
	#git add --ignore-errors DIFFICULTY
	#git add --ignore-errors TIME

.PHONY: pre-commit
##	:pre-commit          pre-commit run -a
pre-commit:
	pre-commit run -a

.PHONY: docs
##	:docs                build docs from sources/*.md
docs:
	@echo "##### [make](https://www.gnu.org/software/make/)" > $(PWD)/0x20bf/sources/MAKE.md
	bash -c "make help >> $(PWD)/0x20bf/sources/MAKE.md"
	bash -c 'cat $(PWD)/0x20bf/sources/HEADER.md                >  $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/PROTOCOL.md              >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/COMMANDS.md              >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/GETTING_STARTED.md       >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/MAKE.md                  >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/CONTRIBUTING.md          >> $(PWD)/README.md'
	bash -c 'cat $(PWD)/0x20bf/sources/FOOTER.md                >> $(PWD)/README.md'
	#brew install pandoc
	bash -c "if hash pandoc 2>/dev/null; then echo; fi || brew install pandoc"
	bash -c 'pandoc -s README.md -o index.html  --metadata title="$(BASENAME)" '
	# bash -c 'pandoc -s README.md -o index.html'
	#bash -c "if hash open 2>/dev/null; then open README.md; fi || echo failed to open README.md"
	git add --ignore-errors $(PWD)/0x20bf/sources/*.md
	git add --ignore-errors *.md
	git add --ignore-errors *.html
	#git ls-files -co --exclude-standard | grep '\.md/$\' | xargs git

.PHONY: clean

clean:
	#bash -c "rm -rf $(BUILDDIR)"

.PHONY: serve

serve:
	bash -c "$(PYTHON3) -m http.server $(PORT) -d . &"

.PHONY: failure
failure:
	@-/bin/false && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"
.PHONY: success
success:
	@-/bin/true && ([ $$? -eq 0 ] && echo "success!") || echo "failure!"


##	:
##	:make   venv && . venv/bin/activate