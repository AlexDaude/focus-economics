# Description

# Python version

pyhton 3.13.5


# Run

## 1) Clone github repository
## 2) From a terminal go to focus-economics directory
## 2) make sure docker engine is up and running in your pc
## 3) run in your terminal -> docker compose up 


# To check the results in the database


## In your terminal run

run -> docker run -it --rm --network focus-economics_default -e PGPASSWORD=1234 postgres:17.5-bookworm psql -h postgres -U admin -d focuseconomics
run -> \dt 

# Reults

# docker compose is running postgresql
# docker compose waits until postgresql is up
# docker compose runs app
# app parse pdf and extracting tables
# app parse tables and extracting clean dfs
# app saves all tables in backend/results as csv
# app finds the 3 top Assets, and the 3 worst (printed in console)
# app uploads results to postgres


