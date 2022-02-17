##### [make](https://www.gnu.org/software/make/)
 	      help
 	      init                initialize requirements
 	      venv                create python3 virtual environment
 	
 	      (venv) - activate
 	make  venv && . venv/bin/activate
 	      test-venv           python3 ./tests/test.py
 	      test-gnupg          python3 ./tests/depends/gnupg/setup.py
 	                          python3 ./tests/depends/gnupg/test_gnupg.py
 	      test-clean-venv     rm -rf venv
 	      build               python3 setup.py build
 	      install             python3 -m pip install -e .
 	      report              environment args
 	      initialize          run 0x020bf/scripts/initialize
 	      requirements        pip install --user -r requirements.txt
 	      seeder              make -C 0x20bf/depends/seeder
 	      legit               make -C 0x20bf/depends/legit legit
 	      gogs                make -C 0x20bf/depends/gogs
 	      install-gnupg       install python gnupg on host
 	      gnupg-test          test depends/gnupg library
 	      install-p2p         install python p2p-network on host
 	      p2p                 install python p2p-network
 	      fastapi             install python fastapi
 	      install-fastapi     install python fastapi
 	      depends             build depends
 	      pre-commit          pre-commit run -a
 	      docs                build docs from sources/*.md
