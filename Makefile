.PHONY: mine


mine:
	nohup python3 -m myweb3 mine-address > /dev/null 2>&1 &
