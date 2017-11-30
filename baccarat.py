import random

SUITS = ['hearts', 'spades', 'clubs', 'diamonds']
RANKS = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king']

class Card:
    """Playing card to be used to fill a baccarat shoe and
    to be drawn to a playing hand.

    Args:
        rank: int or string, the rank of the card.
        suit: string, the suit of the card.

    Attributes:
        value: int, baccarat value of the card.
        rank: int or string, the rank of the card.
        suit: string, the suit of the card.

    Raises:
        ValueError: On invalid card rank or suit.
    """
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError('Invalid card rank.')
        if suit not in SUITS:
            raise ValueError('Invalid card suit.')
        self._rank = rank
        self._suit = suit

    @property
    def value(self):
        """Returns the value of the card according to 
        baccarat rules.
        """
        if self._rank in range(2, 10):
            return self._rank
        elif self._rank == 'ace':
            return 1
        else:
            return 0

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    def __add__(self, other):
        return (self.value + other) % 10

    __radd__ = __add__

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        if isinstance(self._rank, str):
            return f'Card(\'{self._rank}\', \'{self._suit}\')'
        elif isinstance(self._rank, int):
            return f'Card({self._rank}, \'{self._suit}\')'
            

    def __str__(self):
        """Return a string with the rank and suit of the card."""
        return f'{self._rank} of {self._suit}'

class Shoe:
    """Shoe with num_decks shuffled decks. All cards used in the game
    will be drawn from this set.

    Args:
        num_decks: int, number of decks on the shoe.

    Attributes:
        num_decks: int, number of decks on the shoe.
        cards: list, all the instances of the object PlayinCard
            on the Shoe object.

    Raises:
        TypeError: If the num_decks is not an integer.
        ValueError: If the num_decks is not positive.
    """
    def __init__(self, num_decks):
        if not isinstance(num_decks, int):
            raise TypeError('Number of decks must be an integer.')
        elif num_decks < 1:
            raise ValueError('Number of decks must be positive.')
        self._num_decks = num_decks
        self.add_decks()

    @property
    def num_decks(self):
        return self._num_decks

    @property
    def cards(self):
        return self._cards

    def add_decks(self):
        """Refils the shoe with num_decks decks."""
        self._cards = []
        for i in range(self._num_decks):
            for suit in SUITS:
                for rank in RANKS:
                   self._cards.append(Card(rank, suit)) 
        random.shuffle(self._cards)

    def draw_cards(self, num_cards):
        """Draws cards from shoe. Refills the shoe when
        it is empty.

        Args:
            num_cards: int, number of cards to be drawn.

        Returns:
            cards_drawn: list, cards drawn from shoe.
        """
        cards_drawn = []
        for i in range(num_cards):
            if len(self._cards) == 0:
                self.add_decks()
                print('Refilling shoe...')
            cards_drawn.append(self._cards.pop())
        return cards_drawn

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        return f'Shoe({self._num_decks})'

    def __str__(self):
        """Returns a string with the number of decks and the
        number of cards left.
        """
        return f'{self._num_decks} decks shoe. {len(self._cards)} cards left.'

class Hand:
    """A hand of cards to be played. Either from the bank or the player.

    Args:
        cards: list, a list of card objects to be added to the hand
            using the add_cards() method.

    Atributes:
        cards: list, a list of card type objects.
        value: int, the sum of the individual card values according to
            baccarat rules.
    """
    def __init__(self, cards):
        self._cards = []
        self.add_cards(cards)

    @property
    def cards(self):
        return self._cards

    @property
    def value(self):
        return sum(self._cards)

    def add_cards(self, cards):
        """Add cards to the hand object.

        Args:
            cards: list, a list of card type objects

        Raises:
            TypeError: when a object different from card is present on the list
                used as argument to the add_card() method.
        """
        try:
            for card in cards:
                assert isinstance(card, Card)
                self._cards.append(card)
        except AssertionError:
            raise TypeError('Not a valid Card type')

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance.
        """
        return f'Hand({self._cards})'

    def __str__(self):
        """Return a string with all the cards on the hand."""
        return ', '.join([card.__str__() for card in self._cards])

class Player(Hand):
    def __init__(self, cards):
        Hand.__init__(self, cards)

    def third_card(self):
        if 0 <= self.value <= 5:
            return True
        return False

class Bank(Hand):
    def __init__(self, cards):
        Hand.__init__(self, cards)

    def third_card(self, player_third_card=None):

        third_card_rules = {3: [0, 1, 2, 3, 4, 5, 6, 7, 9],
                            4: [2, 3, 4, 5, 6, 7],
                            5: [4, 5, 6, 7],
                            6: [6, 7]}

        if len(self._cards) == 2:
            if player_third_card:
                try:
                    assert isinstance(player_third_card, Card)
                    if 0 <= self.value <= 2:
                        return True
                    elif player_third_card.value in third_card_rules[self.value]:
                        return True
                except AssertionError:
                    raise TypeError('Player third card not a Card type object.')
                except KeyError:
                    return False
                return False
            else:
                if 0 <= self.value <= 5:
                    return True
        return False
