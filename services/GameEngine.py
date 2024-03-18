from services.GameStateSelf import GameState

class GameEngine:
    """
    Game engine logic module
    """
    def __init__(self, num_players, does_not_have_visualizer):
        # create the players
        self.game_state     = GameState()
        self.num_players    = num_players
        self.does_not_have_visualizer = does_not_have_visualizer 

    def perform_action(self, action, player_id, can_see_opp):
        """
        use the user sent action to alter the game state
        """
        status = self.game_state.perform_action(action, player_id, can_see_opp, self.does_not_have_visualizer)
        return status
