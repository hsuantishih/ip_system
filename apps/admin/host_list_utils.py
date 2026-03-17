from sqlalchemy import func, Integer
from admin.models import Host
from admin.forms import SearchIpForm

def build_filter(search_username=None, search_deptname=None, search_type="全部類別", search_class_c="Class C"):
        from auth.models import User
        """Build the filter criteria dynamically based on the input."""
        filters = [Host.deleted == False]
        
        if search_username:
            filters.append(Host.users.any(User.username.like(f"%{search_username}%")))
        if search_deptname:
            filters.append(Host.host_deptname.like(f"%{search_deptname}%"))
        if search_type != "全部類別":
            filters.append(Host.host_type == search_type)
        if search_class_c != "Class C":
            filters.append(Host.host_class_c == search_class_c)
        
        return filters

def query_hosts(search_username=None, search_deptname=None, search_type="全部類別", search_class_c="Class C"):
    """Query hosts based on dynamic filters and ordering."""
    filters = build_filter(search_username, search_deptname, search_type, search_class_c)
    return (
        Host.query.filter(*filters)
        .order_by(
            func.substring(Host.host_class_c, 2).cast(Integer),
            func.substring(Host.host_min, 2).cast(Integer),
        )
        .all()
    )


def query_and_append_choices(form_type, query_condition, transform_func):
     query_results = Host.query.with_entities(query_condition).all()

     getattr(SearchIpForm, form_type).choices = []

     for result in sorted(set(query_results)):
          result_tuple = (transform_func(result))
          getattr(SearchIpForm, form_type).choices.append(result_tuple)

print(build_filter())