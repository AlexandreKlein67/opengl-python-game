"""
    Game Objects & Entities
"""

from object.mesh import load_mesh
from view.transform import hex_to_cartesian, axial_linedraw

class GameObject:

    """
        A class for all the game objects
        Variables :
            mesh : Mesh
                -> Each object has a mesh to be displayed
            hexagonal_position : (q, r)
                -> Each object has a position on the grid
                # NOTE:
                To know if the position is valid, ask it to the "global map".
    """

    #---------- CONSTRUCTOR ----------------
    def __init__(self, mesh_constructor, hex_position):
        # Creating the mesh via the mesh_constructor
        self.mesh = load_mesh(
            mesh_constructor["model"],
            mesh_constructor["texture"],
            mesh_constructor.get("is_png", False)
        )

        # Setting the position
        self.hex_position = hex_position
        self.q = hex_position[0]
        self.r = hex_position[1]

        self.actual_position = hex_position

        self.selected = False

    #---------- METHODS --------------------
    def draw(self, projection_view_matrix, texture_shader):
        cartesian_position = hex_to_cartesian(self.actual_position)
        self.mesh.set_position(cartesian_position[0], 0, cartesian_position[1])
        self.mesh.draw(projection_view_matrix, texture_shader)

    def update(self, *args, **kargs):
        pass


class Entity(GameObject):

    #---------- CONSTRUCTOR ----------------
    def __init__(self, game_object_constructor, player_id=0, life_points=1, costs={}):
        """
        Params:
            game_object_constructor : tuple
                -> the tuple containing the constructor for the game object
            player_id : int
                -> the id of the player who own the entity
            life_points : int
                -> the life points. (0 => dead)
            costs : dict
                -> the costs in ressources to create the entity
        """
        super().__init__(
            game_object_constructor["mesh_constructor"],
            game_object_constructor["hex_position"])

        # Setting the variables
        self.player_id = player_id
        self.life_points = life_points
        self.costs = costs


# WARNING: These two classes are very similar for now, but the main differences
# are in the moving and interacting parts.

class Unit(Entity):

    #---------- CONSTRUCTOR ----------------
    def __init__(self, game_object_constructor, entity_constructor):
        """
        Params:
            game_object_constructor : tuple
                -> the tuple containing the constructor for the game object
            entity_constructor : tuple
                -> the tuple containing the constructor for the entity
        """
        super().__init__(
            game_object_constructor,
            entity_constructor["player_id"],
            entity_constructor.get("life_points", 1),
            entity_constructor.get("costs", {}))

        # Moving part of the entity
        self.direction = (0, 1)
        self.is_moving = False

        self.destinations = []
        self.index = 0

        self.current_start = None
        self.current_end = None

        self.speed = 0.05

    def draw(self, projection_view_matrix, shader):
        cartesian_position = hex_to_cartesian(self.actual_position)
        self.mesh.set_position(cartesian_position[0], 0, cartesian_position[1])
        self.mesh.draw(projection_view_matrix, shader)

    def update(self):

        # While unit is moving
        if self.is_moving:
            if self.actual_position == self.hex_position or len(self.destinations) == 0:
                self.is_moving = False
                return

            if round(self.actual_position[0], 3) == self.destinations[self.index][0] and \
               round(self.actual_position[1], 3) == self.destinations[self.index][1]:
                self.current_start = self.destinations[self.index]
                self.index += 1

            self.move_one_tile(self.destinations[self.index])
            self.rotate_from_direction()



    def set_move_target(self, start, end):
        # Check if the unit is not already moving
        if not self.is_moving:

            self.current_start = self.actual_position

            self.is_moving = True
            self.destinations = axial_linedraw(start, end)
            self.index = 0
            # Set the final destination
            self.hex_position = end


    def move_one_tile(self, ending_position):
        direction_vector = (
            ending_position[0] - self.current_start[0],
            ending_position[1] - self.current_start[1],
        )

        self.direction = (int(direction_vector[0]), int(direction_vector[1]))

        self.actual_position = (
            round(self.actual_position[0] + direction_vector[0] * self.speed, 3),
            round(self.actual_position[1] + direction_vector[1] * self.speed, 3)
            )

    def rotate(self, angle):
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

class Building(Entity):

    #---------- CONSTRUCTOR ----------------
    def __init__(self, game_object_constructor, entity_constructor):
        """
        Params:
            game_object_constructor : tuple
                -> the tuple containing the constructor for the game object
            entity_constructor : tuple
                -> the tuple containing the constructor for the entity
        """
        super().__init__(
            game_object_constructor,
            entity_constructor["player_id"],
            entity_constructor["life_points"],
            entity_constructor["costs"])
