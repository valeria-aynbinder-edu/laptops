--total sales in dates range: total items, total sum in euro, amount of unique customers
-- total income and unique customers
select sum(total_price) as total_price, count(distinct customer_id) as unique_customers from orders;
-- total items sold
select sum(amnt) as total_items  from order_items ;


-- top X best selling laptops
select best_sellers.items_sold, l.*  from laptops l join
(select laptop_id, sum(amnt) as items_sold from order_items oi group by laptop_id order by items_sold desc) as best_sellers
on l.id=best_sellers.laptop_id ;

select laptop_id, sum(amnt) from order_items oi group by laptop_id ;


-- X best customers (those spent most money in our store), in specific dates range
select o.customer_id, c.name, sum(o.total_price) as aggregated_total from orders o join customers c on o.customer_id = c.id
where o.total_price is not null and o.order_date between  date '2020-01-01' and date '2022-02-28'
group by o.customer_id, c.name
order by aggregated_total desc;



-- X laptops that suffered most price decline since specific date, relatively to current price
select o.order_date , o.id, l.id, oi.item_price_euro ,
l.price_euro, oi.item_price_euro -l.price_euro  as price_diff
from orders o join order_items oi on o.id =oi.order_id join laptops l on oi.laptop_id = l.id
where  o.order_date > date '2020-01-01' and oi.item_price_euro -l.price_euro<0
order by price_diff asc;


-- most profitable manufacturers (table of manufacturer name, total items sold, total sum sold)
select m.id, sum(oi.amnt) as total_items_sold, sum(oi.amnt * oi.item_price_euro)
from order_items oi
join laptops l on oi.laptop_id =l.id
join manufacturers m on l.manufacturer_id =m.id
group by m.id;