test:
	  python tests/TestParser.py
	  python tests/TestNetworks.py
	  python tests/TestFirewall.py

coverage:
	  coverage erase
	  coverage run tests/TestParser.py
	  coverage report -m
	  coverage erase
	  coverage run tests/TestNetworks.py
	  coverage report -m
	  coverage erase
	  coverage run tests/TestFirewall.py
	  coverage report -m
