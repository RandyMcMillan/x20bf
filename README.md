<H2>0x20bf - python implementation</H2>

[🐝](https://keys.openpgp.org/vks/v1/by-fingerprint/E616FA7221A1613E5B99206297966C06BB06757B) [🥕](https://keys.openpgp.org/vks/v1/by-fingerprint/57C5E8BB2F2746C3474B8A511421BF6C4DC9817F) [Github](http://github.com/0x20bf-org) [Twitter](https://twitter.com/0x20bf_org)
<html>
<link rel="shortcut icon" href="x20bf/sources/favicon.ico" />
</html>

<br>[![python.yml](https://github.com/0x20bf-org/x20bf/actions/workflows/python.yml/badge.svg)](https://github.com/0x20bf-org/x20bf/actions/workflows/python.yml)

## Getting Started

##### [git](https://git-scm.com/downloads)

```
git clone https://github.com/x20bf-org/x20bf.git
cd x20bf
```

##### [python@3.8+](https://www.python.org/downloads/)

```
git clone https://github.com/x20bf-org/x20bf.git
cd x20bf
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

##### [make](https://www.gnu.org/software/make/)
  
 	help
 	
 	report               environment args
 	
 	init                 initialize requirements
 	initialize           run 0x020bf/scripts/initialize
 	requirements         pip install --user -r requirements.txt
 	
 	poetry-build
 	poetry-install
 	
 	venv                 create python3 virtual environment
 	test-venv            source .venv/bin/activate; pip install -r requirements.txt;
 	test-test            python3 ./tests/test.py
 	test-venv-p2p        p2p  test battery
 	test-venv-p2ps       p2ps test battery
 	test-depends         test-gnupg test-p2p
 	test-gnupg           python3 ./tests/depends/gnupg/test_gnupg.py
 	test-p2p             python3 ./tests/depends/p2p/setup.py
 	venv-clean           rm -rf venv rokeys test_gnupg.log
 	test-p2p             python3 ./tests/test.py
 	
 	PACKAGE
 	
 	build                python3 setup.py build
 	install              python3 -m pip install -e .
 	dist                 python3 setup.py bdist_egg sdist
   
 	SUB-PACKAGES
 	
 	        depends
 	install-depends      install python <packages>
 	install-gnupg        install python gnupg
 	install-p2p          install python p2pnetwork
 	install-git          install python GitPython
 	install-tor          install python torpy
 	install-rustup       install rust toolchain
  
 	pre-commit           pre-commit run -a
 	                     install .git/hooks/pre-commit
  
 	docs                 build docs from sources/*.md
 	clean                rm -rf build
 	serve                serve repo on $(PORT)
 	
 	gui
 	
 	make                 venv && . venv/bin/activate
 	
 	docker               build an alpine docker container
 	
 	docker-test          build an alpine docker container
 	
 	brew-bundle          brew bundle --file Brewfile
 	
 	push-subtrees        push all subtrees to their repos

## [Contributing](./sources/CONTRIBUTING.md)

Check linting and formatting

```shell
  pre-commit run -a
```

Build for distribution

```shell
  python3 setup.py build
```

---

<details>
<summary>Referral Links:</summary>
<p>

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%202.svg)](https://www.digitalocean.com/?refcode=ae5c7d05da91&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

</p>
</details>
