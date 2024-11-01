import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal
from unittest.mock import ANY

@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_meal_stats(mocker):
    """Mock the update_meal_stats function for testing purposes."""
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

"""Fixtures providing sample meals for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(1, 'Sushi', 'Japanese', 30, 'HIGH')

@pytest.fixture
def sample_meal2():
    return Meal(2, 'Pizza', 'Italian', 10, 'MED')

@pytest.fixture
def sample_combatants(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True
    return Any()

##################################################
# Prep Combatant Management Test Cases
##################################################
def test_add_meal_to_battle(battle_model, sample_meal1):
    """Test adding a meal to the battle."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Sushi'

def test_add_meal_to_full_battle(battle_model, sample_combatants, sample_meal1):
    """Test adding a meal to a full battle."""
    battle_model.combatants.extend(sample_combatants)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal1)
##################################################
# Remove Combatants Management Test Cases
##################################################
def test_clear_combatants(battle_model, sample_meal1):
    """Test clearing the entire combatants list."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Playlist should be empty after clearing"
##################################################
# Combantants Retrieval Test Cases
##################################################
def test_get_combatants(battle_model, sample_combatants):
    """Test successfully retrieving all meals from the battle."""
    battle_model.combatants.extend(sample_combatants)
    combatants = battle_model.get_combatants()
    assert len(combatants) == 2
    assert combatants[0].id == 1
    assert combatants[1].id == 2

##################################################
# Battle Score Test Cases
##################################################
def test_get_battle_score_1(battle_model, sample_meal1):
    """Test the get_battle_score method with sample_meal1."""
    difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}
    score = battle_model.get_battle_score(sample_meal1)
    correct_score = (sample_meal1.price * len(sample_meal1.cuisine)) - difficulty_modifier[sample_meal1.difficulty]
    assert score == correct_score

def test_get_battle_score_2(battle_model, sample_meal2):
    """Test the get_battle_score method with sample_meal2."""
    difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}
    score = battle_model.get_battle_score(sample_meal2)
    correct_score = (sample_meal2.price * len(sample_meal2.cuisine)) - difficulty_modifier[sample_meal2.difficulty]
    assert score == correct_score

##################################################
# Battle Test Cases
##################################################
def test_battle(battle_model, sample_combatants, mock_update_meal_stats):
    """Test the battle_model method."""
    battle_model.combatants.extend(sample_combatants)
    winner_meal = battle_model.battle()
    mock_update_meal_stats.assert_any_call(1, Any(str))
    mock_update_meal_stats.assert_any_call(2, Any(str))
    assert mock_update_meal_stats.call_count == 2
    assert battle_model.combatants[0].meal == winner_meal

def test_empty_battle(battle_model):
    """Test the battle_model method with no combatants."""
    assert len(battle_model.get_combatants()) == 0
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle"):
        battle_model.battle()

def test_one_combatant_battle(battle_model, sample_meal1):
    """Test the battle_model method with only one combatant."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.get_combatants()) == 1
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle"):
        battle_model.battle()
