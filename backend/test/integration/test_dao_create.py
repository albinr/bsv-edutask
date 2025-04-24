import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def dao():
  """
  Initialise DAO (and database in DAO)
  """

  collection = "todo"
  dao = DAO(collection)

  dao.collection.delete_many({})  # Clear before test
  yield dao
  dao.collection.delete_many({})  # Clean up after test

@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_valid_input_does_not_raise_writeerror(dao):
  """
  Test case 1
  Test that valid input data does not raise WriteError.
  """
  # Arrange
  test_input_data = {"description": "Eat an apple", "done": True}

  # Act
  result = dao.create(test_input_data)

  # Assert
  assert result["description"] == "Eat an apple"
  assert result["done"] is True
  assert "_id" in result


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_missing_properties_raises_writeerror(dao):
  """
  Test case 2
  Test that invalid input data raises WriteError
  """
  # Arrange
  test_input_data = {
    "done": False,
  }

  # Assert
  with pytest.raises(WriteError):
      # Act
      dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_duplicate_description_raises_writeerror(dao):
  """
  Test case 3
  Test that inserting a duplicate 'description' raises WriteError due to uniqueness constraint.
  """
  # Arrange
  test_input_data = {"description": "Duplicate task", "done": False}
  dao.create(test_input_data)

  # Assert
  with pytest.raises(WriteError):
    # Act
    dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_valid_todo_without_done_is_inserted(dao):
  """
  Test case 4
  Test that a todo with only 'description' is inserted (since 'done' is optional).
  """
  # Arrange
  test_input_data = {
      "description": "Only required field"
  }

  # Act
  result = dao.create(test_input_data)

  # Assert
  assert result["description"] == "Only required field"
  assert "_id" in result


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_missing_description_raises_writeerror(dao):
  """
  Test case 5
  Test that missing required 'description' raises WriteError.
  """
  # Arrange
  test_input_data = {"done": True}

  # Act
  with pytest.raises(WriteError):
      dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_invalid_done_type_raises_writeerror(dao):
    """
    Test case 6
    Test that invalid 'done' type raises WriteError.
    """
    test_input_data = {"description": "wrong type", "done": "no"}
    with pytest.raises(WriteError):
        dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_extra_field_is_allowed(dao):
    """
    Test case 7
    Test that extra field 'category' is allowed and stored correctly.
    """
    test_input_data = {"description": "with category", "done": True, "category": "school"}
    result = dao.create(test_input_data)
    assert result["category"] == "school"

