select
    v.customer_id,
    count(*) as count_no_trans
from
    visits as v
left join
    transactions as t
using
    (visit_id)
where
    (1 = 1)
    and t.transaction_id is null
group by
    v.customer_id;