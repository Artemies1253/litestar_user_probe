from datetime import datetime

test_user_data = {
    "login": "test_user", "first_name": "test_name", "last_name": "test_last_name",
    "created_date": datetime(year=2020, month=1, day=1), "password": "1234", "is_supper_user": False
}

test_admin_data = {
    "login": "admin", "first_name": "Dean", "last_name": "Winchester",
    "created_date": datetime(year=2020, month=1, day=1), "password": "admin", "is_supper_user": True
}
