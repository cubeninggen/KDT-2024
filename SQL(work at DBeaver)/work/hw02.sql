use sqlclass_db;

select year, category, fullname
from nobel 
where year=1960;

select year, category, prize_amount, birth_continent, birth_country
from nobel
where fullname='Albert Einstein';

select year, fullname, birth_country
from nobel
where year between 1910 and 2010;

select category, fullname
from nobel
where fullname like 'John%';

select * from nobel
where year=1964 and category !='Physiology or Medicine';

select year, fullname, gender, birth_country
from nobel 
where category='Literature' and year between 2000 and 2019;

select category from nobel
group by category 
order by count(category) desc;

select distinct year
from nobel
where category = 'Physiology or Medicine';

select count(distinct year)
from nobel
where category!='Physiology or Medicine';

select fullname, category, birth_country
from nobel
where gender='female';

select birth_country, count(birth_country)
from nobel
group by birth_country;

select * from nobel
where birth_country='Korea';

select * from nobel
where birth_country not in ('Europe','North America',' ');

select birth_country, count(*) from nobel
group by birth_country 
having count(*) >= 10
order by count(*) desc;

select fullname,count(*) from nobel
where fullname!=''
group by fullname
having count(*)>=2
order by fullname;