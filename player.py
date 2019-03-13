"""
    That is what defines a player.
    It has a local view of the map, it can interact with the global map and draw
    the view to the screen.
"""

# Import application's modules
import map.local


class Player:

    #----------- CONSTRUCTOR ----------
    def __init__(self, player_id=-1, global_map=None):
        """
        Params :
        player_id : int -> -1 by default if not set
        """

        # Setting the parameters
        self.id = player_id
        self.local_map = map.local.Map(global_map)

    #---------- METHODS ---------------
    def draw(self, projection_view_matrix, shaders):
        """
        Params :
        projection_view_matrix : mat4
            -> The matrix to project the map
        shaders : dict
            -> Both shaders ("texture" & "color")
        """
        self.local_map.draw(projection_view_matrix, shaders)


    def update(self):

        # Update the local map
        self.local_map.update()
