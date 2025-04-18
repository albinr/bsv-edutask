import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import re

@pytest.fixture
def usercontroller():
    """
    Mock DAO and use in usercontroller as param
    """
    # Mock the DAO class
    dao = MagicMock(spec=DAO)
    usercontroller = UserController(dao)

    return usercontroller

@pytest.mark.unit
@pytest.mark.lab1
def test_user_one_match(usercontroller):
  """
  Test case 1
  Test that valid email with one match returns the user object
  """

  # Arrange
  find_return_value = [
      {
          "firstName": "John",
          "lastName": "Doe",
          "email": "user@email.com",
      }
  ]
  usercontroller.dao.find.return_value = find_return_value

  # Act
  result = usercontroller.get_user_by_email("user@email.com")

  # Assert
  assert result == {
    "firstName": "John",
    "lastName": "Doe",
    "email": "user@email.com",
  }

@pytest.mark.unit
@pytest.mark.lab1
def test_user_multiple_match(usercontroller, capfd):
  """
  Test case 2
  Test that valid email with multiple matches returns the first user object and prints out warning message containing email
  """

  # Arrange
  find_return_value = [
      {
          "firstName": "John",
          "lastName": "Doe",
          "email": "user@email.com",
      },
      {
          "firstName": "Jane",
          "lastName": "Doe",
          "email": "user@email.com",
      },
      {
          "firstName": "Erik",
          "lastName": "Doe",
          "email": "user@email.com",
      }
  ]
  usercontroller.dao.find.return_value = find_return_value

  # Act
  result = usercontroller.get_user_by_email("user@email.com")

  # Arrange (again)
  out, _ = capfd.readouterr() # Capture prints

  # Assert
  assert re.search(r"user@email\.com", out) is not None # Check for email in print

  assert result == {
    "firstName": "John",
    "lastName": "Doe",
    "email": "user@email.com",
  }

@pytest.mark.unit
@pytest.mark.lab1
def test_user_no_match(usercontroller):
  """
  Test case 3
  Test that valid email with no match returns None
  """

  # Arrange
  find_return_value = [] # No match
  usercontroller.dao.find.return_value = find_return_value

  # Act
  result = usercontroller.get_user_by_email("user@email.com")

  # Assert
  assert result == None

@pytest.mark.unit
@pytest.mark.lab1
def test_database_problem_raise_exception(usercontroller):
  """
  Test case 4
  Test that exception is raised if database has problems
  """

  # Arrange
  # Simulate database error as side_effect in mocked dao.find
  usercontroller.dao.find.side_effect = Exception("Error in database")

  # Assert
  with pytest.raises(Exception):
      # Act
      usercontroller.get_user_by_email("user@email.com")

@pytest.mark.unit
@pytest.mark.lab1
@pytest.mark.parametrize(
    "test_input_email",
    [
      ("@domain.com"),
      ("name@.com"),
      ("name@domain"),
      ("namedomaincom"),
      (""),
      (1337),

    ]
)
def test_invalid_email_raises_valueerror(usercontroller, test_input_email):
  """
  Test case 5, 6, 7, 8
  Test that invalid email raises ValueError
  """
  # Assert
  with pytest.raises(ValueError):
      # Act
      usercontroller.get_user_by_email(test_input_email)
