.PHONY: all html serve pdf clean

all:
	pip install ../../.. --user
	../../../doker/main.py --html simple

html:
	../../../doker/main.py --html simple
	
serve:
	cd output && python3 -m http.server

clean:
	rm -rvf output
