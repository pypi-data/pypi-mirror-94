import matplotlib
import mpmath
import numpy
import scipy.special

import cplot


def test_create():
    rgb = cplot.create_colormap(L=50)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "custom", rgb.T, N=len(rgb.T)
    )
    # cmap = 'gray'

    cplot.show_linear(rgb)
    cplot.show_circular(rgb, rot=-numpy.pi * 4 / 12)
    # cplot.show_circular(rgb, rot=-numpy.pi * 18/12)
    cplot.show_kovesi_test_image(cmap)
    # cplot.show_kovesi_test_image_circular(cmap)


def zeta(z):
    vals = [[mpmath.zeta(val) for val in row] for row in z]
    out = numpy.array(
        [[float(val.real) + 1j * float(val.imag) for val in row] for row in vals]
    )
    return out


def test_array():
    numpy.random.seed(0)
    n = 5
    z = numpy.random.rand(n) + 1j * numpy.random.rand(n)
    vals = cplot.get_srgb1(z)
    assert vals.shape == (n, 3)


def test_cam16():
    # cplot.savefig("z6_1.png", lambda z: z ** 6 - 1, -2, +2, -2, +2, 200, 200)
    # cplot.savefig(
    #     "f025.png",
    #     lambda z: (z ** 2 - 1) * (z - 2 - 1j) ** 2 / (z ** 2 + 2 + 2j),
    #     -3,
    #     +3,
    #     -3,
    #     +3,
    #     200,
    #     200,
    #     alpha=0.25
    # )

    n = 401
    cplot.imsave("z1.png", lambda z: z ** 1, -2, +2, -2, +2, n, n)
    cplot.imsave("z2.png", lambda z: z ** 2, -2, +2, -2, +2, n, n)
    cplot.imsave("z3.png", lambda z: z ** 3, -2, +2, -2, +2, n, n)

    cplot.savefig("1z.png", lambda z: 1 / z, -2, +2, -2, +2, 100, 100)
    cplot.savefig("z-absz.png", lambda z: z / abs(z), -2, +2, -2, +2, 100, 100)
    cplot.savefig("z+1-z-1.png", lambda z: (z + 1) / (z - 1), -5, +5, -5, +5, 101, 101)

    cplot.savefig("root2.png", numpy.sqrt, -2, +2, -2, +2, 200, 200)
    cplot.savefig("root3.png", lambda x: x ** (1 / 3), -2, +2, -2, +2, 200, 200)
    cplot.savefig("root4.png", lambda x: x ** 0.25, -2, +2, -2, +2, 200, 200)

    cplot.savefig("log.png", numpy.log, -2, +2, -2, +2, 200, 200)
    cplot.savefig("exp.png", numpy.exp, -2, +2, -2, +2, 200, 200)
    cplot.savefig("exp1z.png", lambda z: numpy.exp(1 / z), -1, +1, -1, +1, 200, 200)

    cplot.savefig("sin.png", numpy.sin, -5, +5, -5, +5, 200, 200)
    cplot.savefig("cos.png", numpy.cos, -5, +5, -5, +5, 200, 200)
    cplot.savefig("tan.png", numpy.tan, -5, +5, -5, +5, 200, 200)

    cplot.savefig("sinh.png", numpy.sinh, -5, +5, -5, +5, 200, 200)
    cplot.savefig("cosh.png", numpy.cosh, -5, +5, -5, +5, 200, 200)
    cplot.savefig("tanh.png", numpy.tanh, -5, +5, -5, +5, 200, 200)

    cplot.savefig("arcsin.png", numpy.arcsin, -2, +2, -2, +2, 200, 200)
    cplot.savefig("arccos.png", numpy.arccos, -2, +2, -2, +2, 200, 200)
    cplot.savefig("arctan.png", numpy.arctan, -2, +2, -2, +2, 200, 200)

    cplot.savefig("gamma.png", scipy.special.gamma, -5, +5, -5, +5, 200, 200)
    cplot.savefig("digamma.png", scipy.special.digamma, -5, +5, -5, +5, 200, 200)
    cplot.savefig("zeta.png", zeta, -30, +30, -30, +30, 200, 200)

    # First function from the SIAM-100-digit challenge
    # <https://en.wikipedia.org/wiki/Hundred-dollar,_Hundred-digit_Challenge_problems>
    def siam(z):
        return numpy.cos(numpy.log(z) / z) / z

    cplot.savefig("siam.png", siam, -1, 1, -1, 1, 230, 230, alpha=0.1)

    # a = 10
    # cplot.savefig("bessel0.png", lambda z: scipy.special.jv(0, z), -a, +a, -a, +a, 100, 100)
    # cplot.savefig("bessel1.png", lambda z: scipy.special.jv(1, z), -a, +a, -a, +a, 100, 100)
    # cplot.savefig("bessel2.png", lambda z: scipy.special.jv(2, z), -a, +a, -a, +a, 100, 100)
    # cplot.savefig("bessel3.png", lambda z: scipy.special.jv(3, z), -a, +a, -a, +a, 100, 100)


def test_compare_colorspaces():
    def f(z):
        return (z ** 2 - 1) * (z - 2 - 1j) ** 2 / (z ** 2 + 2 + 2j)

    names = ["cam16", "cielab", "oklab", "hsl"]

    n = 201
    for name in names:
        cplot.savefig(name + "-10.png", f, -3, +3, -3, +3, n, n, colorspace=name)
        cplot.savefig(name + "-05.png", f, -3, +3, -3, +3, n, n, 0.5, name)
        cplot.savefig(name + "-00.png", f, -3, +3, -3, +3, n, n, 0, name)


if __name__ == "__main__":
    # test_cam16()
    test_compare_colorspaces()
    # test_create()
