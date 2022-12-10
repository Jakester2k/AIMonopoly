# Import the random module to use the randint() function
from random import randint

# Define a Player class
class Player:
  def __init__(self, name, money):
    self.name = name
    self.money = money
    self.properties = []
    self.jail_time = 0
    self.get_out_of_jail_card = False
    self.position = 0

  def roll_dice(self):
    # Roll two dice and return their sum
    return randint(1, 6) + randint(1, 6)

  def move(self, spaces):
    self.position += spaces

    # Check if the player passed "Go"
    if self.position > 39:
      self.position -= 40
      self.money += 200

  def buy_property(self, property):
    self.money -= property.cost
    self.properties.append(property)

  def sell_property(self, property):
    self.money += property.cost
    self.properties.remove(property)

  def pay_rent(self, owner, amount):
    self.money -= amount
    owner.money += amount

  def decide_to_buy(self, property):
    # Prompt the player to decide whether to buy the property
    response = input(f"{self.name}, would you like to buy {property.name} for ${property.cost}? (y/n) ")
    return response.lower() == 'y'

  def decide_to_sell(self, property):
    # Prompt the player to decide whether to sell the property
    response = input(f"{self.name}, would you like to sell {property.name} for ${property.cost}? (y/n) ")
    return response.lower() == 'y'

  def use_get_out_of_jail_card(self):
    if self.get_out_of_jail_card:
      # Prompt the player to decide whether to use a "Get Out of Jail" card
      response = input(f"{self.name}, would you like to use a Get Out of Jail card? (y/n) ")
      if response.lower() == 'y':
        self.get_out_of_jail_card = False
        self.jail_time = 0
        return True
    return False

  def decide_to_pay(self, amount):
    # Prompt the player to decide whether to pay to get out of jail
    response = input(f"{self.name}, would you like to pay ${amount} to get out of jail? (y/n) ")
    return response.lower() == 'y'

# Define a Property class
class Property:
  def __init__(self, name, cost, rent=0):
    self.name = name
    self.cost = cost
    self.rent = rent
    self.owner = None

# Define a SpecialSpace class
class SpecialSpace():
  def __init__(self, name, space_action):
    self.name = name
    self.space_action = space_action

  def action(self, player):
    # Perform the action for the special space
    self.space_action(player)

class SpecialUtility(SpecialSpace):
  def __init__(self, name, space_action):
    self.name = name
    self.space_action = space_action
    self.owner = ''

# Define an action for the "Go" space
def go_action(player):
  player.money += 200

# Define a better action for the "Jail" space
def jail_action(player):
  if player.jail_time == 0:
    player.jail_time = 3

  if player.jail_time > 0:
    # Check if the player has a "Get Out of Jail" card
    if player.get_out_of_jail_card:
      # Prompt the player to decide whether to use a "Get Out of Jail" card
      response = input(f"{player.name}, would you like to use a Get Out of Jail card? (y/n) ")
      if response.lower() == 'y':
        player.get_out_of_jail_card = False
        player.jail_time = 0
        return

    # Prompt the player to decide whether to pay to get out of jail
    response = input(f"{player.name}, would you like to pay ${50} to get out of jail? (y/n) ")
    if response.lower() == 'y':
      player.money -= 50
      player.jail_time = 0

# Define the "Free Parking" space
def free_parking_action(player):
  # Prompt the player to decide whether to collect the money in the Free Parking pot
  response = input(f"{player.name}, would you like to collect ${free_parking_pot} from the Free Parking pot? (y/n) ")
  if response.lower() == 'y':
    player.money += free_parking_pot

# Define an action for the "Go to Jail" space
def goto_jail_action(player):
  player.jail_time = 3
  player.position = 10

# Define an action for the "Luxury Tax" space
def luxury_tax_action(player):
  # Take the Luxury Tax amount from the player and add it to the Free Parking pot
  global free_parking_pot
  player.money -= 75
  free_parking_pot += 75

def income_tax_action(player):
  # Prompt the player to choose between paying 10% of their money or $200
  response = input(f"{player.name}, would you like to pay 10% of your money (${player.money * 0.1}) or $200? (10%/200) ")

  # Calculate the tax amount based on the player's response
  if response.lower() == '10%':
    tax_amount = player.money * 0.1
  elif response.lower() == '200':
    tax_amount = 200
  else:
    tax_amount = 0
    print(f"Invalid response. {player.name} did not pay any tax.")

  # Check if the player can afford to pay the tax
  if tax_amount > player.money:
    tax_amount = player.money

  player.money -= tax_amount
  print(f"{player.name} paid ${tax_amount} in income tax.")

  # Check if the player went bankrupt
  if player.money < 0:
    player.properties = []
    player.jail_time = 0
    player.get_out_of_jail_card = False
    player.position = 0
    print(f"{player.name} went bankrupt and lost all of their properties and cards.")

# Define an action for a utility space
def utility_action(player):
  # Check if the utility is owned by another player
  if player.position.owner is not None and player.position.owner != player:
    # Calculate the rent to pay based on the number of utilities owned by the owner
    num_utilities = sum([1 for property in player.position.owner.properties if isinstance(property, Utility)])
    rent = player.position.rent * player.last_dice_roll * num_utilities

    # Pay the rent to the owner
    player.pay_rent(player.position.owner, rent)

def choose_random_card():
  # Create a list of the 16 cards in the chance deck
  chance_cards = [
    "Advance to Go",
    "Go to Jail",
    "Get out of Jail Free",
    "Advance to Illinois Ave.",
    "Advance to St. Charles Place",
    "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 times the amount thrown.",
    "Advance to the nearest Railroad and pay owner twice the rental to which they are otherwise entitled.",
    "Bank pays you dividend of $50",
    "Get Out of Jail Free",
    "Go back 3 spaces",
    "Make general repairs on all your property - for each house pay $25 - for each hotel $100",
    "Pay poor tax of $15",
    "Take a trip to Reading Railroad - if you pass Go, collect $200",
    "Take a walk on the Boardwalk - advance token to Boardwalk",
    "You have been elected chairman of the board - pay each player $50",
    "Your building and loan matures - collect $150"
  ]

  # Choose a random index from 0 to 15
  index = randint(0, 15)

  # Return the card at the chosen index
  return chance_cards[index]

def chance_action(player):
  # Choose a random card from the chance deck
  card = choose_random_card()

  # Perform the action for the chosen card
  if card == "Advance to Go":
    player.position = 0
    player.money += 200
  elif card == "Go to Jail":
    player.position = 10
    player.jail_time = 3
  elif card == "Get out of Jail Free":
    player.get_out_of_jail_card = True
  elif card == "Advance to Illinois Ave.":
    player.position = 24
  elif card == "Advance to St. Charles Place":
    player.position = 11
  elif card == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 times the amount thrown.":
    if player.position == 7 or player.position == 22:
      player.position = 12
      property = board.properties[12]
      if property.owner:
        player.pay_rent(property.owner, 10 * (randint(1, 6) + randint(1, 6)))
      else:
        player.decide_to_buy(property)
    elif player.position == 36:
      player.position = 28
      property = board.properties[28]
      if property.owner:
        player.pay_rent(property.owner, 10 * (randint(1, 6) + randint(1, 6)))
      else:
        player.decide_to_buy(property)
  elif card == "Advance to the nearest Railroad and pay owner twice the rental to which they are otherwise entitled.":
    if player.position == 7 or player.position == 22 or player.position == 36:
      player.position = 5
      property = board.properties[5]
      if property.owner:
        player.pay_rent(property.owner, 2 * property.rent)
      else:
        player.decide_to_buy(property)
    elif player.position == 12 or player.position == 28:
      player.position = 15
      property = board.properties[15]
      if property.owner:
        player.pay_rent(property.owner, 2 * property.rent)
      else:
        player.decide_to_buy(property)
    elif card == "Bank pays you dividend of $50":
        player.money += 50
    elif card == "Get Out of Jail Free":
        player.get_out_of_jail_card = True
    elif card == "Go back 3 spaces":
        player.position -= 3
    elif card == "Make general repairs on all your property - for each house pay $25 - for each hotel $100":
        total_cost = 0
        for property in player.properties:
            if property.number_of_houses == 5:
                total_cost += 100
            else:
                total_cost += property.number_of_houses * 25
        player.money -= total_cost
    elif card == "Pay poor tax of $15":
      player.money -= 15
    elif card == "Take a trip to Reading Railroad - if you pass Go, collect $200":
        if player.position >= 5:
            player.money += 200
        player.position = 5
    elif card == "Take a walk on the Boardwalk - advance token to Boardwalk":
        player.position = 39
    elif card == "You have been elected chairman of the board - pay each player $50":
        for other_player in players:
          if other_player != player:
            player.money -= 50
            other_player.money += 50
    elif card == "Your building and loan matures - collect $150":
      player.money += 150

def choose_random_ccard():
  # Create a list of the 16 cards in the community chest deck
  community_chest_cards = [
    "Advance to Go",
    "Go to Jail",
    "Get out of Jail Free",
    "Bank error in your favor - collect $200",
    "Doctor's fee - Pay $50",
    "From sale of stock you get $50",
    "Get Out of Jail Free",
    "Go to Jail",
    "Grand Opera Night - collect $50 from every player for opening night seats",
    "Holiday Fund matures - Receive $100",
    "Income tax refund - collect $20",
    "Life insurance matures - collect $100",
    "Pay hospital fees of $100",
    "Pay school fees of $150",
    "Receive $25 consultancy fee",
    "You are assessed for street repairs - $40 per house, $115 per hotel"
  ]

  # Choose a random index from 0 to 15
  index = randint(0, 15)

  # Return the card at the chosen index
  return community_chest_cards[index]


def community_chest_action(player):
  # Choose a random card from the community chest deck
  card = choose_random_ccard()

  # Perform the action for the chosen card
  if card == "Advance to Go":
    player.position = 0
    player.money += 200
  elif card == "Go to Jail":
    player.position = 10
    player.jail_time = 3
  elif card == "Get out of Jail Free":
    player.get_out_of_jail_card = True
  elif card == "Bank error in your favor - collect $200":
    player.money += 200
  elif card == "Doctor's fee - Pay $50":
    player.money -= 50
  elif card == "From sale of stock you get $50":
    player.money += 50
  elif card == "Grand Opera Night - collect $50 from every player for opening night seats":
    for other_player in players:
      if other_player != player:
        player.money += 50
        other_player.money -= 50
  elif card == "Holiday Fund matures - Receive $100":
    player.money += 100
  elif card == "Income tax refund - collect $20":
    player.money += 20
  elif card == "Life insurance matures - collect $100":
    player.money += 100
  elif card == "Pay hospital fees of $100":
    player.money -= 100
  elif card == "Pay school fees of $150":
    player.money -= 150
  elif card == "Receive $25 consultancy fee":
    player.money += 25
  elif card == "You are assessed for street repairs - $40 per house, $115 per hotel":
    houses = 0
    hotels = 0
    for property in player.properties:
      houses += property.houses
      hotels += property.hotels
    player.money -= (40 * houses + 115 * hotels)


# Define a Utility class
class Utility(Property):
  def __init__(self, name, cost, rent):
    super().__init__(name, cost, rent)

  def get_rent(self, dice_roll, num_utilities_owned):
    if num_utilities_owned == 1:
      return dice_roll * 4
    else:
      return dice_roll * 10

# Define a Railroad class
class Railroad(Property):
  def __init__(self, name, cost, rent):
    super().__init__(name, cost, rent)

  def get_rent(self, num_railroads_owned):
    return 25 * (2 ** (num_railroads_owned - 1))

# Define a Board class
class Board:
  def __init__(self, properties):
    self.properties = properties

  def get_property(self, position):
    return self.properties[position]

# Define a MonopolyGame class
class MonopolyGame:
  def __init__(self, players, board):
    self.players = players
    self.board = board

  def play(self):
    while True:
      for player in self.players:
        # Roll the dice
        dice_roll = player.roll_dice()

        # Move the player
        player.move(dice_roll)

        # Get the property at the player's new position
        property = self.board.get_property(player.position)

        # Check if the property is available to be bought
        if property.action == None:
            pass
        if property.owner is None:
          if player.decide_to_buy(property):
            player.buy_property(property)

        # Check if the property is owned by another player
        elif property.owner != player:
          player.pay_rent(property.owner, property.rent)

        # Check if the property is owned by the current player
        elif property.owner == player:
          if player.decide_to_sell(property):
            player.sell_property(property)

        # Check if the player is in jail
        if player.jail_time > 0:
          if player.use_get_out_of_jail_card() or player.decide_to_pay(50):
            player.jail_time = 0
          else:
            player.jail_time -= 1

        # Check if the player is bankrupt
        if player.money <= 0:
          self.players.remove(player)

        # Check if only one player is left
        if len(self.players) == 1:
          print(f"{self.players[0].name} wins!")
          return

# Initialize the game
# Create the properties
go              = SpecialSpace("Go", go_action)
property1       = Property("Mediterranean Avenue", 60, 2)
chest1          = SpecialSpace("Community Chest", community_chest_action)
property2       = Property("Baltic Avenue", 60, 4)
incometax       = SpecialSpace("Income Tax", income_tax_action)
railroad1       = Railroad("Reading Railroad", 200, 25)
property3       = Property("Oriental Avenue", 100, 6)
chance1         = SpecialSpace("Chance", chance_action)
property4       = Property("Vermont Avenue", 100, 6)
property5       = Property("Connecticut Avenue", 120, 8)
jail            = SpecialSpace("Jail", jail_action)
property6       = Property("St. Charles Place", 140, 10)
utility1        = SpecialUtility("Electric Company", utility_action)
property7       = Property("States Avenue", 140, 10)
property8       = Property("Virginia Avenue", 160, 12)
railroad2       = Railroad("Pennsylvania Railroad", 200, 25)
property9       = Property("St. James Place", 180, 14)
chest2          = SpecialSpace("Community Chest", community_chest_action)
property10      = Property("Tennessee Avenue", 180, 14)
property11      = Property("New York Avenue", 200, 16)
free_parking    = SpecialSpace("Free Parking", free_parking_action)
property12      = Property("Kentucky Avenue", 220, 18)
chance2         = SpecialSpace("Chance", chance_action)
property13      = Property("Indiana Avenue", 220, 18)
property14      = Property("Illinois Avenue", 240, 20)
railroad3       = Railroad("B. & O. Railroad", 200, 25)
property15      = Property("Atlantic Avenue", 260, 22)
property16      = Property("Ventnor Avenue", 260, 22)
utility2        = SpecialUtility("Water Works", utility_action)
property17      = Property("Marvin Gardens", 150, 10)
goto_jail       = SpecialSpace("Go to Jail", goto_jail_action)
property18      = Property("Pacific Avenue", 300, 26)
chest3          = SpecialSpace("Community Chest", community_chest_action)
property19      = Property("North Carolina Avenue", 300, 26)
property20      = Property("Pennsylvania Avenue", 320, 28)
railroad4       = Railroad("Short Line RR", 200, 25)
chance3         = SpecialSpace("Chance", chance_action)
property21      = Property("Park Place", 350, 35)
luxury_tax      = SpecialSpace("Luxury Tax", luxury_tax_action)
property22      = Property("Boardwalk", 400, 50)

# Create a list of properties on the board
properties = [go,
property1,
chest1,
property2,
incometax,
railroad1,
property3,
chance1,
property4,
property5,
jail,
property6,
utility1,
property7,
property8,
railroad2,
property9,
chest2,
property10,
property11,
free_parking,
property12,
chance2,
property13,
property14,
railroad3,
property15,
property16,
utility2,
property17,
goto_jail,
property18,
chest3,
property19,
property20,
railroad4,
chance3,
property21,
luxury_tax,
property22]

board = Board(properties)

# Create some players
player1 = Player("Player 1", 1000)
player2 = Player("Player 2", 1000)
player3 = Player("Player 3", 1000)
player4 = Player("Player 4", 1000)
players = [player1, player2, player3, player4]
free_parking_pot = 0


# Create a Monopoly game with the players and board
game = MonopolyGame(players, board)

# Play the game
game.play()
