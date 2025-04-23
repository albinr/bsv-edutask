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

    return dao

@pytest.mark.integration
@pytest.mark.lab1
@pytest.mark.lab1assignment3
def test_missing_properties_raises_writeerror(dao):
  """
  Test case:
  Test that invalid email raises ValueError
  """
  # Arrange
  test_input_data = {
    "done": False,
  }

  # Assert
  with pytest.raises(WriteError):
      # Act
      dao.create(test_input_data)
