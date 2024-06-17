call liquibase update --changelog-file=./changelogs/create-table-weather.xml

cd ../

call python -m persistance.weather_populate

cd db

call liquibase tag --tag=entire_weather_table

call liquibase update --changelog-file=./changelogs/create-table-astro.xml

cd ../

call python -m persistance.astro_populate

cd db

call liquibase update --changelog-file=./changelogs/cut-table-weather.xml

call liquibase tag --tag=weather_and_astro_state

call liquibase update --changelog-file=./changelogs/add-outside-recommendation.xml

cd ../

call python -m persistance.populate_outside_recommendation

cd db

call liquibase tag --tag=outside_recommendation_state

pause