##### [make](https://www.gnu.org/software/make/)
 	make  command
 	
 	      help
 	      report              environment args
 	      init                initialize requirements
 	      initialize          run 0x020bf/scripts/initialize
 	      requirements        pip install --user -r requirements.txt
 	
 	      venv                create python3 virtual environment
 	      test-venv           python3 ./tests/test.py
 	      tests-depends       test-gnupg test-p2p test-fastapi
 	      test-gnupg          python3 ./tests/depends/gnupg/test_gnupg.py
 	      test-p2p            python3 ./tests/depends/p2p/setup.py
 	      test-fastapi        TODO
 	      test-clean-venv     rm -rf venv
 	
 	      build               python3 setup.py build
 	      install             python3 -m pip install -e .
 	      install-gnupg       install python gnupg on host
 	      install-p2p         install python p2p-network
 	      install-fastapi     install python fastapi
 	      depends             build depends
 	      pre-commit          pre-commit run -a
 	      docs                build docs from sources/*.md
 	
 	      make   venv && . venv/bin/activate
