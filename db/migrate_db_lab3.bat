call liquibase update --changelog-file=./changelogs/create-table-weather.xml

cd ../

call python -m persistance.weather_populate

cd db

call liquibase tag --tag=entire_weather_table

pause