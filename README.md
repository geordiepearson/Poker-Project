# Poker-Project
An application that generates poker hands for the chosen number of players and hand length. It then evaluates all the poker combinations 
that each player has and prints them.

Input variables:

  - Number of Players: int
  - Number of Cards in Players Hand: int
  - Number of Cards on Board: int

Outputs 5 arrays to denote the various types of results. Each of these arrays contain an array for each players results. Within these 
secondary arrays data is stored based upon the type of results: 
  - Straight Flushes: Stored as a tuple in form (card_value(int),card_suit(str))
  - Straights:Stored as a tuple in form (card_value(int),card_suit(str))
  - Flushes:Stores flush of suit in form card_suit(str) 
  - Of a Kinds:Stored as a tuple in form (number_of_cards(int, eg. pair, triplet, quartet), card_value(int))
  - Highcard:Stores highest card in form card_value(int)
