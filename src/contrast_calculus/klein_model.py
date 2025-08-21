# src/contrast_calculus/klein_model.py

from dataclasses import dataclass

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

# Define the group elements for convenience
e = KleinElement(0, 0) # Identity
a = KleinElement(1, 0)
b = KleinElement(0, 1)
c = KleinElement(1, 1) # c = a + b

def omega_cocycle(g1: KleinElement, g2: KleinElement, g3: KleinElement) -> int:
    """
    Implements the non-trivial 3-cocycle for Z₂ × Z₂ with values in U(1)={+1, -1}.
    Formula: ω(g₁, g₂, g₃) = (-1)^(x₁(x₂y₃ + y₂x₃))
    """
    exponent = g1.x * (g2.x * g3.y + g2.y * g3.x)
    return -1 if exponent % 2 != 0 else 1

# --- Demonstration ---
if __name__ == "__main__":
    print("--- Verifying the Klein Group Z₂ × Z₂ ---")
    print(f"e = {e}, a = {a}, b = {b}, c = {c}")
    print(f"a + b = {a + b} (should be {c})")
    print(f"c + a = {c + a} (should be {b})")
    print(f"b + b = {b + b} (should be {e})")
    print("-" * 20)

    print("--- Testing the 3-cocycle ω ---")
    # Examples from our previous discussion
    val_aab = omega_cocycle(a, a, b)
    print(f"ω(a, a, b) = {val_aab} (expected -1)")

    val_abc = omega_cocycle(a, b, c)
    print(f"ω(a, b, c) = {val_abc} (expected -1)")

    val_eab = omega_cocycle(e, a, b)
    print(f"ω(e, a, b) = {val_eab} (expected 1)")
    print("-" * 20)
