PYTHON = PYTHONPATH=$(CURDIR)/../python:$(PYTHONPATH) /usr/bin/env python
Q=@

all: math_tests drawing_tests

math_tests:
	$(Q)$(PYTHON) ./math/vectors.py
	$(Q)$(PYTHON) ./math/complex.py
	$(Q)$(PYTHON) ./math/quaternion.py
	$(Q)$(PYTHON) ./math/matrix.py
	$(Q)$(PYTHON) ./math/bezier.py
	$(Q)$(PYTHON) ./math/polynomial.py

drawing_tests:
	$(Q)$(PYTHON) ./graphics/drawing.py
