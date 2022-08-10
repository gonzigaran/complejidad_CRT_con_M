
from folpy.semantics.morphisms import Homomorphism
from folpy.semantics.lattices import LatticeProduct


def descomp_subdirecta(algebra, quasi):
    rsi = quasi.generate_rsi()
    homeos = set()
    ker = {(x, y) for x in algebra.universe for y in algebra.universe}
    mincon = {(x, x) for x in algebra.universe}
    for B in rsi:
        for f in algebra.homomorphisms_to(B, B.type, surj=True):
            ker = ker & {tuple(t) for t in f.kernel().table()}
            homeos.add(f)
    assert mincon == ker
    producto = LatticeProduct([f.target for f in homeos])
    d = {}
    for x in algebra.universe:
        d[(x,)] = tuple([f(x,) for f in homeos])
    return Homomorphism(d, algebra, producto, algebra.type)

def dos_proyeccion(homeo, i, j):
    if i > j:
        subji = dos_proyeccion(homeo, j, i)
        return [(x, y) for (y, x) in subji]
    sub = homeo.target.restrict(list(homeo.image())).universe
    subij = list(set([(x[i],x[j]) for x in sub]))
    return sorted(subij)

def dos_proyeccion_extendida(homeo, i, j):
    prod = homeo.target.universe
    subij = dos_proyeccion(homeo, i, j)
    result = [x for x in prod if (x[i],x[j]) in subij]
    return sorted(result)

def comp_ijk(homeo, i, j, k):
    aij = dos_proyeccion(homeo, i, j)
    ajk = dos_proyeccion(homeo, j, k)
    comp = [(x,y) for (x,v) in aij for (w,y) in ajk if v == w]
    return comp
