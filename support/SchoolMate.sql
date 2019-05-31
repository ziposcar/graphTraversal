##################################
# MySQL Databases For SchoolMate #
##################################
set @@sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DROP DATABASE IF EXISTS schoolmate;

CREATE DATABASE schoolmate;

USE schoolmate;

#
# Structure for table adminstaff :
#

DROP TABLE IF EXISTS adminstaff;

CREATE TABLE adminstaff (
  adminid int(11) NOT NULL auto_increment,
  userid int(11) NOT NULL default '0',
  fname varchar(20) NOT NULL default '',
  lname varchar(15) NOT NULL default '',
  PRIMARY KEY  (adminid),
  UNIQUE KEY UserID (userid)
);

#
# Structure for table assignments :
#

DROP TABLE IF EXISTS assignments;

CREATE TABLE assignments (
  assignmentid int(11) NOT NULL auto_increment,
  courseid int(11) NOT NULL default '0',
  semesterid int(11) NOT NULL default '0',
  termid int(11) NOT NULL default '0',
  title varchar(15) NOT NULL default '',
  totalpoints double(6,2) NOT NULL default '0.00',
  assigneddate date NOT NULL default '0000-00-00',
  duedate date NOT NULL default '0000-00-00',
  assignmentinformation text,
  PRIMARY KEY  (assignmentid)
);

#
# Structure for table courses :
#

DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
  courseid int(11) NOT NULL auto_increment,
  semesterid int(11) NOT NULL default '0',
  termid int(11) NOT NULL default '0',
  coursename varchar(20) NOT NULL default '',
  teacherid int(11) NOT NULL default '0',
  sectionnum varchar(15) NOT NULL default '0',
  roomnum varchar(15) NOT NULL default '',
  periodnum char(15) NOT NULL default '',
  q1points double(6,2) NOT NULL default '0.00',
  q2points double(6,2) NOT NULL default '0.00',
  totalpoints double(6,2) NOT NULL default '0.00',
  aperc double(6,3) NOT NULL default '0.000',
  bperc double(6,3) NOT NULL default '0.000',
  cperc double(6,3) NOT NULL default '0.000',
  dperc double(6,3) NOT NULL default '0.000',
  fperc double(6,3) NOT NULL default '0.000',
  dotw varchar(11) default NULL,
  substituteid int(11) default NULL,
  secondcourseid int(11) default NULL,
  PRIMARY KEY  (courseid)
);

INSERT INTO courses VALUES(1,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(2,2,2,'xxxxx',2,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(3,3,3,'xxxxx',3,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(4,4,4,'xxxxx',4,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(5,5,5,'xxxxx',5,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(6,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(7,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(8,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(9,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(10,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(11,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(12,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(13,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(14,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(15,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(16,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(17,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(18,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(19,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(20,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
INSERT INTO courses VALUES(21,1,1,'xxxxx',1,'1','1','1','0','0','0','0','0','0','0','0','',1,1);
#
# Structure for table grades :
#

DROP TABLE IF EXISTS grades;

CREATE TABLE grades (
  gradeid int(11) NOT NULL auto_increment,
  assignmentid int(11) NOT NULL default '0',
  courseid int(11) NOT NULL default '0',
  semesterid int(11) NOT NULL default '0',
  termid int(11) NOT NULL default '0',
  studentid int(11) NOT NULL default '0',
  points double(6,2) default '0.00',
  comment text,
  submitdate date default '0000-00-00',
  islate int(1) default '0',
  PRIMARY KEY  (gradeid)
);

#
# Structure for table parent_student_match :
#

DROP TABLE IF EXISTS parent_student_match;

CREATE TABLE parent_student_match (
  matchid int(11) NOT NULL auto_increment,
  parentid int(11) NOT NULL default '0',
  studentid int(11) NOT NULL default '0',
  PRIMARY KEY  (matchid)
);

INSERT INTO parent_student_match VALUES(8,8,8);
INSERT INTO parent_student_match VALUES(9,9,9);
INSERT INTO parent_student_match VALUES(10,10,10);
#
# Structure for table parents :
#

DROP TABLE IF EXISTS parents;

CREATE TABLE parents (
  parentid int(11) NOT NULL auto_increment,
  userid int(11) NOT NULL default '0',
  fname varchar(15) default NULL,
  lname varchar(15) default NULL,
  PRIMARY KEY  (parentid)
);
INSERT INTO parents VALUES(1,1,"ppp","ppp");
INSERT INTO parents VALUES(2,2,"ppp","ppp");
INSERT INTO parents VALUES(3,3,"ppp","ppp");
INSERT INTO parents VALUES(4,4,"ppp","ppp");
INSERT INTO parents VALUES(5,5,"ppp","ppp");
INSERT INTO parents VALUES(6,6,"ppp","ppp");
INSERT INTO parents VALUES(7,7,"ppp","ppp");
INSERT INTO parents VALUES(8,8,"ppp","ppp");
INSERT INTO parents VALUES(9,9,"ppp","ppp");
INSERT INTO parents VALUES(10,10,"ppp","ppp");
#
# Structure for table registrations :
#

DROP TABLE IF EXISTS registrations;

CREATE TABLE registrations (
  regid int(11) NOT NULL auto_increment,
  courseid int(11) NOT NULL default '0',
  studentid int(11) NOT NULL default '0',
  semesterid int(11) NOT NULL default '0',
  termid int(11) NOT NULL default '0',
  q1currpoints double(6,2) NOT NULL default '0.00',
  q2currpoints double(6,2) NOT NULL default '0.00',
  currentpoints double(6,2) NOT NULL default '0.00',
  PRIMARY KEY  (regid)
);

INSERT INTO registrations VALUES(1,1,1,1,1,'0','0','0');
INSERT INTO registrations VALUES(2,1,2,1,1,'0','0','0');
INSERT INTO registrations VALUES(3,1,3,1,1,'0','0','0');
INSERT INTO registrations VALUES(4,1,4,1,1,'0','0','0');
INSERT INTO registrations VALUES(5,1,5,1,1,'0','0','0');
INSERT INTO registrations VALUES(6,1,6,1,1,'0','0','0');
INSERT INTO registrations VALUES(7,1,7,1,1,'0','0','0');
INSERT INTO registrations VALUES(8,1,8,1,1,'0','0','0');
INSERT INTO registrations VALUES(9,1,9,1,1,'0','0','0');

#
# Structure for table schoolattendance :
#

DROP TABLE IF EXISTS schoolattendance;

CREATE TABLE schoolattendance (
  sattendid int(11) NOT NULL auto_increment,
  studentid int(11) NOT NULL default '0',
  sattenddate date NOT NULL default '0000-00-00',
  semesterid int(11) NOT NULL default '0',
  termid int(11) NOT NULL default '0',
  type enum('tardy','absent') default NULL,
  PRIMARY KEY  (sattendid)
);

INSERT INTO schoolattendance VALUES(1,1,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(2,2,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(3,3,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(4,4,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(5,5,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(6,6,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(7,7,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(8,8,'2019-05-28',1,1,'tardy');
INSERT INTO schoolattendance VALUES(9,9,'2019-05-28',1,1,'tardy');

#
# Structure for table schoolbulletins :
#

DROP TABLE IF EXISTS schoolbulletins;

CREATE TABLE schoolbulletins (
  sbulletinid int(11) NOT NULL auto_increment,
  title varchar(15) NOT NULL default '',
  message text NOT NULL,
  bulletindate date NOT NULL default '0000-00-00',
  PRIMARY KEY  (sbulletinid)
);

INSERT INTO schoolbulletins VALUES(1,'xxxxx1','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(2,'xxxxx2','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(3,'xxxxx3','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(4,'xxxxx4','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(5,'xxxxx5','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(6,'xxxxx6','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(7,'xxxxx7','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(8,'xxxxx8','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(9,'xxxxx9','ttttttt','2019-05-28');
INSERT INTO schoolbulletins VALUES(10,'xxxxx10','ttttttt','2019-05-28');

#
# Structure for table schoolinfo :
#

DROP TABLE IF EXISTS schoolinfo;

CREATE TABLE schoolinfo (
  schoolname varchar(50) NOT NULL default '',
  address varchar(50) default NULL,
  phonenumber varchar(14) default NULL,
  sitetext text,
  sitemessage text,
  currenttermid int(11) default NULL,
  numsemesters int(3) NOT NULL default '0',
  numperiods int(3) NOT NULL default '0',
  apoint double(6,3) NOT NULL default '0.000',
  bpoint double(6,3) NOT NULL default '0.000',
  cpoint double(6,3) NOT NULL default '0.000',
  dpoint double(6,3) NOT NULL default '0.000',
  fpoint double(6,3) NOT NULL default '0.000',
  PRIMARY KEY  (schoolname)
);

#
# Data for table schoolinfo;
#

INSERT INTO schoolinfo VALUES ('School Name','1,
Street','52365895','','This is the Message of the day:-
\r\n\r\nWe think our fathers fools, so wise do we grow,
no doubt our wisest sons would think us
so.',NULL,0,0,0.000,0.000,0.000,0.000,0.000);


#
# Structure for table semesters :
#

DROP TABLE IF EXISTS semesters;

CREATE TABLE semesters (
  semesterid int(11) NOT NULL auto_increment,
  termid varchar(15) NOT NULL default '',
  title varchar(15) NOT NULL default '',
  startdate date NOT NULL default '0000-00-00',
  midtermdate date NOT NULL default '0000-00-00',
  enddate date NOT NULL default '0000-00-00',
  type enum('1','2') default NULL,
  PRIMARY KEY  (semesterid)
);

INSERT INTO semesters VALUES(1,1,'sss','2019-05-28','2019-05-28','2019-05-28',1);
INSERT INTO semesters VALUES(2,2,'sss','2019-05-28','2019-05-28','2019-05-28',1);
INSERT INTO semesters VALUES(3,3,'sss','2019-05-28','2019-05-28','2019-05-28',1);
INSERT INTO semesters VALUES(4,4,'sss','2019-05-28','2019-05-28','2019-05-28',1);
INSERT INTO semesters VALUES(5,5,'sss','2019-05-28','2019-05-28','2019-05-28',2);

#
# Structure for table students :
#

DROP TABLE IF EXISTS students;

CREATE TABLE students (
  studentid int(11) NOT NULL auto_increment,
  userid int(11) NOT NULL default '0',
  fname varchar(15) NOT NULL default '',
  mi char(15) NOT NULL default '',
  lname varchar(15) NOT NULL default '',
  PRIMARY KEY  (studentid),
  UNIQUE KEY UserID (userid)
);

INSERT INTO students VALUES(1,11,'fff','m','sss');
INSERT INTO students VALUES(2,12,'fff','m','sss');
INSERT INTO students VALUES(3,13,'fff','m','sss');
INSERT INTO students VALUES(4,14,'fff','m','sss');
INSERT INTO students VALUES(5,15,'fff','m','sss');
INSERT INTO students VALUES(6,16,'fff','m','sss');
INSERT INTO students VALUES(7,17,'fff','m','sss');
INSERT INTO students VALUES(8,18,'fff','m','sss');
INSERT INTO students VALUES(9,19,'fff','m','sss');
INSERT INTO students VALUES(10,20,'fff','m','sss');

#
# Structure for table teachers :
#

DROP TABLE IF EXISTS teachers;

CREATE TABLE teachers (
  teacherid int(11) NOT NULL auto_increment,
  userid int(11) NOT NULL default '0',
  fname varchar(15) NOT NULL default '',
  lname varchar(15) NOT NULL default '',
  PRIMARY KEY  (teacherid),
  UNIQUE KEY UserID (userid)
);

INSERT INTO teachers VALUES(1,21,'ffft','lllt');
INSERT INTO teachers VALUES(2,22,'ffft','lllt');
INSERT INTO teachers VALUES(3,23,'ffft','lllt');
INSERT INTO teachers VALUES(4,24,'ffft','lllt');
INSERT INTO teachers VALUES(5,25,'ffft','lllt');
INSERT INTO teachers VALUES(6,26,'ffft','lllt');
INSERT INTO teachers VALUES(7,27,'ffft','lllt');
INSERT INTO teachers VALUES(8,28,'ffft','lllt');
INSERT INTO teachers VALUES(9,29,'ffft','lllt');
INSERT INTO teachers VALUES(10,30,'ffft','lllt');

#
# Structure for table terms :
#

DROP TABLE IF EXISTS terms;

CREATE TABLE terms (
  termid int(11) NOT NULL auto_increment,
  title varchar(15) NOT NULL default '',
  startdate date NOT NULL default '0000-00-00',
  enddate date NOT NULL default '0000-00-00',
  PRIMARY KEY  (termid)
);

INSERT INTO terms VALUES(1,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(2,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(3,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(4,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(5,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(6,'ttttt','2019-05-28','2019-05-28');
INSERT INTO terms VALUES(7,'ttttt','2019-05-28','2019-05-28');

#
# Structure for table users :
#

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  userid int(11) NOT NULL auto_increment,
  username varchar(15) NOT NULL default '',
  password varchar(32) NOT NULL default '',
  type enum('Admin','Teacher','Substitute','Student','Parent') NOT NULL default 'Admin',
  PRIMARY KEY  (userid),
  UNIQUE KEY username (username)
);

#
# Data for table users  (LIMIT 0,500)
#

INSERT INTO users (userid, username, password, type) VALUES (1,'test1','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (2,'test2','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (3,'test3','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (4,'test4','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (5,'test5','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (6,'test6','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (7,'test7','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (8,'test8','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (9,'test9','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (10,'test10','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (11,'test11','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (12,'test12','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (13,'test13','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (14,'test14','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (15,'test15','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (16,'test16','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (17,'test17','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (18,'test18','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (19,'test19','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (20,'test20','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (21,'test21','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (22,'test22','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (23,'test23','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (24,'test24','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (25,'test25','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (26,'test26','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (27,'test27','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (28,'test28','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (29,'test29','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (30,'test30','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (31,'test31','098f6bcd4621d373cade4e832627b4f6','Substitute');
INSERT INTO users (userid, username, password, type) VALUES (32,'test32','098f6bcd4621d373cade4e832627b4f6','Substitute');
INSERT INTO users (userid, username, password, type) VALUES (33,'test33','098f6bcd4621d373cade4e832627b4f6','Substitute');
INSERT INTO users (userid, username, password, type) VALUES (34,'test34','098f6bcd4621d373cade4e832627b4f6','Substitute');
INSERT INTO users (userid, username, password, type) VALUES (35,'test35','098f6bcd4621d373cade4e832627b4f6','Substitute');
INSERT INTO users (userid, username, password, type) VALUES (36,'test36','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (37,'test37','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (38,'test38','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (39,'test39','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (40,'test40','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (41,'test41','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (42,'test42','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (43,'test43','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (44,'test44','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (45,'test45','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (46,'test46','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (47,'test47','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (48,'test48','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (49,'test49','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (50,'test50','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (51,'test51','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (52,'test52','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (53,'test53','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (54,'test54','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (55,'test55','098f6bcd4621d373cade4e832627b4f6','Student');
INSERT INTO users (userid, username, password, type) VALUES (56,'test56','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (57,'test57','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (58,'test58','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (59,'test59','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (60,'test60','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (61,'test61','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (62,'test62','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (63,'test63','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (64,'test64','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (65,'test65','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (66,'test66','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (67,'test67','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (68,'test68','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (69,'test69','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (70,'test70','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (71,'test71','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (72,'test72','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (73,'test73','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (74,'test74','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (75,'test75','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (76,'test76','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (77,'test77','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (78,'test78','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (79,'test79','098f6bcd4621d373cade4e832627b4f6','Teacher');
INSERT INTO users (userid, username, password, type) VALUES (80,'test','098f6bcd4621d373cade4e832627b4f6','Admin');
INSERT INTO users (userid, username, password, type) VALUES (81,'test81','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (82,'test82','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (83,'test83','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (84,'test84','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (85,'test85','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (86,'test86','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (87,'test87','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (88,'test88','098f6bcd4621d373cade4e832627b4f6','Parent');
INSERT INTO users (userid, username, password, type) VALUES (89,'test89','098f6bcd4621d373cade4e832627b4f6','Parent');

COMMIT;

