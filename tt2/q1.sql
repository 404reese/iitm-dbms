-- Retrieve the names of all students in the CSE department.
select name 
from students
where department = 'CSE';

-- Find the course names and credits for all courses offered by the ECE department
select course_name, credits
from courses
where department = 'ECE';

-- Get the student IDs and names of students who have scored an A grade in any course
select 

-- Q4: List the course IDs and names of courses that have more than 3 credits.
select course_id, course_name
from courses
where credits > 3;

-- Q5: Find the average grade of students in the MECH department.
-- (Assume grade points: A=10, B=8, C=6, D=4, F=0)
select AVG(g.grade) as avg_grade
from students s
join grades G on s.student_id = 

-- Q6: Retrieve the student IDs and names of students who have not scored any grade.

-- Q7: Find the course IDs and names of courses that have been taken by more than 5 students.
select c.course_id, c.course_name
from courses c 
join grades G on c.course_id = G.course_id
group by c.course_id, c.course_name
having count(distinct g.student_id) > 5;

-- Q8: Get the department-wise count of students.
SELECT department, COUNT(*) AS student_count
FROM Students
GROUP BY department;

-- Q9: List the student IDs and names of students who have scored an A grade in a course offered by the CSE department.

-- Q10: Find the course IDs and names of courses that have the highest credits.
