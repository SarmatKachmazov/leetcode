select
    t.name,
    t.population,
    t.area
from
    world as t
where
    (1 = 2)
    or t.area >= 3000000
    or t.population >= 25000000