select
    p.product_name,
    s.year,
    s.price
from
    sales as s
left join
    product as p
using
    (product_id);