import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def usercontroller():
    dao = MagicMock(spec=DAO)
    usercontroller = UserController(dao)

    return usercontroller

@pytest.mark.unit
@pytest.mark.lab1
@pytest.mark.parametrize(
    "test_input_email",
    [
      ("@domain.com"),
      ("name@.com"),
      ("name@domain"),
      ("namedomaincom"),
    ]
)
def test_invalid_email_raises_valueerror(usercontroller, test_input_email):
    # Test Case 5, 6, 7
      with pytest.raises(ValueError):
          usercontroller.get_user_by_email(test_input_email)
