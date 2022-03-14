##### [make](https://www.gnu.org/software/make/)
 	
 	  help
 	  report              environment args
 	  init                initialize requirements
 	  initialize          run 0x020bf/scripts/initialize
 	  requirements        pip install --user -r requirements.txt
 	
 	  venv                create python3 virtual environment
 	  test-venv           python3 ./tests/test.py
 	  test-venv-p2p       p2p test battery
 	  test-depends        test-gnupg test-p2p test-fastapi
 	  test-gnupg          python3 ./tests/depends/gnupg/test_gnupg.py
 	  test-p2p            python3 ./tests/depends/p2p/setup.py
 	  venv-clean          rm -rf venv rokeys test_gnupg.log
 	
 	  build               python3 setup.py build
 	  install             python3 -m pip install -e .
 	  dist                python3 setup.py bdist_egg sdist
 	
 	  install-gnupg       install python gnupg on host
 	  install-p2p         install python p2p-network
 	  install-fastapi     install python fastapi
 	  depends             build and install depends
 	  pre-commit          pre-commit run -a
 	  docs                build docs from sources/*.md
 	  clean               rm -rf build
 	
 	  make   venv && . venv/bin/activate