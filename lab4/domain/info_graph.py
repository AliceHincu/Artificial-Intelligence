class InfoGraph:
    def __init__(self, sensors, min_distance, drone_coordinates):
        """
        Create a dictionary with all the necessary information for the ants
        :param sensors:  result of function sensor_seen_squares
        :param min_distance:  result of function get_sensor_min_distance
        :return:
        """
        print(sensors, min_distance)
        self.sensor_number = {}  # key: tuple with coordinates, value: the sensor number
        self.sensor_coordinates = {}  # key: the sensor number, value: tuple with coordinates
        self.seen_squares = {}  # key: sensor number, value: list with seen squares for each energy
        self.cost = {}  # key: tuple with start number and destination number, value: the distance from start to dest
        self.next_dest = {}  # key: position number, value: list with possible destinations
        self.unseen_squares_coords = sensors  # key: sensor number, value: what squares can it see per value ([0-5])
        self.drone_coordinates = drone_coordinates

        # --- compute values for each dict
        self.sensor_number, self.sensor_coordinates = self.compute_sensor_number(sensors, drone_coordinates)
        self.seen_squares = self.compute_seen_squares(sensors)
        self.cost = self.compute_cost(min_distance)
        self.next_dest = self.compute_next_dest()


    @staticmethod
    def compute_sensor_number(sensors, drone_coordinates):
        sensor_number = {tuple(drone_coordinates): 0}
        sensor_coordinates = {0: tuple(drone_coordinates)}

        for i in range(len(sensors)):
            index = i + 1
            x_coord = sensors[i][0]
            y_coord = sensors[i][1]
            sensor_number[(x_coord, y_coord)] = index
            sensor_coordinates[index] = (x_coord, y_coord)

        return sensor_number, sensor_coordinates

    def compute_seen_squares(self, sensors):
        seen_squares = {}

        for sensor in sensors:
            coord = (sensor[0], sensor[1])
            number = self.sensor_number[coord]
            seen_squares[number] = sensor[2]

        return seen_squares

    def compute_cost(self, distances):
        cost = {}

        for distance in distances:
            src = self.sensor_number[distance[0]]
            dest = self.sensor_number[distance[1]]
            cost[(src, dest)] = distances[distance]
            cost[(dest, src)] = distances[distance]

        return cost

    def compute_next_dest(self):
        next_dest = {}

        for pair in self.cost.keys():
            src = pair[0]
            dest = pair[1]

            if src not in next_dest.keys():
                next_dest[src] = [dest]
            else:
                next_dest[src].append(dest)

            # we should not add the drone coordinates as a destination...the drone coords can only be a src
            if src != 0:
                if dest not in next_dest.keys():
                    next_dest[dest] = [src]
                else:
                    next_dest[dest].append(src)

        # remove duplicates since self.cost has (src, dest) and (dest, src) as keys
        for src in next_dest.keys():
            dest = next_dest[src]
            dest = list(dict.fromkeys(dest))
            next_dest[src] = dest

        return next_dest

    def __str__(self):
        text = "--- Information Graph ---"
        text += f"\n\tsensor_number: {self.sensor_number}"
        text += f"\n\tseen_squares: {self.seen_squares}"
        text += f"\n\tcost: {self.cost}"
        text += f"\n\tnext_dest: {self.next_dest}"
        text += f"\n\tunseen_squares_coords: {self.unseen_squares_coords}"
        return text
