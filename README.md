# Description

# Python version

pyhton 3.13.5


# Run

1) Clone github repository
2) From a terminal go to focus-economics directory 
3) make sure docker engine is up and running in your pc
4) run in your terminal -> docker compose up 
5) wait until docker compose up finishes you will see in terminal app-1 exited with code 0


# To check the results in the database


## In your terminal run

run -> docker run -it --rm --network focus-economics_default -e PGPASSWORD=1234 postgres:17.5-bookworm psql -h postgres -U admin -d focuseconomics
run -> \dt 
run -> SELECT * FROM tablename


# Reults

docker compose is running postgresql
docker compose waits until postgresql is up
docker compose runs app
app parse pdf and extracting tables
app parse tables and extracting clean dfs
app saves all tables in backend/results as csv, in folder results - it should appear inside focus-economics folder -
app finds the 3 top Assets, and the 3 worst (printed in console)
app uploads results to postgres

# Problems found

The main problem was to split the tables as they're sometimes joined by error by the pdf parser.

