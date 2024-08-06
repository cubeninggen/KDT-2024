drop database testdb;
CREATE DATABASE testdb;
USE testdb;

# person 테이블이 있으면 삭제 
DROP TABLE IF EXISTS person;

# person 테이블 생성 
# CONSTRAINT  pk_person: 제약 조건의 이름 설정 
CREATE TABLE person
      (person_id SMALLINT UNSIGNED,
       fname VARCHAR(20),
       lname VARCHAR(20),
       eye_color ENUM('BR','BL','GR'),
       birth_date DATE,
       street VARCHAR(30),
       city VARCHAR(20),
       state VARCHAR(20),
       country VARCHAR(20),
       postal_code VARCHAR(20),
       CONSTRAINT pk_person PRIMARY KEY (person_id)
      );
      
# person 테이블 구성 확인 
desc person;    

DROP TABLE IF EXISTS favorite_food;
# favorite_food 테이블 생성  
CREATE TABLE favorite_food 
	(person_id SMALLINT UNSIGNED,
	food VARCHAR(20),
	CONSTRAINT pk_favorite_food PRIMARY KEY (person_id, food),
	CONSTRAINT fk_fav_food_person_id FOREIGN KEY (person_id) REFERENCES person(person_id)
	);
	
# favorite_food 테이블 구성 확인 
desc favorite_food;  

set foreign_key_checks=0;
ALTER table person modify person_id smallint unsigned auto_increment;
set foreign_key_checks=1;

INSERT into person(person_id, fname, lname, eye_color, birth_date) VALUES(null, 'William', 'Turner', 'BR', '1972-05-27');

select * from person;

select person_id, fname, lname, birth_date from person;
select person_id, fname, lname, birth_date from person where lname= 'Turner';

insert into favorite_food(person_id, food)
VALUES(1, 'pizza');
insert into favorite_food(person_id, food)
VALUES(1, 'cookies');
insert into favorite_food(person_id, food)
VALUES(1, 'nachos');

delete from favorite_food where person_id=1;

insert into favorite_food(person_id, food)
VALUES(1, 'pizz'),
(1, 'cookie'),
(1, 'nachos');

select * from favorite_food

select food from favorite_food where person_id=1 order by food;      #오름차순
select food from favorite_food where person_id=1 order by food desc; #내림차순

insert into person(person_id, fname, lname, eye_color, birth_date, street, city, state, country, postal_code)
VALUES(null, 'Susan', 'Smith', 'BL', '1975-11-02','23 Maple St.', 'Arlington', 'VA', 'USA', '20220');

select person_id, fname, lname, birth_date from person;

update person set street= '1225 Tremon St.',city= 'Boston',state= 'MA',country= 'USA',postal_code= '02138'
where person_id=1;

select * from person;

delete from person where person_id=2;
select * from person;