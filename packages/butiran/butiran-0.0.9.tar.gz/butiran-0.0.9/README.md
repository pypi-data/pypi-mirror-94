# butiran-py
Python package for simulation of grain-based system using molecular dynamics method and agent-based model


## module
- **vect3**
	+ `Vect3()` Initialize with 3 arguments or none
	+ `strval()` Get string value of Vect3 instance
	+ `add()` Add two Vect3 instances
	+ `sub()` Substract two Vect3 instances
	+ `dot()` Dot product of two Vect3 instances
	+ `cross()` Cross product of two Vect3 instances
	+ `mul()` Multiply a scalar with a Vect3 instance (or vice versa)
	+ `div()` Divide a Vect3 instance with a scalar
	+ `len()` Get length or magnitude of a Vect3 instance
	+ `unit()` Get unit vector of a Vect3 instance
	+ `neg()` Set a Vect3 instance to opposite direction


## usage
```python
from butiran.vect3 import Vect3

a = Vect3(100.001, -0.5, 2021)
print("a = " + a.strval())

b = a.neg()
print("b = " + b.strval())
```

```
a = (100.001, -0.5, 2021)
b = (-100.001, 0.5, -2021)
```