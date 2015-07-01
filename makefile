debug:
		./generate.py --debug --ipplan dynamic/ipplan --database ipplan.db --manifest dynamic/manifest --seatmap dynamic/seatmap.json 

test:
	  python tests/TestParser.py
	  python tests/TestNetworks.py
	  python tests/TestFirewall.py

coverage:
	  coverage erase
	  coverage run -p tests/TestParser.py
	  coverage run -p tests/TestNetworks.py
	  coverage run -p tests/TestFirewall.py
	  coverage run -p tests/TestSeatmap.py
	  coverage combine
	  coverage report -m

draw: debug
		python viewer.py --database ipplan.db --hall D

lint:
		pep8 -r .
