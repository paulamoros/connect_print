

all:
	sudo python3 setup.py

clean:
	sudo rm -drf d_imprimante*
	sudo rm printers_infos.txt
	sudo rm locks/*

