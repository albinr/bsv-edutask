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
def test_duplicate_description_raises_writeerror(dao):
  """
  Test case 2
  Test that inserting a duplicate 'description' raises WriteError due to uniqueness constraint.
  """
  # Arrange
  test_input_data = {"description": "Duplicate task", "done": False} # First insert
  dao.create(test_input_data)

  # Assert
  with pytest.raises(WriteError):
    # Act
    dao.create(test_input_data) # Second insert with same description


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_int_input_raises_writeerror(dao):
  """
  Test case 3
  Test that inserting a int raises writeerror.
  """
  test_input_data = 2
  with pytest.raises(WriteError):
      dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_list_input_raises_writeerror(dao):
  """
  Test case 4
  Test that inserting a int raises writeerror.
  """  
  test_input_data = ["description", "List input", "done", True]
  with pytest.raises(WriteError):
      dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_missing_properties_raises_writeerror(dao):
  """
  Test case 5
  Test that invalid input data raises WriteError (missing required properties).
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
def test_valid_todo_without_done_is_inserted(dao):
  """
  Test case 6
  Test that a todo with only 'description' is inserted (since "done" is optional).
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
def test_invalid_data_raises_writeerror(dao):
  """
  Test case 7
  Test that missing required "description" raises WriteError.
  """
  # Arrange
  test_input_data = {"blabla": 100, "wrong": "true"}

  # Act
  with pytest.raises(WriteError):
      dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_input_empty_dict_raises_writeerror(dao):
  """
  Test case 8
  Test that inserts empty dict type raises WriteError.
  """
  # Arrange
  test_input_data = {}
  # Act
  with pytest.raises(WriteError):
    # Assert
    dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_invalid_done_type_raises_writeerror(dao):
  """
  Test case 9
  Test that invalid "done" type raises WriteError.
  """
  # Arrange
  test_input_data = {"description": "wrong type", "done": "no"}
  # Act
  with pytest.raises(WriteError):
    # Assert
    dao.create(test_input_data)


@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_extra_field_is_allowed(dao):
  """
  Test case 10
  Test that extra field "extra" is allowed and stored correctly.
  """
  # Arrange
  test_input_data = {"description": "test with extra field", "done": True, "extra": "extra field"}
  # Act
  result = dao.create(test_input_data)
  # Assert
  assert result["extra"] == "extra field"
