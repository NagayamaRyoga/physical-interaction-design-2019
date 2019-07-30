.PHONY: all clean

all:
	${MAKE} -C serial-led-pi

clean:
	${RM} -r __pycache__ *.pyc
	${MAKE} -C serial-led-pi clean
