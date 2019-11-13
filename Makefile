
CWD		= $(CURDIR)
MODULE	= $(notdir $(CWD))

PY		= $(CWD)/bin/python3
PIP		= $(CWD)/bin/pip3

run: $(MODULE).py $(MODULE).ini
	$(PY) $^

install: $(PIP) $(MODULE).py $(MODULE).ini
	$(MAKE) update

update: requirements.txt
	$(PIP) install -U pip
	$(PIP) install -U -r $<
	$(MAKE) $<

.PHONY: requirements.txt
requirements.txt:
	- $(PIP) freeze | grep -v 0.0.0 > $@

venv: $(PIP)
$(PIP):
	python3 -m venv .
