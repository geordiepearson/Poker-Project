import random

"""all straight flushes, compute winner """
Values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
Suits = ('H', 'D', 'S', 'C')


class Deck:
    def __init__(self):
        self._deck = []
        for suit in Suits:
            for value in Values:
                card = (value, suit)
                self._deck.append(card)

    def get_cards(self):
        return self._deck

    def shuffle(self):
        random.shuffle(self._deck)

    def get_amount(self):
        return len(self._deck)

    def deal(self):
        if self.get_amount() == 0:
            return
        else:
            return self._deck.pop(0)


class Hands:
    def __init__(self, num_players, hand_size, board_size):
        self._hands = []
        self._board_cards = []
        self._num_players = num_players
        self._hand_size = hand_size
        self._board_size = board_size
        self._deck = Deck()
        self._deck.shuffle()

        for player in range(self._num_players):
            hand = []
            for card in range(self._hand_size):
                hand.append(self._deck.deal() + (True,))
            self._hands.append(hand)

    def get_cards(self):
        return self._hands

    def draw_board(self):
        while len(self._board_cards) < self._board_size:
            self._board_cards.append(self._deck.deal() + (False,))

    def create_hands(self):
        for player in range(self._num_players):
            self._hands[player].extend(self._board_cards)

    def sort_hands(self):
        for player in range(self._num_players):
            self._hands[player].sort(key=lambda tup: tup[0])

    def initialize_hands(self):
        self.draw_board()
        self.create_hands()
        self.sort_hands()


class PokerGame:
    def __init__(self, num_players, hand_size, board_size):
        self._num_players = num_players
        self._hand_size = hand_size
        self._board_size = board_size
        self._total_hand_size = self._hand_size + self._board_size

        self._hand = Hands(self._num_players, self._hand_size, self._board_size)
        self._hand.initialize_hands()
        self._hands = self._hand.get_cards()
        self._suit_combo = []
        self._scores = []

        self._straight_flush_flag = False
        self._four_of_kind_flag = False
        self._flush_flag = False
        self._straight_flag = False
        self._three_of_kind_flag = False
        self._pair_flag = False

        for player in range(num_players):
            self._scores.append([])

    def get_hands(self):
        return self._hands

    def iterate_value_same(self, hand, search_value):
        count = 0
        for card in range(self._total_hand_size):
            current_card = hand[card]
            if current_card[0] == search_value:
                count += 1
                if count == 2:
                    self._pair_flag = True
                elif count == 3:
                    self._three_of_kind_flag = True
                elif count == 4:
                    self._four_of_kind_flag = True

    def iterate_suit(self, hand, suit):
        count = 0
        for card in range(self._total_hand_size):
            current_card = hand[card]
            if current_card[1] == suit:
                count += 1
            if count == 5:
                self._flush_flag = True

    def iterate_sequential(self, hand, search_value, break_value):
        for card in range(self._total_hand_size):
            current_card = hand[card]

            if current_card[0] == search_value:
                if search_value == break_value:
                    self._straight_flag = True
                else:
                    self.iterate_sequential(hand, search_value - 1, break_value)

    def iterate_straight_flush(self, hand, search_value, break_value, suit):
        for card in hand:
            if (search_value, ''.join(suit)) == (card[0], card[1]):
                if search_value == break_value:
                    self._straight_flush_flag = True
                else:
                    search_value -= 1
                    self.iterate_straight_flush(hand, search_value, break_value, suit)

    def is_straight(self):
        total_results = []
        for player in range(self._num_players):
            hand = self._hands[player]
            player_results = []

            for card in range(self._total_hand_size):
                current_card = hand[card]

                if current_card[0] == 14:
                    self.iterate_sequential(hand, current_card[0], current_card[0] - 4)
                    if self._straight_flag:
                        self._straight_flag = False
                        player_results.append((current_card[0], current_card[1]))

                    else:
                        self.iterate_sequential(hand, 5, 2)
                        if self._straight_flag:
                            self._straight_flag = False
                            player_results.append((5, current_card[1]))

                else:
                    self.iterate_sequential(hand, current_card[0], current_card[0] - 4)

                    if self._straight_flag:
                        self._straight_flag = False
                        player_results.append((current_card[0], current_card[1]))

            total_results.append(player_results)
        return total_results

    def is_flush(self):
        total_results = []
        for player in range(self._num_players):
            hand = self._hands[player]
            player_results = []

            for suit in Suits:
                self.iterate_suit(hand, suit)
                if self._flush_flag:
                    self._flush_flag = False
                    player_results.append(suit)
            total_results.append(player_results)
        return total_results

    def is_straight_flush(self):
        total_results = []
        straight_results = self.is_straight()
        flush_results = self.is_flush()

        for player in range(self._num_players):
            player_results = []
            suit = flush_results[player]
            straight = straight_results[player]

            if suit != [] and straight != []:
                for card in straight:
                    if card[1] != suit[0]:
                        straight.remove(card)

                    else:
                        if card[0] == 5:
                            search_value = 5
                            break_value = 2
                            self.iterate_straight_flush(self._hands[player], search_value, break_value, suit)
                            if self._straight_flush_flag:
                                self._straight_flush_flag = False
                                player_results.append((card[0], card[1]))

                        else:
                            search_value = card[0] - 1
                            break_value = card[0] - 4

                            self.iterate_straight_flush(self._hands[player], search_value, break_value, suit)
                            if self._straight_flush_flag:
                                self._straight_flush_flag = False
                                player_results.append((card[0], card[1]))
            total_results.append(player_results)
        return total_results

    def is_of_a_kind(self):
        total_results = []
        for player in range(self._num_players):
            hand = self._hands[player]
            player_results = []

            for search_value in range(2, 15):
                self.iterate_value_same(hand, search_value)

                if self._four_of_kind_flag:
                    self._four_of_kind_flag = False
                    self._three_of_kind_flag = False
                    self._pair_flag = False
                    player_results.append((4, search_value))

                elif self._three_of_kind_flag and not self._four_of_kind_flag:
                    self._three_of_kind_flag = False
                    self._pair_flag = False
                    player_results.append((3, search_value))

                elif self._pair_flag and not (self._four_of_kind_flag and self._three_of_kind_flag):
                    self._pair_flag = False
                    player_results.append((2, search_value))
            player_results = list(dict.fromkeys(player_results))
            total_results.append(player_results)
        return total_results

    def is_high(self):
        total_results = []
        for player in range(self._num_players):
            hand = self._hands[player]
            player_results = []
            highest_card = hand[0]

            for card in range(self._total_hand_size):
                current_card = hand[card]
                if current_card[0] > highest_card[0]:
                    highest_card = current_card
            player_results.append(highest_card[0])
            total_results.append(player_results)
        return total_results

    def compute_results(self):
        print('Straight_Flushes: ' + str((self.is_straight_flush())))
        print('Straights: ' + str(self.is_straight()))
        print('Flushes: ' + str(self.is_flush()))
        print('Of A Kinds: ' + str(self.is_of_a_kind()))
        print('Highcards: ' + str(self.is_high()))

        straight_flush_results = self.is_straight_flush()
        straight_results = self.is_straight()
        flush_results = self.is_flush()
        of_a_kind_results = self.is_of_a_kind()
        high_card_results = self.is_high()

def main():
    game = PokerGame(2, 2, 5)
    print(game.get_hands())
    game.compute_results()


if __name__ == '__main__':
    main()