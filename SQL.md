1. get all statuses, not repeating, alphabetically ordered. |
SELECT DISTINCT status 
FROM tasks 
ORDER BY status

2. get the count of all tasks in each project, order by tasks count descending. |
SELECT project_id, COUNT(*) AS task_count 
FROM tasks 
GROUP BY project_id 
ORDER BY task_count DESC

3. get the count of all tasks in each project, order by projects names. |
SELECT p.name AS project_name, COUNT(*) AS task_count 
FROM tasks AS t 
JOIN projects AS p ON t.project_id = p.id 
GROUP BY p.name 
ORDER BY p.name ASC

4. get the tasks for all projects having the name beginning with "N" letter. |
SELECT *
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%'

5. get the list of all projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id= NULL. | 
SELECT p.name AS project_name, COUNT(t.id) AS task_count
FROM projects AS p
LEFT JOIN tasks AS t ON t.project_id = p.id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name

6. get the list of tasks with duplicate names. Order alphabetically. | 
SELECT name, COUNT(*) AS dup_count
FROM tasks
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name

7. get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count. | 
SELECT name, status, COUNT(*) AS dup_count
FROM tasks AS t
JOIN projects AS p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY dup_count DESC

8. get the list of project names having more than 10 tasks in status 'completed'. Order by project_id. | 
SELECT p.name, COUNT(*) as task_count
FROM tasks as t
JOIN projects AS p ON t.project_id = p.id 
WHERE t.status = 'completed'
GROUP BY p.name, p.id
HAVING COUNT(*) > 10
ORDER BY p.id
