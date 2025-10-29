select
    c.name
from
    customer as c
where
    (1 = 2)
    or c.referee_id <> 2
    or c.referee_id is null