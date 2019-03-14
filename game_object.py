"""
    Game Objects & Entities
"""


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
        self.q = position[0]
        self.r = position[1]


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

class Units(Entity):

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
