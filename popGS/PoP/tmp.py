
country_list = []
city_list = []

while True:
    try:
        text = input()
        text = text.split(',')
        country, city = text[1], text[3]
        country_list.append(country)
        city_list.append(city)
    except:
        break

country_list = list(set(country_list))
city_list = list(set(city_list))

print(len(country_list))
print('city', len(city_list))
