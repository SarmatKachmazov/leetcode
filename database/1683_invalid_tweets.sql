select
    t.tweet_id
from
    tweets as t
where
    (1 = 1)
    and length(t.content) > 15;