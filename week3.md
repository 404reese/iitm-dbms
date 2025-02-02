## Question 1
Write an SQL statement to find the match number of the match held on ‘2020-05-11’
and the name of the main referee who refereed that match.
Print match num first followed by respective main referee name.</br>
Note: main referee is to be obtained from the ‘referee’ attribute.</br>
Database: FLIS

### Solution:
```
select match_num,name from referees
inner join match_referees on referees.referee_id=match_referees.referee
inner join matches using(match_num)
where match_date=’2020-05-11’;
```

## Question 2
Write an SQL statement to find the name of the youngest player in the team named
“All Stars”.</br>
Database: FLIS

### Solution:
```
SELECT name
FROM players
WHERE team_id IN (SELECT team_id FROM teams WHERE name = 'All Stars')
ORDER BY dob ASC
LIMIT 1
```
## Question 3
Write an SQL statement to find the names of teams that do not have any player with
jersey number (jersey no) 74.</br>
Database: FLIS

### Solution:
```
select name
from teams where team_id in
  ((select team_id from teams)
  except
  (select distinct team_id
  from players
  where jersey_no = 74));
```
## Question 4
Write an SQL statement to find student fname and student lname of all students who
have issued at least one book.</br>
Database: LIS

### Solution:
```
select student_fname, student_lname
from students
where roll_no in
  (select roll_no
  from members a, book_issue b
  where a.member_no=b.member_no
);
```
## Question 5
Write an SQL statement to find the book titles and the number of copies of the books
which has the word “Database” in their title.</br>
Database: LIS

### Solution:
```
select title, count(*)
from book_catalogue b1 join book_copies b2
on b1.isbn_no = b2.isbn_no
where title like ’%Database%’ group by title;
```