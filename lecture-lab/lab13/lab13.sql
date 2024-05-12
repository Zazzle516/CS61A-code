.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = "blue" AND pet = "dog";


CREATE TABLE bluedog_songs AS
  SELECT color, pet,song FROM students WHERE color = "blue" AND pet = "dog";


CREATE TABLE matchmaker AS
  SELECT
  stu_A.pet, stu_A.song, stu_A.color, stu_B.color 
  FROM
  students stu_A INNER JOIN students stu_B 
  WHERE stu_A.pet = stu_B.pet AND stu_A.song = stu_B.song AND stu_A.time < stu_B.time
  ORDER BY stu_A.time;


CREATE TABLE sevens AS
  SELECT 
  students.seven
  FROM students INNER JOIN numbers
  WHERE students.number = 7 AND numbers.'7' = 'True' AND students.time = numbers.time;


CREATE TABLE favpets AS
  SELECT pet, COUNT(*) AS count FROM students GROUP BY pet ORDER BY count DESC LIMIT 10;


CREATE TABLE dog AS
  SELECT pet, COUNT(*) AS count FROM students WHERE students.pet = 'dog' GROUP BY pet;


CREATE TABLE bluedog_agg AS
  SELECT song, COUNT(*) AS count FROM bluedog_songs GROUP BY song ORDER BY count DESC;


CREATE TABLE instructor_obedience AS
  SELECT seven, instructor, COUNT(*) AS cuont FROM students WHERE students.seven = '7' GROUP BY instructor;

