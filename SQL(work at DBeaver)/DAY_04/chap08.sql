use sakila;

select customer_id, count(*)
from rental
group by customer_id;

select customer_id, count(*)
from rental
group by customer_id
order by 2 desc;    # or oder by count(*) desc;

# where절에 필터링을 적용할수없음
# -그룹화한 결과에는 having절을 사용함
select customer_id, count(*)
from rental
group by customer_id
having count(*) >= 40;

select max(amount) as max_amt,min(amount) as min_amt,avg(amount) as avg_amt,sum(amount) as tot_amt,count(*) as num_payments
from payment;

select customer_id,max(amount) as max_amt,min(amount) as min_amt,avg(amount) as avg_amt,sum(amount) as tot_amt,count(*) as num_payments
from payment 
GROUP by customer_id;

select count(customer_id) as num_rows,count(distinct customer_id) as num_customers
from payment;                            # 중복제거(distinct키워드)

select max(datediff(return_date, rental_date))
from rental;

select avg(datediff(return_date, rental_date)) 
from rental;

use sqlclass_db;
drop table if exists number_tbl;
create table number_tbl(val smallint);
desc number_tbl;

INSERT into number_tbl VALUES(1);
INSERT into number_tbl VALUES(3);
INSERT into number_tbl VALUES(5);

select count(*) as num_rows,count(val) as num_vals,sum(val) as total,max(val) as max_val,avg(val) as avg_val
from number_tbl;

INSERT into number_tbl values(NULL);
select * from number_tbl;
# 함수들이 null값을 만나면 무시

use sakila;

select actor_id, count(*)
from film_actor
group by actor_id;

select fa.actor_id, f.rating, count(*)
from film_actor as fa
	inner join film as f
	on fa.film_id= f.film_id
group by fa.actor_id, f.rating
order by 1, 2;

select fa.actor_id, f.rating, count(*)
from film_actor as fa
	inner join film as f
	on fa.film_id= f.film_id
group by fa.actor_id, f.rating with rollup
order by 1, 2;

select fa.actor_id, f.rating, count(*)
from film_actor fa
	inner join film f
	on fa.film_id= f.film_id
where f.rating IN('G','PG')
group by fa.actor_id, f.rating
having count(*) > 9;

select customer_id, count(*), sum(amount)
from payment
group by customer_id;