import pytest
from src.rolls.dice import D4, D6, D8, D10, D12, D20, D100
from src.rolls.dice_pool import RollXDX


@pytest.mark.parametrize(
    "dx,x,upper_range",
    [
        pytest.param(D4, 10, 10 * 4, id="D4"),
        pytest.param(D6, 10, 10 * 6, id="D6"),
        pytest.param(D8, 10, 10 * 8, id="D8"),
        pytest.param(D10, 10, 10 * 10, id="D10"),
        pytest.param(D12, 10, 10 * 12, id="D12"),
        pytest.param(D20, 10, 10 * 20, id="D20"),
        pytest.param(D100, 10, 10 * 100, id="D100"),
    ],
)
def test_xdx_roll(dx, x, upper_range):
    roll_result = RollXDX(
        x=x,
        dx=dx,
    ).roll()

    assert (1 * x) <= roll_result <= (x * upper_range)
