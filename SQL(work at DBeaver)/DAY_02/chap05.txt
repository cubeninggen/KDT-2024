use sakila;

select c.first_name, c.last_name, a.address
from customer as c cross join address as a;

select count(*) from customer;
select count(*) from address;
select count(*) from customer as c join address as a;

select c.first_name, c.last_name, a.address, a.district 
from customer as c inner join address as a 
on c.address_id= a.address_id;

select count(*)from customer as c inner join address as a 
on c.address_id= a.address_id;

select c.first_name, c.last_name, ct.city, a.address, a.district, a.postal_code
from customer as c 
	inner join address as a on c.address_id= a.address_id
	inner join city as ct on a.city_id= ct.city_id;

select c.first_name, c.last_name, addr.address, addr.city, addr.district
from customer as c
	inner join
	(select a.address_id, a.address, ct.city, a.district
	from address as a 
		inner join city as ct 
		on a.city_id= ct.city_id
	where a.district= 'California') as addr
on c.address_id= addr.address_id;

select f.title
from film as f
	inner join film_actor as fa 
	on f.film_id= fa.film_id
	inner join actor a 
	on fa.actor_id= a.actor_id
where((a.first_name= 'CATE'and a.last_name= 'MCQUEEN')or(a.first_name= 'CUBA'and a.last_name= 'BIRCH'));

# 두명의배우가같이출연한영화검색
# CATE MCQUEEN만검색
select f.title, f.film_id, a1.first_name, a1.last_name
from film as f
	inner join film_actor as fa1
	on f.film_id= fa1.film_id
	inner join actor a1 
	on fa1.actor_id = a1.actor_id
where(a1.first_name = 'CATE'and a1.last_name = 'MCQUEEN');

# CUBA BIRCH만검색
select f.title, f.film_id, a2.first_name, a2.last_name
from film as f 
	inner join film_actor as fa2 
	on f.film_id= fa2.film_id
	inner join actor a2 
	on fa2.actor_id = a2.actor_id
where(a2.first_name = 'CUBA'and a2.last_name = 'BIRCH');

select f.title
from film as f 
	inner join film_actor as fa1 
	on f.film_id= fa1.film_id
	inner join actor a1 # film, film_actor, actor 내부조인#1
	on fa1.actor_id = a1.actor_id 
	inner join film_actor as fa2 
	on f.film_id= fa2.film_id 
	inner join actor a2 #film, film_actor, actor 내부조인#2
	on fa2.actor_id = a2.actor_id
where(a1.first_name = 'CATE'and a1.last_name = 'MCQUEEN') and(a2.first_name = 'CUBA'and a2.last_name = 'BIRCH');

use sqlclass_db;
DROP TABLE IF EXISTS customer;
create table customer
	(customer_id smallint unsigned,
	first_name varchar(20),
	last_name varchar(20),
	birth_date date,
	spouse_id smallint unsigned,
	constraint primary key(customer_id));

desc customer;

insert into customer (customer_id, first_name, last_name, birth_date, spouse_id)
values
(1, 'John', 'Mayer', '1983-05-12', 2),
(2, 'Mary', 'Mayer', '1990-07-30', 1),
(3, 'Lisa', 'Ross', '1989-04-15', 5),
(4, 'Anna', 'Timothy', '1988-12-26', 6),
(5, 'Tim', 'Ross', '1957-08-15', 3),
(6, 'Steve', 'Donell', '1967-07-09', 4);

insert into customer (customer_id, first_name, last_name, birth_date)
values(7, 'Donna', 'Trapp', '1978-06-23');

select* from customer;

select
	cust.customer_id,
	cust.first_name,
	cust.last_name,
	cust.birth_date,
	cust.spouse_id,
	spouse.first_name as spouse_firstname,
	spouse.last_name as spouse_lastname
from customer as cust
	join customer as spouse
	on cust.spouse_id= spouse.customer_id;