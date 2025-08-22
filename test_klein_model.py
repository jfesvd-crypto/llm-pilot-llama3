# tests/test_klein_model.py

import pytest
from hypothesis import given, strategies as st

# Importujemy nasz model, który chcemy testować
from src.contrast_calculus.klein_model import KleinElement, omega_cocycle, reduce_snakes, e, a, b, c

# --- Testy Poprawności Grupy (sanity checks) ---

def test_klein_group_operations():
    assert a + b == c
    assert c + a == b
    assert b + b == e
    assert a + a == e
    assert c + c == e
    assert a + b + c == e

# --- Testy 3-kocyklu ---

def test_omega_cocycle_specific_cases():
    """Testuje konkretne, znane wartości kocyklu."""
    assert omega_cocycle(a, a, b) == -1
    assert omega_cocycle(a, b, c) == -1
    assert omega_cocycle(e, a, b) == 1
    assert omega_cocycle(a, e, b) == 1
    assert omega_cocycle(a, b, e) == 1

# --- Test Spójności Pentagonu (Najważniejszy!) ---

def check_pentagon_identity(g1, g2, g3, g4):
    """
    Sprawdza warunek 3-kocyklu (dω=1) dla czterech elementów grupy.
    Równanie: ω(g₂,g₃,g₄) * ω(g₁,g₂g₃,g₄)⁻¹ * ω(g₁,g₂,g₃g₄) * ω(g₁g₂,g₃,g₄)⁻¹ * ω(g₁,g₂,g₃) = 1
    Ponieważ wartościami są {+1, -1}, mnożenie to to samo co dodawanie wykładników mod 2,
    a odwrotność (x⁻¹) to to samo co x.
    Więc sprawdzamy, czy iloczyn wszystkich pięciu wartości ω wynosi 1.
    """
    val1 = omega_cocycle(g2, g3, g4)
    val2 = omega_cocycle(g1, g2 + g3, g4)
    val3 = omega_cocycle(g1, g2, g3 + g4)
    val4 = omega_cocycle(g1 + g2, g3, g4)
    val5 = omega_cocycle(g1, g2, g3)

    # W naszej grupie U(1)={+1, -1}, a⁻¹ = a, więc równanie upraszcza się do:
    # ω(g₂,g₃,g₄) * ω(g₁,g₂g₃,g₄) * ω(g₁,g₂,g₃g₄) * ω(g₁g₂,g₃,g₄) * ω(g₁,g₂,g₃) = 1
    product = val1 * val2 * val3 * val4 * val5
    return product == 1

# Strategia dla Hypothesis: generuj losowe elementy grupy Kleina
klein_elements = st.sampled_from([e, a, b, c])

@given(g1=klein_elements, g2=klein_elements, g3=klein_elements, g4=klein_elements)
def test_pentagon_coherence_with_hypothesis(g1, g2, g3, g4):
    """
    Property-based test, który sprawdza warunek pentagonu dla tysięcy
    losowych kombinacji elementów grupy.
    """
    assert check_pentagon_identity(g1, g2, g3, g4)

# --- Testy Dualności i Redukcji (Twierdzenie B) ---

def test_dual_method():
    """Sprawdza, czy metoda dual() działa poprawnie (dla Z₂×Z₂ g* = g)."""
    assert a.dual() == a
    assert b.dual() == b
    assert c.dual() == c
    assert e.dual() == e

def test_snake_reductions():
    """
    Sprawdza, czy funkcja reduce_snakes poprawnie implementuje
    tożsamości wężowe ("Prawo Zorro").
    """
    # Test prostej pętli (powinna zniknąć)
    assert reduce_snakes([b, b.dual()]) == []
    assert reduce_snakes([c, c.dual()]) == []

    # Test bardziej złożonego diagramu - TUTAJ JEST POPRAWKA
    # Prawidłowy wynik to [a, b], a nie [b]
    assert reduce_snakes([a, c, c.dual(), b, a, a.dual()]) == [a, b]

    # Test diagramu bez możliwych redukcji
    assert reduce_snakes([a, b, c]) == [a, b, c]

    # Test zagnieżdżonej redukcji
    assert reduce_snakes([a, b, c, c.dual(), b.dual(), a.dual()]) == []