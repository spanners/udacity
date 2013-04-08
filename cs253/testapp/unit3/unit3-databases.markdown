#What is a database?
##A program that stores and retrieves large amounts of structured data

(User) ----> (Internet) ----> (Servers) >--query--> <--response-< (Database)

#Tables
##columns and rows

##Link table

ID | votes | user | date | title | url                
--- | --- | --- | --- | --- | ---
5 | 207 | 21 | 1359 | Zombie Dogs! | www.zombiedogs.com 
6  | 0 | 22 | 1762 | Lazors! | www.lazors.com

##User table

ID | name | date | password                
--- | --- | --- | ---
21 | spez | ... | ...

#SQL -- Structured Query Language
##A language for expressing questions to a relational DB to get data out of it. Invented in 1970.

##Example -- A Basic Request:

		SELECT * FROM links WHERE id = 5;

###Key:
#### fetch data | all columns | table | constraint

### You can actually select from multiple tables, but this one selects from only one table, links.

##Example -- Ordering query results:

		SELECT * FROM links WHERE votes > 10 ORDER BY votes

### default order is ususally ascending, but you can add DESC at the end for descending

##Example:

		select id from links where submitter_id = 62443 order by submitted_time asc

### You can select only the id from the query to get the id's in the table that match these constraints

#Joins
## Not used much in web stuff. *Why??*
##Example -- Using the join character , :

		SELECT link.* FROM link,user WHERE link.user_id = user.id AND user.name = 'spez'


