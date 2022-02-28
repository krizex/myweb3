.PHONY: mine install-packages


mine:
	nohup python3 -m myweb3 mine-address > /dev/null 2>&1 &

install-packages:
	pip3 install -U --upgrade-strategy eager \
		-r requirements.txt

