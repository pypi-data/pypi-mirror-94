# Yahtzee API
Welcome to the Yahtzee API! This package provides the core functionalities to programmatically play a game of Yahtzee. The purpose of this package is for use with reinforcement learning environments (in development), however it is generalized for many different use cases including simple algorithm development. 

This package is composed of two classes: the Game class and the Player class. The Game class provides the general structure and manages advancing turns and determining the winner. 
Instantiating a Game object will create a list of Player objects that can be interacted with using the methods outlined in the docs at https://yahtzee-api.tomarbeiter.com.

### Installation
To install this package, run `pip install yahtzee-api`

### Documentation
For complete documentation on the current API methods, please visit https://yahtzee-api.tomarbeiter.com.

### Rules
This API adheres to the rules of Yahtzee outliend here: https://www.hasbro.com/common/instruct/yahtzee.pdf.

### Example
The following is an example of a simple (and really poorly performing!) algorithm playing a 1-player game of Yahtzee with the Yahtzee API:

```python
from yahtzee_api.game import Game

# Specify number of players
game = Game(1)  

# Iterate for each turn
for i in range(13):
    # Roll all 5 dice
    game.c_player.roll([0, 0, 0, 0, 0])
    index = 0
    max_score = 0
    # Choose the highest possible score from that roll
    for entry in game.c_player.t_scorecard:
        if entry[0] >= max_score and entry[2] > 0:
            max_score = entry[0]
            index = game.c_player.t_scorecard.index(entry)
    # End turn by scoring the max value
    game.c_player.end_turn(index)
    # Advances global turn because there is only 1 player
    game.next_player()

game.print_final("test.txt", True)
```
This algorithm is obviously not going to win you any Yahtzee games (it never even rerolls the dice!), but demonstrates some of the core functionalities of the API. I recommend viewing the documentation in tandem with this example to fully understand what each method does/returns.

### A Note on Versioning
This project is my first headfirst dive into the world of publishing Python packages, using Sphinx for documentation, GitHub Actions, etc. As such, there are plenty of junk commits and mistakes in the repo. I've done my best to clean it up and make sure that what is presented is accurate, up-to-date, and at least somewhat helpful. 
Canonically, v0.1.2 is the first release of this package. Yes, v0.1.0 and v0.1.1 existed, but both fell victim to my inexperience with Python publishing (amongst other things). From v0.1.2 on, all changes and versioning will following semantic versioning guidelines specified by https://semver.org/.

### Contributing
Questions? Comments? Want to contribute? Reach out to me via email: arbeitertom@gmail.com.
