import pytest
from tools.db_models import Host

def check_db_host(before_subnet, subnet):
    if before_subnet < subnet:
        return "split"
    elif before_subnet > subnet:
        return "merge"
    else:
        return "exist"
    
def check_db_mgr(host_id):
    if host_id:
        return "assigned"
    else:
        return "unassigned"
    




def test_split_host():
    status = check_db_host(24, 25)
    assert status == "split"

def test_merge_host():
    status = check_db_host(24, 23)
    assert status == "merge"

def test_exist_host():
    status = check_db_host(24, 24)
    assert status == "exist"


host = Host()

host.id = 1

def test_assigned_mgr():
    mgr = check_db_mgr(host)
    assert mgr == "assigned"

host.id = 1

def test_assigned_sub_mgr():
    mgr = check_db_mgr(host)
    assert mgr == "assigned"

host.id = None

def test_unassigned_mgr():
    mgr = check_db_mgr(host.id)
    assert mgr == "unassigned"


def test_unassigned_sub_mgr():
    mgr = check_db_mgr(host.id)
    assert mgr == "unassigned"