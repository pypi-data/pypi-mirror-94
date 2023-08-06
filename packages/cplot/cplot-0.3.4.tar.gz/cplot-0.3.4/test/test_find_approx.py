# Find a for such that x^a / (x^a + 1) approximates 2/pi * arctan(x) best.
# The
import matplotlib.pyplot as plt
import numpy
from scipy.optimize import minimize

x = numpy.linspace(0.0, 1.0, 10000)


def f(a):
    # diff = x ** a / (x ** a + 1) - x / 2
    diff = x ** a / (x ** a + 1) - 2 / numpy.pi * numpy.arctan(x)
    # diff = x ** a / (x ** a + 1) - (1 - 0.5 ** x)
    return numpy.max(numpy.abs(diff))


out = minimize(f, 1.2)
print(out)
print(f(out.x[0]))

a = out.x[0]
x = numpy.linspace(0.0, 1.0, 500)
plt.plot(x, x ** a / (x ** a + 1), label="x^a / (x^a + 1), a_opt")
plt.plot(x, 2 / numpy.pi * numpy.arctan(x), label="arctan")
plt.legend()
plt.grid()
plt.show()
