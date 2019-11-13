
CWD		= $(CURDIR)
MODULE	= $(notdir $(CWD))

PY		= $(CWD)/bin/python3
PIP		= $(CWD)/bin/pip3

run: $(MODULE).py $(MODULE).ini
	$(PY) $^

MERGE  = Makefile README.md .gitignore
MERGE += $(MODULE).py $(MODULE).ini static templates

merge: $(MERGE)
	git checkout master
	git checkout shadow -- $(MERGE)

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
