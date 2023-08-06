"""Longer strings for error messages, etc."""
# Error messages for Player.roll()
NO_ROLLS_LEFT = "ValueError in Player.roll(): No rolls remaining."
BAD_TYPE = "TypeError in Player.roll(): dice_to_roll must be \
    of type list."
BAD_LENGTH = "ValueError in Player.roll():dice_to_roll \
                argument must be a list of length 5."
NO_BINARY = "TypeError in Player.roll(): dice_to_roll \
                argument must contain only binary values."
ALL_DICE = "Error in Player.roll(): All 5 dice must be \
                rolled on the first roll of the turn."

# Error messages for Player.end_turn()
BAD_SCORE_TYPE = "ValueError in Player.end_turn(): score_type must be between \
                    0 and 12, inclusive."
