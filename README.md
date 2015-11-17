# API-Project

**DUE 11/16**

This website calculates the "efficiency" of a NYC teacher.
The "efficiency" is defined to be the rating of a teacher on http://ratemyteachers.com divided by the teacher's annual salary.
It is recommended to fill out the form with a teacher's official first and last name.
If either the first or last name is unknown, a nickname or abbreviation may be used, or the field may be left blank, but this may produce unwanted results.

###Some Notes on the Project
 - The SODA API was used to gather salary data from the NYC payroll database for fiscal year 2014, which can be found at https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-FY2014/k397-673e.
 - There was no API available for http://ratemyteachers.com, so the Python regex library was used to scrape the search results for the given teacher and high school. The data returned by the first MatchObject was the listed name of the teacher, the subject he or she teaches, his or her avergae rating, and the number of students who submitted ratings.
 - To improve accuracy of results, users are required to select from a pre-determined list of NYC high schools. This list was taken from the 2016 NYC High School Directory, which can be found at http://schools.nyc.gov/NR/rdonlyres/B0C37C45-E280-434D-9DF7-3251B7F895B0/0/2016HighSchoolDirectory_English.pdf.
 - When a teacher cannot be immediately located in the payroll database, a search is made on http://ratemyteachers.com for a teacher from the given high school with the name most similar to the one provided in the form. A new search is then performed on the payroll database with this name, and, if that fails, the salary is simply set to "N/A".
 - Leaving both the first name and last name blank in the form will return the first teacher that appears in the search results for the given high school on http://ratemyteachers.com.
 - The Google Image Search API was used to generate an image that probably contains the teacher whose data was gathered.
 - The Code Cogs LaTeX API was used to generate an image that represents the calculation for a teacher's efficiency.
 - A teacher's efficiency involved the maximum salary that can be earned by working for the NYC Department of Education, which is $100,049 according to http://schools.nyc.gov/nr/rdonlyres/eddb658c-be7f-4314-85c0-03f5a00b8a0b/0/salary.pdf.
