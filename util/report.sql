SELECT o.last_execution_time,
       p.side                       AS parent_side,
       p.total_size                 AS size,
       p.price                      AS start_price,
       o.side,
       o.order_type,
       CASE
           WHEN o.price IS NULL THEN o.stop_price
           WHEN o.stop_price IS NULL THEN o.price
           END                      AS end_price,
       ROUND(
               CASE
                   WHEN p.side = 'BUY' AND o.side = 'SELL' AND o.order_type = 'STOP' THEN (o.stop_price - p.price) * p.total_size
                   WHEN p.side = 'SELL' AND o.side = 'BUY' AND o.order_type = 'STOP' THEN (p.price - o.stop_price) * p.total_size
                   WHEN p.side = 'BUY' AND o.side = 'SELL' AND o.order_type = 'LIMIT' THEN (o.price - p.price) * p.total_size
                   WHEN p.side = 'SELL' AND o.side = 'BUY' AND o.order_type = 'LIMIT' THEN (p.price - o.price) * p.total_size
                   ELSE 0
                   END::NUMERIC, 5) AS profit_and_lost
FROM core_order o
         JOIN public.core_order p ON o.parent_id = p.order_id
WHERE o.status = 'Filled';