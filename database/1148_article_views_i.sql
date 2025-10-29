select
    distinct
    t.author_id as id
from
    views as t
where
    (1 = 1)
    and t.author_id = t.viewer_id
order by
    id