PYTHON = python3

.PHONY: new
new:
	$(PYTHON) ./scripts/new.py $(NAME)

.PHONY: sync
sync:
	$(PYTHON) ./scripts/sync.py

.PHONY: test
test:
	$(PYTHON) -m unittest discover -v --start-directory ./scripts
