from persistance.all_weather_access import AllWeatherDAO

weather_source = AllWeatherDAO()
weather_source.connect()
end = False
while not end:
    country, last = tuple(input('Enter country, last_updated: ').split(', '))
    print(weather_source.read(country, last))
    end = input('End program?[y/n]: ') == 'y'

weather_source.disconnect()