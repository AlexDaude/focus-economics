# Description

# Python version

python 3.13.5


# Run

1) Clone github repository -> https://github.com/AlexDaude/focus-economics.git
2) From a terminal go to focus-economics directory 
3) make sure docker engine is up and running in your pc
4) run in your terminal -> docker compose up 
5) wait until docker compose up finishes you will see in terminal app-1 exited with code 0


# Check results in postgres


## In your terminal run

1) run -> docker run -it --rm --network focus-economics_default -e PGPASSWORD=1234 postgres:17.5-bookworm psql -h postgres -U admin -d focuseconomics
2) run -> \dt 
3) run -> SELECT * FROM tablename


# Results

1) docker compose is running postgresql
2) docker compose waits until postgresql is up
3) docker compose runs app
4) app parse pdf and extracting tables
5) app parse tables and extracting clean dfs
6) app split tables if they're wrongly joined
6) app saves all tables in backend/results as csv, in folder results - it should appear inside focus-economics folder -
7) app finds the 3 top Assets, and the 3 worst (printed in console)
8) app uploads results to postgres

# Problems found

The main problem was to split the tables as they're sometimes joined by error by the pdf parser.

