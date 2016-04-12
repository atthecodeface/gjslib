PYTHON = PYTHONPATH=$(CURDIR)/../python:$(PYTHONPATH) /usr/bin/env python
Q=@

all: math_tests drawing_tests

math_tests:
	$(Q)$(PYTHON) ./math/vectors.py
	$(Q)$(PYTHON) ./math/bezier.py
	$(Q)$(PYTHON) ./math/quaternion.py

drawing_tests:
	$(Q)$(PYTHON) ./graphics/drawing.py
