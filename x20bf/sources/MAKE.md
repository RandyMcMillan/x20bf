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
