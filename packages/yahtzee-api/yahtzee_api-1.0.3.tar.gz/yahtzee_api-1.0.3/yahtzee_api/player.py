import random
import copy
from .constants import (BAD_LENGTH, BAD_SCORE_TYPE, BAD_TYPE,
                        NO_BINARY, NO_ROLLS_LEFT, ALL_DICE)


class Player:
    """Stores information about each player's current status including score,
    theoretical score, rolls remaining in their turn, and the status of their
    last roll.

    This class tracks the data associated with each player, and additionally
    performs all scoring calculations including all possible scores based on
    the current configuration of the dice and their scorecard. The Player
    object will expose all of the relevant information needed for algorithmic
    decision making, including a theoretical scorecard that gives all the
    possible scores based on what the player has already scored and the
    current configuration of the dice.

    Attributes:
        player_name (str): A string containing the name of the player.
        score (int): An integer value indicating the point total for the
            player (calculated at the end of the game).
        scorecard (list): A list of lists tracking each row of a Yahtzee
            scorecard, with each row (inner list) of the card following
            this structure: [score, [dice used to get score], number of rolls].
            This is updated when a player ends their turn with the end_turn()
            method.

            Scorecard indices are as follows:

            [0]: 1's

            [1]: 2's

            [2]: 3's

            [3]: 4's

            [4]: 5's

            [5]: 6's

            [6]: Three of a Kind

            [7]: Four of a Kind

            [8]: Full House

            [9]: Small Straight

            [10]: Large Straight

            [11]: Yahtzee

            [12]: Chance

        t_scorecard (list): A list of lists tracking each row of a
            Yahtzee scorecard, calculated after each roll, with each row of
            the card following this structure:
            [score, [0 if index is unused, 1 if index is used], # of rolls].
            This is calculated after every roll and can be used to make
            decisions about which dice to roll again, which score to take,
            and more.

            Theoretical Scorecard indices are as follows:

            [0]: 1's

            [1]: 2's

            [2]: 3's

            [3]: 4's

            [4]: 5's

            [5]: 6's

            [6]: Three of a Kind

            [7]: Four of a Kind

            [8]: Full House

            [9]: Small Straight

            [10]: Large Straight

            [11]: Yahtzee

            [12]: Chance

        dice (list): A list of the 5 dice in play - index is preserved
            throughout calculations.
        rolls_left (int): Integer tracking how many rolls the player has left
            on the current turn (there are 3 rolls per turn).
        jokers (int): Tracks how many times a Yahtzee was used as a Joker.
    """
    def __init__(self, player_name):
        """Constructor method for Player class.

        Args:
            player_name: A string specifying the name for the instance of
                the Player class.
        """
        self.player_name = player_name
        self.score = 0
        self.scorecard = [
            [0, [0, 0, 0, 0, 0], 0],         # 1's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 2's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 3's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 4's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 5's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 6's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Three of a Kind (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Four of a Kind (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Full House (25)
            [0, [0, 0, 0, 0, 0], 0],         # Small Straight (30)
            [0, [0, 0, 0, 0, 0], 0],         # Large Straight (40)
            [0, [0, 0, 0, 0, 0], 0],         # Yahtzee (50)
            [0, [0, 0, 0, 0, 0], 0],         # Chance (value of dice)
        ]
        self.t_scorecard = [
            [0, [0, 0, 0, 0, 0], 0],         # 1's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 2's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 3's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 4's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 5's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # 6's (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Three of a Kind (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Four of a Kind (value of dice)
            [0, [0, 0, 0, 0, 0], 0],         # Full House (25)
            [0, [0, 0, 0, 0, 0], 0],         # Small Straight (30)
            [0, [0, 0, 0, 0, 0], 0],         # Large Straight (40)
            [0, [0, 0, 0, 0, 0], 0],         # Yahtzee (50)
            [0, [0, 0, 0, 0, 0], 0],         # Chance (value of dice)
        ]
        # Master list of dice - index preserved
        self.dice = [0, 0, 0, 0, 0]
        self.rolls_left = 3
        self._sorted_dice = []
        self._bonus = False

    def roll(self, to_roll):
        """Rolls dice specified by the to_roll list, updates related class
        attributes, and calculates the theoretical scorecard values.

        Args:
            to_roll (list): A list of length 5 containing binary values
                where 0 indicates the die in that position should be rolled.

        Raises:
            ValueError: If the number of rolls remaining is <= 0.
            TypeError: If to_roll is not a list.
            ValueError: If the length of to_roll is not 5.
            TypeError: If the to_roll list is not only binary values.
            ValueError: If the player attempts to roll fewer than 5 dice on
                the first roll of their turn.
        """
        if self.rolls_left <= 0:
            raise ValueError(NO_ROLLS_LEFT)
        if not isinstance(to_roll, list):
            raise TypeError(BAD_TYPE)
        if len(to_roll) != 5:
            raise ValueError(BAD_LENGTH)
        if len([x for x in to_roll if x not in [0, 1]]) != 0:
            raise TypeError(NO_BINARY)
        if self.rolls_left == 3 and len([x for x in to_roll if x != 0]) > 0:
            raise ValueError(ALL_DICE)
        for i in range(5):
            if to_roll[i] == 0:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1
        self._sorted_dice = copy.deepcopy(self.dice)
        self._sorted_dice.sort()
        self._calculate_yahtzee_bonus()
        self._reset_t_scorecard()
        self._calculate_t_scorecard()

    def end_turn(self, score_type):
        """Resets turn-based parameters and fills in scorecard based on player choice.

        Args:
            score_type (int): Index of the scorecard entry that the player has
                chosen to score for this round.
        Raises:
            ValueError: If score_type is not between 0 and 12.
        """
        if score_type < 0 or score_type > 12:
            raise ValueError(BAD_SCORE_TYPE)

        self.scorecard[score_type][0] = self.t_scorecard[score_type][0]
        self.scorecard[score_type][1] = copy.deepcopy(self.dice)
        self.scorecard[score_type][2] = 3 - self.rolls_left
        self._calculate_bonus()
        self.rolls_left = 3
        self.dice = copy.deepcopy([0, 0, 0, 0, 0])
        self._reset_t_scorecard()

    def _reset_t_scorecard(self):
        """Resets the theoretical scorecard.
        Called after each roll of the dice.
        """
        self.t_scorecard = [
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
            [0, [0, 0, 0, 0, 0], 0],
        ]

    def _calculate_top_half(self):
        """Calculates values for 1's --> 6's based on the current roll and
        stores result in the theoretical scorecard.
        """
        for i in range(6):
            # Checks if scorecard entry has not been scored yet.
            # Looks at # of rolls in case of a 0 on an entry after 3 rolls.
            if self.scorecard[i][2] == 0:
                # Builds list tracking which indices are used in calculation
                dice_indices = [1 if self.dice[j] == i + 1 else 0
                                for j in range(5)]
                self.t_scorecard[i][0] = dice_indices.count(1) * (i + 1)
                self.t_scorecard[i][1] = dice_indices
                self.t_scorecard[i][2] = 3 - self.rolls_left

    def _calculate_three_kind(self):
        """Calculates three of a kind value based on the current roll and
        stores result in the theoretical scorecard.
        """
        # Checks if scorecard entry has not been scored yet.
        # Looks at # of rolls in case of a 0 on an entry after 3 rolls.
        if self.scorecard[6][2] == 0:
            # For each die value, check 3 of a kind, store the indices of the
            # dice in the dice_indices list, and update theoretical scorecard.
            for i in range(6):
                # Builds list tracking which indices are used in calculation
                dice_indices = [1 if self.dice[j] == i + 1 else 0
                                for j in range(5)]
                # Only one three of a kind can exist, so once it is found
                # update the theoretical scorecard and return.
                if dice_indices.count(1) == 3:
                    self.t_scorecard[6][0] = sum(self.dice)
                    self.t_scorecard[6][1] = dice_indices
                    self.t_scorecard[6][2] = 3 - self.rolls_left
                    return
            # Set the rolls used so far even if we don't have a 3 of a kind.
            self.t_scorecard[6][2] = 3 - self.rolls_left

    def _calculate_four_kind(self):
        """Calculates four of a kind value based on the current roll and stores
        result in the theoretical scorecard.
        """
        # Checks if scorecard entry has not been scored yet.
        # Looks at # of rolls in case of a 0 on an entry after 3 rolls.
        if self.scorecard[7][2] == 0:
            # For each die value, check 4 of a kind, store the indices of the
            # dice in the dice_indices array, and update theoretical scorecard.
            for i in range(6):
                # Builds list tracking which indices are used in calculation
                dice_indices = [1 if self.dice[j] == i + 1 else 0
                                for j in range(5)]
                # Only one four of a kind can exist, so once it is found update
                # the theoretical scorecard and return.
                if dice_indices.count(1) == 4:
                    self.t_scorecard[7][0] = sum(self.dice)
                    self.t_scorecard[7][1] = dice_indices
                    self.t_scorecard[7][2] = 3 - self.rolls_left
                    return
            # Set the rolls used even if we don't have a 4 of a kind.
            self.t_scorecard[7][2] = 3 - self.rolls_left

    def _calculate_full_house(self):
        """Calculates full house based on current roll (uses sorted dice) and
        stores result in the theoretical scorecard.

        Leverages the fact that the dice are sorted, so just check if first 2
        are the same and the last 3 are the same or vice versa,
        and that all 5 are not the same.
        """
        # Checks if scorecard entry has not been scored yet.
        # Looks at # of rolls in case of a 0 on an entry after 3 rolls.
        if self.scorecard[8][2] == 0:
            if (self._sorted_dice[0] == self._sorted_dice[1] and
                    self._sorted_dice[2] == self._sorted_dice[4] and
                    self._sorted_dice[0] != self._sorted_dice[4]):
                self.t_scorecard[8][0] = 25
                self.t_scorecard[8][1] = [1, 1, 1, 1, 1]
            if (self._sorted_dice[0] == self._sorted_dice[2] and
                    self._sorted_dice[3] == self._sorted_dice[4] and
                    self._sorted_dice[0] != self._sorted_dice[4]):
                self.t_scorecard[8][0] = 25
                self.t_scorecard[8][1] = [1, 1, 1, 1, 1]
            # Set the rolls used even if we don't have a full house.
            self.t_scorecard[8][2] = 3 - self.rolls_left

    def _calculate_small_straight(self):
        """Calculates small straight based on current roll
        (uses sorted dice and additionally removes duplicates)
        and storeS result in the theoretical scorecard.
        """
        # Checks if scorecard entry has not been scored yet.
        # Looks at # of rolls in case of a 0 on an entry after 3 rolls.
        if self.scorecard[9][2] == 0:
            found = False
            # Remove duplicates from combined dice to remove edge cases from
            # small straight test (i.e., [2, 3, 3, 4, 5]) then check that
            # there are still at least 4 dice.
            temp_dice = copy.deepcopy(list(dict.fromkeys(self._sorted_dice)))
            dice_indices = [0, 0, 0, 0, 0]
            if len(temp_dice) == 5:
                # Small straight in sorted list of 5 must start at postion 0 or
                # position 1, so do two iterations to check those positions.
                for i in range(2):
                    if (temp_dice[i + 1] == temp_dice[i] + 1 and
                            temp_dice[i + 2] == temp_dice[i + 1] + 1 and
                            temp_dice[i + 3] == temp_dice[i + 2] + 1):
                        found = True
                        temp_dice = temp_dice[1:] if i == 1 else temp_dice[:4]
                        break
            elif len(temp_dice) == 4:
                # Small straight in sorted list of 4 must start at position 0.
                if (temp_dice[1] == temp_dice[0] + 1 and
                        temp_dice[2] == temp_dice[1] + 1 and
                        temp_dice[3] == temp_dice[2] + 1):
                    found = True
            if found:
                for elt in temp_dice:
                    if elt in self.dice:
                        dice_indices[self.dice.index(elt)] = 1
                self.t_scorecard[9][0] = 30
                self.t_scorecard[9][1] = dice_indices
            # Set the rolls used even if we don't have a small straight.
            self.t_scorecard[9][2] = 3 - self.rolls_left

    def _calculate_large_straight(self):
        """Calculates large straight based on current roll (uses sorted dice)
        and stores result in theoretical scorecard.
        """
        if self.scorecard[10][2] == 0:
            if (self._sorted_dice[1] == self._sorted_dice[0] + 1 and
                    self._sorted_dice[2] == self._sorted_dice[1] + 1 and
                    self._sorted_dice[3] == self._sorted_dice[2] + 1 and
                    self._sorted_dice[4] == self._sorted_dice[3] + 1):
                self.t_scorecard[10][0] = 40
                self.t_scorecard[10][1] = [1, 1, 1, 1, 1]
            # Set the rolls used even if we don't have a large straight.
            self.t_scorecard[10][2] = 3 - self.rolls_left

    def _calculate_yahtzee(self):
        """Calculates Yahtzee based on current roll/frozen dice combo
        (uses sorted dice) and store result in theoretical scorecard.
        """
        if self.scorecard[11][2] == 0:
            if self._sorted_dice[0] == self._sorted_dice[-1]:
                self.t_scorecard[11][0] = 50
                self.t_scorecard[11][1] = [1, 1, 1, 1, 1]
            # Set the rolls used even if we don't have a yahtzee.
            self.t_scorecard[11][2] = 3 - self.rolls_left
        # If the number making the Yahtzee has been scored in the upper half,
        # Joker rules apply.
        elif self.scorecard[self.dice[0] - 1][2] != 0:
            if self.scorecard[6][2] == 0:
                self.t_scorecard[6][0] = sum(self.dice)
                self.t_scorecard[6][1] = [1, 1, 1, 1, 1]
                self.t_scorecard[6][2] = 3 - self.rolls_left
            if self.scorecard[7][2] == 0:
                self.t_scorecard[7][0] = sum(self.dice)
                self.t_scorecard[7][1] = [1, 1, 1, 1, 1]
                self.t_scorecard[7][2] = 3 - self.rolls_left
            if self.scorecard[8][2] == 0:
                self.t_scorecard[8][0] = 25
                self.t_scorecard[8][1] = [1, 1, 1, 1, 1]
                self.t_scorecard[8][2] = 3 - self.rolls_left
            if self.scorecard[9][2] == 0:
                self.t_scorecard[9][0] = 30
                self.t_scorecard[9][1] = [1, 1, 1, 1, 1]
                self.t_scorecard[9][2] = 3 - self.rolls_left
            if self.scorecard[10][2] == 0:
                self.t_scorecard[10][0] = 40
                self.t_scorecard[10][1] = [1, 1, 1, 1, 1]
                self.t_scorecard[10][2] = 3 - self.rolls_left

    def _calculate_chance(self):
        """Calculates chance value and store result
        in theoretical scorecard.
        """
        if self.scorecard[12][2] == 0:
            self.t_scorecard[12][0] = sum(self.dice)
            self.t_scorecard[12][1] = [1, 1, 1, 1, 1]
            self.t_scorecard[12][2] = 3 - self.rolls_left

    def _calculate_bonus(self):
        """Determines if Player has earned the top-half bonus by scoring at
        least 63 points on the first 6 scorecard entries.
        """
        total = 0
        for i in range(6):
            total += self.scorecard[i][0]
        if total >= 63 and not self._bonus:
            self.score += 35
            self.bonus = True

    def _calculate_yahtzee_bonus(self):
        """Adds Yahtzee bonus to Player's total score when earned.

        Yahtzee bonus is earned by rolling more than one Yahtzee in a single
        game and is worth 100 points.
        """
        if (self.scorecard[11][0] == 50 and
                self._sorted_dice[0] == self._sorted_dice[4]):
            self.score += 100

    def _calculate_t_scorecard(self):
        """Wrapper function to fill in the entire theoretical scorecard
        after each roll.
        """
        self._calculate_top_half()
        self._calculate_three_kind()
        self._calculate_four_kind()
        self._calculate_full_house()
        self._calculate_small_straight()
        self._calculate_large_straight()
        self._calculate_yahtzee()
        self._calculate_chance()
