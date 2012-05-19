palabra-meta
============

palabra-meta is a command-line program for querying crossword metadata
using MongoDB.

Requirements:

* MongoDB 2.0.5
* PyMongo 2.2

Commands
========

You can pass main.py the following commands:

* **initialimport [integer]**: This resets the database and creates the given number of crosswords.
* **checkcount**: Computes the total number of checked cells in all crosswords in the database.
A cell is called 'checked' iff it is used in both an Across and Down entry.