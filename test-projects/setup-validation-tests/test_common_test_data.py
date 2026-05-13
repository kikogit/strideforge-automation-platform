import pytest
from common_utils.test_data import TestDataManager
from common_utils.exceptions import TestDataError

def test_test_data_manager_loads_common_users_json():
    manager = TestDataManager()
    data = manager.load_json("common/positive/users.json")
    assert "valid_user" in data
    assert data["valid_user"]["username"] == "test.user@example.com"

def test_test_data_manager_loads_api_posts_json():
    manager = TestDataManager()
    data = manager.load_json("api/positive/posts.json")
    assert "create_post" in data
    assert data["create_post"]["title"] == "automation framework"

def test_test_data_manager_loads_ui_login_yaml():
    manager = TestDataManager()
    data = manager.load_yaml("ui/positive/login_users.yaml")
    assert "valid_login" in data
    assert data["valid_login"]["username"] == "test.user@example.com"

def test_test_data_manager_gets_json_record():
    manager = TestDataManager()
    data = manager.get_json_record("common/positive/users.json", "admin_user")
    assert data["username"] == "admin.user@example.com"
    assert data["role"] == "admin_user"

def test_test_data_manager_gets_yaml_record():
    manager = TestDataManager()
    data = manager.get_yaml_record("ui/positive/login_users.yaml", "valid_login")
    assert data["username"] == "test.user@example.com"
    assert data["expected_role"] == "standard_user"

def test_test_data_manager_raises_error_for_missing_file():
    manager = TestDataManager()
    with pytest.raises(TestDataError):
        manager.load_json("common/positive/missing_file.json")
    

def test_test_data_manager_raises_error_for_missing_record():
    manager = TestDataManager()
    with pytest.raises(TestDataError):
        manager.get_json_record("common/positive/users.json", "missing_user")  