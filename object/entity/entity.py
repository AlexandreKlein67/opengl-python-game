
from object.mesh import load_mesh
from view.transform import hex_to_cartesian, axial_linedraw, hex_direction

class Entity:

    def __init__(self, model_file, texture_file, png=False):
        self.mesh = load_mesh(model_file, texture_file, png)

        self.position = None

        self.is_moving = False
        self.start_position = None
        self.ending_position = None
        self.current_ending_position = None
        self.positions_to_move = None
        self.i = 0

        self.change_angle = True
        self.start_angle = 0
        self.current_angle = 0
        self.final_angle = 0
        self.angular_speed = 5

        self.direction = hex_direction(0)

        self.speed = 5

        # -----
        self.actions = {}

    def draw(self, projection_view_matrix, shader):
        cartesian_position = hex_to_cartesian(self.position)
        self.mesh.set_position(cartesian_position[0], 0, cartesian_position[1])
        self.mesh.draw(projection_view_matrix, shader)

    def update(self, _dt, keys):
        self.rotate_from_direction()

        if self.position == self.current_ending_position:
            self.i += 1
            self.start_position = self.position

        if self.position == self.ending_position:
            self.is_moving = False
            self.i = 0

        if self.is_moving and self.position != self.ending_position:
            self.move_one_tile(self.positions_to_move[self.i])

    def set_position(self, x, z=None):
        if not z:
            self.mesh.set_position(x[0], 0, x[1])
        else:
            self.mesh.set_position(x, 0, z)


    def move(self, start_position, new_position):
        self.start_position = start_position
        self.ending_position = new_position
        self.positions_to_move = axial_linedraw(start_position, new_position)
        self.is_moving = True


    def move_one_tile(self, position):
        self.current_ending_position = position

        direction_vector = (
            self.current_ending_position[0] - self.start_position[0],
            self.current_ending_position[1] - self.start_position[1],
        )


        self.direction = (int(direction_vector[0]), int(direction_vector[1]))

        speed = self.speed / 100

        new_pos = (
            round(self.position[0] + direction_vector[0] * speed, 3),
            round(self.position[1] + direction_vector[1] * speed, 3)
            )

        self.position = new_pos

    def rotate(self, angle):
        self.final_angle = angle

        if self.change_angle == True:
            self.mesh.rotate((0, 1, 0), angle)

    def rotate_from_direction(self):
        # print(self.direction)
        if self.direction[0] == 1 and self.direction[1] == 0:
            self.rotate(0)
        elif self.direction[0] == 1 and self.direction[1] == -1:
            self.rotate(60)
        elif self.direction[0] == 0 and self.direction[1] == -1:
            self.rotate(120)
        elif self.direction[0] == -1 and self.direction[1] == 0:
            self.rotate(180)
        elif self.direction[0] == -1 and self.direction[1] == 1:
            self.rotate(240)
        elif self.direction[0] == 0 and self.direction[1] == 1:
            self.rotate(300)


    def set_action(self, key, function):
        pass
