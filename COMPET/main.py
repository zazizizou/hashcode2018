import numpy as np


def read_rides(filename):
    with open(filename, "r") as file:
        param = file.readline().replace("\n", "").split(" ")
        r = int(param[0])
        c = int(param[1])
        f = int(param[2])
        n = int(param[3])
        b = int(param[4])
        t = int(param[5])

        rides = []
        for line in file:
            rides += [line.replace("\n", "").split(" ")]

    return (r,c,f,n,b,t), rides


def distance(ax, ay, bx, by):
    return np.abs(ax - bx) + np.abs(ay - by)


class Car:

    def __init__(self, ride, B):
        self.ride = ride

        self.pos_x = 0
        self.pos_y = 0

        self.ax = int(self.ride[0])
        self.ay = int(self.ride[1])
        self.bx = int(self.ride[2])
        self.by = int(self.ride[3])
        self.t_start = int(self.ride[4])
        self.t_finish = int(self.ride[5])
        self.start_on_time_bonus = int(B)

        self.remaining_distance = distance(self.pos_x, self.pos_y, self.bx, self.by)
        self.distance_to_pickup = distance(self.pos_x, self.pos_y, self.ax, self.ay)

        self.status = "WAITING"

    def go_to_client(self):
        if self.pos_x - self.ax > 0:
            self.pos_x -= 1
            self.status = "GOING_TO_CLIENT"
        elif self.pos_x - self.ax < 0:
            self.pos_x += 1
            self.status = "GOING_TO_CLIENT"
        elif self.pos_y - self.ay < 0:
            self.pos_y += 1
            self.status = "GOING_TO_CLIENT"
        elif self.pos_y - self.ay > 0:
            self.pos_y -= 1
            self.status = "GOING_TO_CLIENT"

        elif self.pos_x == self.ax and self.pos_y == self.ay:
            self.status = "ARRIVED_TO_CLIENT"

    def go_to_destination(self, global_time):
        if global_time >= self.t_start:
            if self.pos_x - self.bx < 0:
                self.pos_x += 1
                self.status = "GOING_TO_DESTINATION"
            elif self.pos_x - self.bx > 0:
                self.pos_x -= 1
                self.status = "GOING_TO_DESTINATION"
            elif self.pos_y - self.by < 0:
                self.pos_y += 1
                self.status = "GOING_TO_DESTINATION"
            elif self.pos_y - self.by > 0:
                self.pos_y -= 1
                self.status = "GOING_TO_DESTINATION"

            elif self.pos_x == self.bx and self.pos_y == self.by:
              self.status = "ARRIVED!"

    def step(self, global_time):

        if self.status == "WAITING":
            self.go_to_client()
        elif self.status == "ARRIVED_TO_CLIENT":
            self.go_to_destination(global_time)
        elif self.status == "GOING_TO_DESTINATION":
            self.go_to_destination(global_time)
        elif self.status == "GOING_TO_CLIENT":
            self.go_to_client()

        # TODO: add case for missed ride

        return self.status


def write_assignments(filename, assignments):
    with open(filename, "w") as file:
        for ass in assignments:
            for elm in ass:
                file.write(str(elm) + " ")
            file.write("\n")


def get_closest_available_car_to_ride(all_cars, rides):
    dist = np.empty((len(all_cars), len(rides)))
    for i, car in enumerate(all_cars):
        if car.status == "ARRIVED!":
            for j, ride in enumerate(rides):
                dist[i][j] = distance(int(car.pos_x), int(car.pos_y), int(ride[0]), int(ride[1]))

    min_idx =  np.unravel_index(np.argmin(dist, axis=None), dist.shape)
    closest_car_idx, closest_ride_idx = min_idx[0], min_idx[1]
    return closest_car_idx, closest_ride_idx


def main():

    data = ["a_example.in",
            "b_should_be_easy.in",
            "c_no_hurry.in",
            "d_metropolis.in",
            "e_high_bonus.in"]

    for dataset_file in data:
        (rows, columns, nb_cars, nb_rides, bonus_per_ride, nb_sim_steps), rides = read_rides(dataset_file)

        # distribute initial rides on cars
        all_cars = []
        assignments = []
        rides_counter = 0
        for n in range(int(nb_cars)):
            all_cars += [Car(rides[0], bonus_per_ride)]
            assignments += [[1, n]]
            rides.pop(0)
            rides_counter += 1

        # simulation
        for global_time in range(nb_sim_steps):
            if global_time % 1000 == 0:
                print(global_time, "from ", nb_sim_steps, "complete")
            for idx, car in enumerate(all_cars):
                # print("status " + str(idx), car.status)
                car.step(global_time)

            if len(rides) != 0:
                closest_car_idx, closest_ride_idx = get_closest_available_car_to_ride(all_cars, rides)
                closest_car = all_cars[closest_car_idx]
                closest_car.rides = rides[closest_ride_idx]
                rides.pop(closest_ride_idx)
                assignments[closest_car_idx][0] += 1
                assignments[closest_car_idx].append(rides_counter)
                rides_counter += 1
                closest_car.status = "WAITING"

        write_assignments(dataset_file.replace("in", "out"), assignments)


if __name__ == "__main__":
    main()