create database uefa_project;
use uefa_project;
Drop database uefa_project;
create table UEFA(U_name varchar(15) primary key,date_since date,Website varchar(35));

insert into UEFA value('UEFA','1993.10.20','www.uefa.com');

create table Champoionships(C_num int primary key,C_name varchar (200) ,C_type varchar(50), sponsr varchar (60),
 season int, status varchar(25),U_name varchar(15),
foreign key(U_name)references UEFA(U_name)on delete cascade on update cascade);

insert into Champoionships value
(1,'laliga','local','spotyfay',2025,'active','UEFA'),
(2,'premier league','local','flydubai',2025,'active','UEFA'),
(3,'Serie A','local','Niky',2022,'inactive','UEFA'),
(4,' Ligue1','local','Adidas',2020,'inactive','UEFA'),
(5,'Bundesliga','local','boma',2023,'inactive','UEFA');

create table Team(T_name varchar(20) primary key,trophies varchar(35),C_num int,
foreign key(C_num)references Champoionships(C_num)on delete cascade on update cascade);

INSERT INTO Team values
('Real madrid', '102 trophies',1),
('Barcelona', '105 trophies',1),
('Liverpol', '80 trophies',2),
('Manchester City', '60 trophies',2),
('joventus', '40 trophies',3),
('Napoly', '30 trophies',3),
('Paris', '15 trophies',4),
('lil', '33 trophies',4),
('Bayern', '88 trophies',5),
('BVB', '35 trophies',5);
    #-------------------

    #-------------------

create table Matches(M_id int primary key,M_date date,score varchar(30),VS varchar (100),C_num int,
foreign key(C_num)references Champoionships(C_num)on delete cascade on update cascade);
insert into Matches value
(101,'2025.12.6','5-1','Barcelona-Real madrid',1),
(102,'2025.6.10','3-1','Liverpol-Manchester City',2),
(103,'2025.7.5','1-1','joventus-Napoly',3),
(104,'2025.8.10','2-1','Paris-lil',4),
(105,'2025.9.14','6-1','Bayern-BVB',5);
    #-------------------

create table Stadium(S_name char(50) primary key,Attendance int,Capasity int,M_id int,
foreign key(M_id)references Matches(M_id)on delete cascade on update cascade);

insert into Stadium value
('Campnou',80000,105000,101),
('anfield',60000,80000,102),
('Alianz',44000,67000,103),
('Pierre',51000,50000,104),
('Signal_Park',57000,49000,105);
    #-------------------

CREATE TABLE Matches_of_Teams (M_id INT,T_name varchar(20),M_date DATE,
    FOREIGN KEY (M_id) REFERENCES Matches(M_id),
    FOREIGN KEY (T_name) REFERENCES Team(T_name),
    PRIMARY KEY (M_id, T_name));
    
insert into Matches_of_Teams value
(101,'Barcelona','2025.12.6'),
(102,'Manchester City','2025.6.10'),
(103,'joventus','2025.7.5'),
(104,'Paris','2025.8.10'),
(105,'BVB','2025.9.14');

	#-------------------
create table Person(P_id int not null auto_increment primary key,P_name varchar (80)not null,P_nation varchar(25) not null, U_name varchar(15),T_name varchar(20),
foreign key(U_name)references UEFA(U_name)on delete cascade on update cascade,
foreign key(T_name)references Team(T_name)on delete cascade on update cascade);

 insert into Person value
(10,'Anriki','Spain','UEFA','Paris'),
(11,'Gatozo','Italyan','UEFA','Napoly'),
(12,'Flik','Germany','UEFA','Barcelona'),
(14,'Gerard Martín','Spain','UEFA','Barcelona'),
(15,'Marcus Rashford','Ingeland','UEFA','Barcelona'),
(16,'Raphinha','Brazil','UEFA','Barcelona'),
(17,'Koundé','France','UEFA','Barcelona'),
(18,'Olmo','Spain','UEFA','Barcelona'),
(19,'Courtois','Blgeka','UEFA','Real madrid'),
(20,'Bellingham','Ingeland','UEFA','Real madrid'),
(28,'alonso','Spain','UEFA','Real madrid'),
(21,'Mbappé','France','UEFA','Real madrid'),
(22,'Vinícius Júnior','Brazil','UEFA','Real madrid'),
(23,'Carvajal','Spain','UEFA','Real madrid'),
(24,'Alisson','Brazil','UEFA','Liverpol'),
(25,'Salah','Egypt','UEFA','Liverpol'),
(26,'Núñez','Uruguay','UEFA','Liverpol'),
(27,'Robertson','Scotland','UEFA','Liverpol'),
(29,'Neuer','Germany','UEFA','Bayern'),
(30,'Kimmich','Germany','UEFA','Bayern'),
(31,'Müller','Germany','UEFA','Bayern'),
(32,'Company','Germany','UEFA','Bayern'),
(33,'Hummels','Germany','UEFA','BVB'),
(34,'Kobel','Switzerland','UEFA','BVB'),
(35,'Brandt','Germany','UEFA','BVB'),
(36,'jon','Germany','UEFA','BVB'),
(37,'Donnarumma','Italyan','UEFA','Paris'),
(38,'Marquinhos','Brazil','UEFA','Paris'),
(39,'Kimpembe','France','UEFA','Paris'),
(40,'André','France','UEFA','LIL'),
(41,'David','Knada','UEFA','LIL'),
(42,'Chevalier','France','UEFA','LIL'),
(43,'de Ligt','Holland','UEFA','joventus'),
(44,'Rabiot','France','UEFA','joventus'),
(45,'Kean','Italyan','UEFA','joventus'),
(46,'Del Piero','Italyan','UEFA','joventus'),
(47,'Zieliński','poland','UEFA','Napoly'),
(48,'Lorenzo','Italyan','UEFA','Napoly'),
(49,'Osimhen','Nigeria','UEFA','Napoly'),
(50,'Haaland','Norway','UEFA','Manchester City'),
(51,'Dias','Bortogal','UEFA','Manchester City'),
(52,'Grealish','France','UEFA','Manchester City');

DESCRIBE Person;


    #-------------------

CREATE TABLE Players(
    P_id INT PRIMARY KEY, P_num int, Position varchar(20),
    FOREIGN KEY (P_id) REFERENCES Person(P_id)on delete cascade on update cascade);
    
insert into Players value
(14,18,'LB'),
(15,14,'RW'),
(16,11,'LW'),
(17,23,'RB'),
(18,20,'CAM'),
(19,1,'GK'),
(20,5,'CAM'),
(21,10,'ST'),
(22,7,'LW'),
(23,2,'RB'),
(24,1,'GK'),
(25,11,'RW'),
(26,7,'ST'),
(27,26,'LB'),
(29,1,'GK'),
(30,6,'CDM'),
(31,25,'CAM'),
(33,15,'CB'),
(34,1,'GK'),
(35,19,'CAM'),
(37,99,'GK'),
(38,5,'CB'),
(39,3,'CB'),
(40,4,'CM'),
(41,7,'CAM'),
(42,16,'GK'),
(43,4,'CB'),
(44,25,'CM'),
(45,18,'ST'),
(47,20,'CM'),
(48,22,'RB'),
(49,9,'ST'),
(50,9,'ST'),
(51,3,'CB'),
(52,10,'LW');


CREATE TABLE Staff(
P_id INT PRIMARY KEY, Salary int, job varchar(20),
FOREIGN KEY (P_id) REFERENCES Person(P_id)on delete cascade on update cascade);

insert into Staff value
(10,1200000,'Coach'),
(11,4000000,'Coach'),
(12,8500000,'Coach'),
(28,1100000,'Coach'),
(36,1375000,'Coach');

DROP TABLE IF EXISTS Person_log;

CREATE TABLE Person_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    P_id INT NOT NULL,
    action VARCHAR(100),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DELIMITER $$

CREATE TRIGGER after_Person_insert
AFTER INSERT ON Person
FOR EACH ROW
BEGIN
    INSERT INTO Person_log (P_id, action)
    VALUES (NEW.P_id, 'Person Added');
END$$

DELIMITER ;


INSERT INTO Person (P_name, P_nation, T_name)
VALUES ('Hassan', 'Saudi', 'Liverpol');

SELECT * FROM Person_log;


DROP TABLE IF EXISTS Person_log;
DROP TRIGGER IF EXISTS after_Person_insert;

	#-------------------

show tables;
select * from Team;
select * from Players;
select * from Staff;
select * from Matches;
select * from UEFA;
select * from Person;
select * from Champoionships;
select * from Matches_of_Teams;
SELECT * FROM Users;


update Champoionships set c_num = (1) where C_num = (6);
update staff set Team = ('Real madrid') where employee_id =15;

Select AVG (salary) AS "Avg Salary"
from staff where salary > 5000000;

update Person set P_id = ('13') where P_id =28;

select * from Players where Position like ('C_%');
select * from Players where Position like ('L_%');
select * from Players where Position like ('G_%');

SELECT * FROM person
WHERE P_name LIKE 'A%';

SELECT * FROM person
WHERE P_name LIKE 'C%';
