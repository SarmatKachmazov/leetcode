select
    eu.unique_id,
    e.name
from
    employees as e
left join
    employeeUNI as eu
using
    (id)