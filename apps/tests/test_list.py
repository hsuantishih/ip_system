from sqlalchemy import inspect
from tools.db_models import Host, User
from utils.host_list_utils import build_filter

def test_build_filter_no_criteria():
    filters = build_filter()
    assert len(filters) == 1
    assert str(filters[0]) == str(Host.deleted == False)

def test_build_filter_with_username():
    filters = build_filter(search_username="test_user")
    assert len(filters) == 2
    assert str(filters[0]) == str(Host.deleted == False)
    assert str(filters[1]) == str(Host.users.any(User.username.like("%test_user%")))

def test_build_filter_with_deptname():
    filters = build_filter(search_deptname="test_dept")
    assert len(filters) == 2
    assert str(filters[0]) == str(Host.deleted == False)
    assert str(filters[1]) == str(Host.host_deptname.like("%test_dept%"))

def test_build_filter_with_type():
    filters = build_filter(search_type="test_type")
    assert len(filters) == 2
    assert str(filters[0]) == str(Host.deleted == False)
    assert str(filters[1]) == str(Host.host_type == "test_type")

def test_build_filter_with_class_c():
    filters = build_filter(search_class_c="test_class_c")
    assert len(filters) == 2
    assert str(filters[0]) == str(Host.deleted == False)
    assert str(filters[1]) == str(Host.host_class_c == "test_class_c")

def test_build_filter_with_all_criteria():
    filters = build_filter(search_username="test_user", search_deptname="test_dept", search_type="test_type", search_class_c="test_class_c")
    assert len(filters) == 5
    assert str(filters[0]) == str(Host.deleted == False)
    assert str(filters[1]) == str(Host.users.any(User.username.like("%test_user%")))
    assert str(filters[2]) == str(Host.host_deptname.like("%test_dept%"))
    assert str(filters[3]) == str(Host.host_type == "test_type")
    assert str(filters[4]) == str(Host.host_class_c == "test_class_c")