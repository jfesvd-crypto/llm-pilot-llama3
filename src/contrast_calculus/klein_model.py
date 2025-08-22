# src/contrast_calculus/klein_model.py

from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class KleinElement:
    """Represents an element of the Klein group Z₂ × Z₂."""
    x: int
    y: int

    def __post_init__(self):
        # Ensure values are always in Z₂
        if self.x not in (0, 1) or self.y not in (0, 1):
            raise ValueError("KleinElement coordinates must be 0 or 1.")

    def __add__(self, other: "KleinElement") -> "KleinElement":
        """Group operation: component-wise addition modulo 2."""
        return KleinElement((self.x + other.x) % 2, (self.y + other.y) % 2)

    def __repr__(self) -> str:
        """A nice representation for printing."""
        return f"({self.x},{self.y})"

    def dual(self) -> "KleinElement":
        """
        Returns the dual of the element. In an abelian group like Z₂ × Z₂,
        the dual g* is simply the inverse g⁻¹. For this group, every
        element is its own inverse.
        """
        return self

def omega_cocycle(g1: KleinElement, g2: KleinElement, g3: KleinElement) -> int:
    """
    Implements the non-trivial 3-cocycle for Z₂ × Z₂ with values in U(1)={+1, -1}.
    Formula: ω(g₁, g₂, g₃) = (-1)^(x₁(x₂y₃ + y₂x₃))
    """
    exponent = g1.x * (g2.x * g3.y + g2.y * g3.x)
    return -1 if exponent % 2 != 0 else 1

def reduce_snakes(diagram: List[KleinElement]) -> List[KleinElement]:
    """
    Applies the "snake identities" (Zorro's Law) to a planar diagram.
    It finds and removes adjacent pairs of an element and its dual (g, g*).
    The process is repeated until no more reductions are possible.
    """
    reduced_diagram = diagram[:]
    while True:
        found_reduction = False
        if len(reduced_diagram) < 2:
            break
        
        next_diagram = []
        i = 0
        while i < len(reduced_diagram):
            if i + 1 < len(reduced_diagram) and reduced_diagram[i+1] == reduced_diagram[i].dual():
                # Found a pair (g, g*), skip both
                i += 2
                found_reduction = True
            else:
                next_diagram.append(reduced_diagram[i])
                i += 1
        
        reduced_diagram = next_diagram
        if not found_reduction:
            break
            
    return reduced_diagram

# --- Group elements for convenience ---
e = KleinElement(0, 0)
a = KleinElement(1, 0)
b = KleinElement(0, 1)
c = KleinElement(1, 1)

# --- Demonstration of new functionality ---
if __name__ == "__main__":
    print("--- Testing dual() method ---")
    print(f"Dual of a: {a.dual()} (should be {a})")
    print(f"Dual of c: {c.dual()} (should be {c})")
    print("-" * 20)

    print("--- Testing snake reduction ---")
    simple_loop = [b, b.dual()]
    print(f"Reducing simple loop {simple_loop} -> {reduce_snakes(simple_loop)} (should be [])")

    complex_diagram = [a, c, c.dual(), b, a, a.dual()]
    print(f"Reducing complex diagram {complex_diagram} -> {reduce_snakes(complex_diagram)} (should be [{b}])")
    
    no_reduction = [a, b, c]
    print(f"Reducing {no_reduction} -> {reduce_snakes(no_reduction)} (should be [{a}, {b}, {c}])")
    print("-" * 20)
