import pytest

from Weight import Weight, WeightUnit


class TestWeight:

    @pytest.mark.regression
    @pytest.mark.parametrize("weight1, weight2, expected_result", [
        (Weight(10, WeightUnit.G), Weight(10, WeightUnit.G), 20),
        (Weight(1, WeightUnit.KG), Weight(10, WeightUnit.G), 1.01),
        (Weight(10, WeightUnit.KG), Weight(10, WeightUnit.LB), 14.53592),
        (10, Weight(10, WeightUnit.LB), 10.022046244201839)
    ])
    def test_adding(self, weight1: Weight, weight2: Weight, expected_result: int):
        assert weight1 + weight2 == expected_result
        weight1 += weight2
        if type(weight1) == Weight:
            assert weight1.weight == expected_result

        else:
            assert weight1 == expected_result

    @pytest.mark.regression
    @pytest.mark.parametrize("weight1, weight2, expected_result", [
        (Weight(10, WeightUnit.G), Weight(10, WeightUnit.G), 0),
        (Weight(1, WeightUnit.KG), Weight(10, WeightUnit.G), 0.99),
        (Weight(10, WeightUnit.KG), Weight(10, WeightUnit.LB), 5.46408),
        (10, Weight(10, WeightUnit.LB), 9.977953755798163)
    ])
    def test_subtracting(self, weight1: Weight, weight2: Weight, expected_result: int):
        assert weight1 - weight2 == expected_result
        weight1 -= weight2
        if type(weight1) == Weight:
            assert weight1.weight == expected_result

        else:
            assert weight1 == expected_result

