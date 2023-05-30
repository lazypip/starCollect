res = []  # [(), ]

while True:
    try:
        text = input()
        text = text.split(',')
        _, country, area, city, __ = text

        if country == 'US':
            res.append((country, area, city))
    except:
        break

for i in list(set(res)):
    print(i)
