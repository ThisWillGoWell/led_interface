rsync -r --exclude=".*" . pi@192.168.2.28:~/wall_controller
exit 0
ssh pi@192.168.2.28 sudo python ~/wall_controller/gpio/cp.py