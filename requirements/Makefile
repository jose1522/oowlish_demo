
all.txt: clean base.txt dev.txt
	pip-compile all.in
base.txt:
	pip-compile base.in
dev.txt:
	pip-compile dev.in
clean:
	find . -name '*.txt' -exec rm -f {} \;