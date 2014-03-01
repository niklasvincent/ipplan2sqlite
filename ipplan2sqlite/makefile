test:
	  python tests/TestParser.py
	  python tests/TestNetworks.py

coverage:
	  coverage erase
	  coverage run tests/TestParser.py
	  coverage report -m
	  coverage erase
	  coverage run tests/TestNetworks.py
	  coverage report -m
