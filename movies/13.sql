SELECT name FROM people WHERE name NOT LIKE 'Kavin Bacon'AND birth NOT LIKE '1958' AND id IN
(SELECT person_id FROM stars WHERE movie_id In
(SELECT id FROM movies WHERE id IN
(SELECT movie_id FROM stars WHERE person_id IN
(SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958))));
