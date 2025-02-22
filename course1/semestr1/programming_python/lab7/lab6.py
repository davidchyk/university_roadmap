class Planets:

    def __init__(self, name="", number=0, distance=0, volume=0, mass=0, speed=0):

        self.name = name
        self.number = number
        self.distance = distance
        self.volume = volume
        self.mass = mass
        self.speed = speed

    def density(self):

        return round(self.mass / self.volume, 4)

    def mass_ratio(self):

        return round(5.976 / self.mass, 4)

    def speed_ratio(self):

        return round(29.78 / self.speed, 4)

mercury = Planets(name="Меркурій", number=1, distance=57.9, volume=3.7, mass=3.303, speed=15.06)
venus = Planets(name="Венера", number=2, distance=108.2, volume=12.11, mass=4.867, speed=24.62)
earth = Planets(name="Земля", number=3, distance=149.6, volume=12.12, mass=5.976, speed=29.78)
mars = Planets(name="Марс", number=4, distance=227.9, volume=6.419, mass=6.417, speed=24.62)
jupiter = Planets(name="Юпітер", number=5, distance=778.6, volume=13.08, mass=1898.0, speed=11.86)
saturn = Planets(name="Сатурн", number=6, distance=1433.5, volume=9.44, mass=568.0, speed=29.78)
uranus = Planets(name="Уран", number=7, distance=2872.5, volume=8.69, mass=86.8, speed=82.74)
neptune = Planets(name="Нептун", number=8, distance=4498.1, volume=11.15, mass=102.4, speed=164.79)
pluto = Planets(name="Плутон", number=9, distance=5906.4, volume=0.91, mass=206.2, speed=24.62)

planet_list = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

result = []

for x in sorted([planet.density() for planet in planet_list]):

    for planet in planet_list:

        if planet.density() == x: result.append(planet.name)

"""
while True:

    result = []

    planet_name = input("Введіть планету для розрахунку: ")
    for planet in planet_list:

        if planet.name == planet_name:

            print(f"Інформація щодо {planet.name}:\n",
                    f"Густина = {planet.density()} кг/м3\n",
                    f"Маса {planet.name} відносно маси Землі = {planet.mass_ratio()}\n",
                    f"Швидкість {planet.name} відносно швидкості Землі = {planet.speed_ratio()}\n")

    for x in sorted([planet.density() for planet in planet_list]):

        for planet in planet_list:

            if planet.density() == x: result.append(planet.name)

    print(f"Список планет з найбільш більшою густиною:\n{result} \n\n")

"""