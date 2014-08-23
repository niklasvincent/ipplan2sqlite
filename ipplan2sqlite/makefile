debug:
		./generate.py --debug --ipplan dynamic/ipplan --database ipplan.db --manifest dynamic/manifest --seatmap dynamic/seatmap.json 

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

draw: debug
		python viewer.py --database ipplan.db --hall D

lint:
		pep8 -r .
