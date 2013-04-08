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
##A language for expressing questions to a relational DB to get data out of it.
###Invented in 1970.

##Example -- SQL for A Basic Request:

		SELECT * FROM links WHERE id = 5;

###Key:
####fetch data | all columns | table | constraint

###You can actually select from multiple tables, but this one selects from only one table, links.

##Example -- SQL for Ordering query results:

		SELECT * FROM links WHERE votes > 10 ORDER BY votes;

###default order is ususally ascending, but you can add DESC at the end for descending

##Example -- SQL to Sort by DESCending order:

		SELECT id FROM links WHERE submitter_id = 62443 ORDER BY submitted_time DESC;

### You can select only the id from the query to get the id's in the table that match these constraints

#Joins
## Not used much in web stuff. *Why??*
##Example -- SQL for Using the join character , :

		SELECT link.* FROM link,user WHERE link.user_id = user.id AND user.name = 'spez';

#Indexes
##Increase the speed of database queries
###This is because they allow you to directly access the element(s) you need without having to iterate over the results.
###The results from a non-indexed query may be millions of rows which would be time-expensive to iterate over!
##Decrease the speed of database inserts (very probably)
###This is because you have to update your index (probably)

##Example -- SQL for Creating an index:

		CREATE INDEX hotel_id ON hotels(id);