import random
import math

class City:
    def __init__(self, lon, lat, name):
        self.lon = lon
        self.lat = lat
        self.name = name

    def distance(self, city):
        distanciaX = (city.lon - self.lon) * 40000 * math.cos((self.lat + city.lat) * math.pi / 360) / 360
        distanciaY = (self.lat - city.lat) * 40000 / 360
        d = math.sqrt((distanciaX * distanciaX) + (distanciaY * distanciaY))
        return d
    
    def get_city_name(self, city):
        return city.name

# Clase administación del tour

class TourAdmin:
    destination_cities = []
    def add_city(self, city):
        self.destination_cities.append(city)
    
    def get_city(self, index):
        return self.destination_cities[index]

    def get_cities(self):
        return self.destination_cities
    
    def number_of_cities(self):
        return len(self.destination_cities)

# Clase administación del tour

class Tour:
    def __init__(self, tour_admin, tour=None):
        self.tour_admin = tour_admin
        self.tour = []
        self.distance = 0
        if tour is not None:
            self.tour = list(tour)
        else:
            for _ in range(0, self.tour_admin.number_of_cities()):
                self.tour.append(None)
    
    def __getitem__(self, index):
        return self.tour[index]

    def generate_tour(self):
        for city_index in range(0, self.tour_admin.number_of_cities()):
            self.set_city(city_index, self.tour_admin.get_city(city_index))

    def get_city(self, tour_pos):
        return self.tour[tour_pos]

    def set_city(self, tour_pos, city):
        self.tour[tour_pos] = city
        self.distance = 0

    def get_distance(self):
        if self.distance == 0:
            tour_distance = 0
            for city_index in range(0, self.tour_length()):
                start_city = self.get_city(city_index)
                if city_index + 1 < self.tour_length():
                    arrival_city = self.get_city(city_index + 1)
                else:
                    arrival_city = self.get_city(0)
                tour_distance += start_city.distance(arrival_city)
            self.distance = tour_distance
        return self.distance

    def tour_length(self):
        return len(self.tour)

    def show(self):
        for i in range(0, self.tour_length()):
            print(self.get_city(i).name)

# Simulated Annealing

class SimulatedAnnealing:
    def __init__(self, destinations, init_temp, velocity):
        self.tour_admin = destinations
        self.tour = Tour(destinations)
        self.tour.generate_tour()
        self.best = self.tour
        self.temperature = init_temp
        self.velocity = velocity
        self.cont = 0
    
    def acceptance_function(self, delta_energy):
        if delta_energy < 0:
            return True
        elif random.random() <= math.exp(-(delta_energy/self.temperature)):
            return True
        return False
    
    def new_tour(self):
        new_tour = Tour(self.tour_admin, self.tour)
        pos1 = random.randrange(self.tour.tour_length())
        pos2 = random.randrange(self.tour.tour_length())
        city1 = new_tour.get_city(pos1)
        city2 = new_tour.get_city(pos2)
        new_tour.set_city(pos2, city1)
        new_tour.set_city(pos1, city2)
        actual_energy = self.tour.get_distance()
        new_energy = new_tour.get_distance()
        delta = new_energy - actual_energy
        if self.acceptance_function(delta):
            self.tour = new_tour
        if(new_tour.get_distance() < self.best.get_distance()):
            self.best = new_tour
            print(new_tour.get_distance())
    
    def run(self):
        while self.temperature > 1:
            self.cont = self.cont + 1
            self.new_tour()
            self.temperature = (1 - self.velocity) * self.temperature

def main():
    destinations = TourAdmin()
    city1 = City(-77.0282400, -12.0431800, 'Lima')
    destinations.add_city(city1)
    city2 = City(-55.0000000, -10.0000000, 'Brasil')
    destinations.add_city(city2)
    city3 = City(-65.0000000, -17.0000000, 'Bolivia')
    destinations.add_city(city3)
    city4 = City(-58.0000000, -23.0000000, 'Paraguay')
    destinations.add_city(city4)
    city5 = City(-71.0000000, -30.0000000, 'Chile')
    destinations.add_city(city5)
    
    sa = SimulatedAnnealing(destinations, init_temp=10000, velocity=0.003)
    print(sa.tour.show())
    print(sa.tour.get_distance())
    sa.run()
    print(sa.tour.show())
    print(sa.tour.get_distance())
    print(sa.cont)

main()