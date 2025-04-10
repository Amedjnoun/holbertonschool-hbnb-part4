#!/bin/bash

echo "Creating table and inserting data"
sqlite3 instance/development.db < sql/create_tables.sql
sqlite3 instance/development.db < sql/insert_initial_data.sql

echo "Launch the app"
python run.py
