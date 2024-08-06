select 1 as num, 'abc' as str
union 
select 9 as num, 'xyz' as str;

use sakila;

SELECT'CUST'as type1, c.first_name, c.last_name
from customer c 
union all
SELECT'ACTR'as type1, a.first_name, a.last_name
from actor a;

select count(first_name) from customer;

select count(first_name) from actor;

SELECT'ACTR1'as type, a.first_name, a.last_name
from actor a 
union all 
SELECT'ACTR2'as type, a.first_name, a.last_name
from actor a;

select 'cust' as type1, c.first_name, c.last_name
from customer c
where c.first_name LIKE'J%'and c.last_name LIKE'D%'
union all 
select 'act' as type1, a.first_name, a.last_name
from actor a 
where a.first_name LIKE'J%'and a.last_name LIKE'D%';

select c.first_name, c.last_name
from customer c 
where c.first_name LIKE'J%'and c.last_name LIKE'D%'
union
select a.first_name, a.last_name
from actor a 
where a.first_name LIKE'J%'and a.last_name LIKE'D%';

select c.first_name, c.last_name
from customer c 
where c.first_name LIKE'D%'and c.last_name LIKE'T%';

select a.first_name, a.last_name 
from actor a
where a.first_name LIKE'D%'and a.last_name LIKE'T%';

select c.first_name, c.last_name 
from customer c
where c.first_name LIKE'D%'and c.last_name LIKE'T%'
intersect
select a.first_name, a.last_name
from actor a
where a.first_name LIKE'D%'and a.last_name LIKE'T%';

select c.first_name, c.last_name 
from customer c
where c.first_name LIKE'J%'and c.last_name LIKE'D%'
intersect
select a.first_name, a.last_name
from actor a
where a.first_name LIKE'J%'and a.last_name LIKE'D%';

select c.first_name, c.last_name
from customer as c 
inner join actor as a
ON(c.first_name= a.first_name) and(c.last_name= a.last_name);

select c.first_name, c.last_name
from customer as c 
	inner join actor as a 
	ON(c.first_name= a.first_name) and(c.last_name= a.last_name)
where a.first_name LIKE'J%'and a.last_name LIKE'D%';

select a.first_name, a.last_name
from actor a 
where a.first_name LIKE'J%'and a.last_name LIKE'D%'
except
select c.first_name, c.last_name
from customer c
where c.first_name LIKE'J%'and c.last_name LIKE'D%';

select a.first_name, a.last_name
from actor a
where a.first_name LIKE'J%'and a.last_name LIKE'D%'
union all 
select a.first_name, a.last_name
from actor a
where a.first_name LIKE'M%'and a.last_name LIKE'T%'
union
select c.first_name, c.last_name
from customer c 
where c.first_name LIKE'J%'and c.last_name LIKE'D%';

select first_name, last_name
from actor
where last_name like'L%'
union
select first_name, last_name
from customer
where last_name like'L%';

select first_name, last_name
from actor
where last_name LIKE'L%'
union 
select first_name, last_name
from customer 
where last_name LIKE'L%'
order by last_name;