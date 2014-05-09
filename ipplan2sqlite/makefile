debug:
		./generate.py --debug --ipplan dynamic/ipplan --database ipplan.db --services dynamic/services --flows dynamic/flows --seatmap dynamic/seatmap.json 

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
