import numpy as np

class Card(object):
    '''
    Card stores the suit and rank of a single card
    Note:
        The suit variable in a standard card game should be one of [S, H, D, C, BJ, RJ] meaning [Spades, Hearts, Diamonds, Clubs, Black Joker, Red Joker]
        Similarly the rank variable should be one of [A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K]
    '''

    suit = None
    rank = None
    valid_suit = ['S', 'H', 'D', 'C', 'BJ', 'RJ']
    valid_rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    def __init__(self, suit, rank):
        ''' Initialize the suit and rank of a card
        Args:
            suit: string, suit of the card, should be one of valid_suit
            rank: string, rank of the card, should be one of valid_rank
        '''
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            # don't attempt to compare against unrelated types
            return NotImplemented

    def __hash__(self):
        suit_index = Card.valid_suit.index(self.suit)
        rank_index = Card.valid_rank.index(self.rank)
        return rank_index + 100 * suit_index

    def __str__(self):
        ''' Get string representation of a card.
        Returns:
            string: the combination of rank and suit of a card. Eg: AS, 5H, JD, 3C, ...
        '''
        return self.rank + self.suit

    def get_index(self):
        ''' Get index of a card.
        Returns:
            string: the combination of suit and rank of a card. Eg: 1S, 2H, AD, BJ, RJ...
        '''
        return self.suit+self.rank

def init_standard_deck():
    ''' Initialize a standard deck of 52 cards
    Returns:
        (list): A list of Card object
    '''
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    res = [Card(suit, rank) for suit in suit_list for rank in rank_list]
    return res

def get_random_cards(cards, num, np_random=None):
    ''' Randomly get a number of chosen cards out of a list of cards
    Args:
        cards (list): List of Card object
        num (int): The  number of cards to be chosen
    Returns:
        (list): A list of chosen cards
        (list): A list of remained cards
    '''
    if not np_random:
        np_random = np.random.RandomState()
    if not num> 0:
        raise AssertionError('Invalid input number')
    if not num <= len(cards):
        raise AssertionError('Input number larger than length of cards')
    remained_cards = []
    chosen_cards = []
    remained_cards = cards.copy()
    np_random.shuffle(remained_cards)
    chosen_cards = remained_cards[:num]
    remained_cards = remained_cards[num:]
    return chosen_cards, remained_cards

def print_card(cards):
    ''' Nicely print a card or list of cards
    Args:
        card (string or list): The card(s) to be printed
    '''
    if cards is None:
        cards = [None]
    if isinstance(cards, str):
        cards = [cards]

    lines = [[] for _ in range(9)]

    for card in cards:
        if card is None:
            lines[0].append('┌─────────┐')
            lines[1].append('│░░░░░░░░░│')
            lines[2].append('│░░░░░░░░░│')
            lines[3].append('│░░░░░░░░░│')
            lines[4].append('│░░░░░░░░░│')
            lines[5].append('│░░░░░░░░░│')
            lines[6].append('│░░░░░░░░░│')
            lines[7].append('│░░░░░░░░░│')
            lines[8].append('└─────────┘')
        else:
            elegent_card = elegent_form(card)
            suit = elegent_card[0]
            rank = elegent_card[1]
            if len(elegent_card) == 3:
                space = elegent_card[2]
            else:
                space = ' '

            lines[0].append('┌─────────┐')
            lines[1].append('│{}{}       │'.format(rank, space))
            lines[2].append('│         │')
            lines[3].append('│         │')
            lines[4].append('│    {}    │'.format(suit))
            lines[5].append('│         │')
            lines[6].append('│         │')
            lines[7].append('│       {}{}│'.format(space, rank))
            lines[8].append('└─────────┘')

    for line in lines:
        print ('   '.join(line))


def elegent_form(card):
    ''' Get a elegent form of a card string
    Args:
        card (string): A card string
    Returns:
        elegent_card (string): A nice form of card
    '''
    suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣','s': '♠', 'h': '♥', 'd': '♦', 'c': '♣' }
    rank = '10' if card[1] == 'T' else card[1]

    return suits[card[0]] + rank

def Card_Rank(card_hand):
    # Function assumes sorded rank card_hand

    cards =[]
    for card in card_hand:
        cards.append((CF_I[card.get_index()[1]], CC_I[card.get_index()[0]] ))


    # Possible multi Figures or colors
    c_fig = [[] for _ in range(13)]
    c_col = [[] for _ in range(4)]
    for c in cards:
            c_fig[c[0]].append(c)
            c_col[c[1]].append(c)

    n_fig = [len(f) for f in c_fig]

     # search for flush
    col_cards = None
    colour = None
    for cL in c_col:
        if len(cL) > 4:
            col_cards = cL
            colour = cL[0][1]
            break

    sc_fig = c_fig[-1:] + c_fig # with aces at the beginning
    in_row = []
    pix = -2
    for ix in range(14):
        if len(sc_fig[ix]):
            # select card
            crd = sc_fig[ix][0]
            if len(sc_fig[ix]) > 1 and colour:
                for c in sc_fig[ix]:
                    if c[1] == colour:
                        crd = c
                        break
            if pix + 1 == ix:
                in_row.append(crd)
            else:
                if len(in_row) in [3,4]: break # no chance anymore
                if len(in_row) in [0,1,2]: in_row = [crd] # still a chance
                else: break # got 5
            pix = ix
    possible_straight = len(in_row) > 4

    # straightFlush case check
    col_in_row = []
    possible_straight_flush = False
    if possible_straight and col_cards:

        # remove from row cards out of colour
        col_in_row = [] + in_row
        to_delete = []
        for c in col_in_row:
            if c[1] != colour: to_delete.append(c)
        for c in to_delete: col_in_row.remove(c) # after this col may be not in row (may be split)

        if len(col_in_row) > 4:
            possible_straight_flush = True # assume true

            splitIX = [] # indexes of split from
            for ix in range(1,len(col_in_row)):
                if col_in_row[ix-1][0]+1 != col_in_row[ix][0]: splitIX.append(ix)

            if splitIX:
                if len(col_in_row)<6 or len(splitIX)>1: possible_straight_flush = False # any split gives possibility for SF only for 6 cards (7 with one removed from inside/notEdge/ gives 6 with split) with one split
                else:
                    if splitIX[0] not in [1,5]: possible_straight_flush = False
                    else:
                        ixF = 0
                        ixT = 5
                        if splitIX[0]==1:
                            ixF = 1
                            ixT = 6
                        col_in_row = col_in_row[ixF:ixT]

            if len(col_in_row) > 5: col_in_row = col_in_row[len(col_in_row)-5:] # trim

    if possible_straight_flush:                             top_rank = 8 # straight flush
    elif 4 in n_fig:                                        top_rank = 7 # four of
    elif (3 in n_fig and 2 in n_fig) or n_fig.count(3) > 1: top_rank = 6 # full house
    elif col_cards:                                         top_rank = 5 # flush
    elif possible_straight:                                 top_rank = 4 # straight
    elif 3 in n_fig:                                        top_rank = 3 # three of
    elif n_fig.count(2) > 1:                                top_rank = 2 # two pairs
    elif 2 in n_fig:                                        top_rank = 1 # pair
    else:                                                   top_rank = 0 # high card

    # find five cards
    five_cards = []
    if top_rank == 8: five_cards = col_in_row
    if top_rank == 7:
        four = []
        for cL in c_fig:
            if len(cL) == 4:
                four = cL
                break
        for c in four: cards.remove(c)
        five_cards = [cards[-1]] + four
    if top_rank == 6:
        five_cards = []
        for cL in c_fig:
            if len(cL) == 2: five_cards += cL
        for cL in c_fig:
            if len(cL) == 3: five_cards += cL
        five_cards = five_cards[-5:]
    if top_rank == 5:
        if len(col_cards) > 5: col_cards = col_cards[len(col_cards)-5:]
        five_cards = col_cards
    if top_rank == 4:
        if len(in_row) > 5: in_row = in_row[len(in_row)-5:]
        five_cards = in_row
    if top_rank == 3:
        three = []
        for cL in c_fig:
            if len(cL) == 3: three = cL
        for c in three: cards.remove(c)
        five_cards = cards[-2:] + three
    if top_rank == 2:
        two2 = []
        for cL in c_fig:
            if len(cL) == 2: two2 += cL
        if len(two2) > 4: two2 = two2[len(two2)-4:]
        for c in two2: cards.remove(c)
        five_cards = cards[-1:] + two2
    if top_rank == 1:
        two = []
        for cL in c_fig:
            if len(cL) == 2: two = cL
        for c in two: cards.remove(c)
        five_cards = cards[-3:] + two
    if top_rank == 0:
        five_cards = cards[-5:]

    five_str = []
    for a_card in five_cards:
        five_str.append(str(CRD_COL[a_card[1]]) + str(CRD_FIG[a_card[0]]))

    original_hand, seven_str = convert(card_hand)

    return top_rank, five_cards, five_str, original_hand, seven_str

def convert(card_hand):
    cards =[]
    for card in card_hand:
        cards.append((CF_I[card.get_index()[1]], CC_I[card.get_index()[0]] ))

    seven_str = []
    for a_card in cards:
        seven_str.append(str(CRD_COL[a_card[1]]) + str(CRD_FIG[a_card[0]]))
    return cards, seven_str
# card figures
CRD_FIG = {
    0:      '2',
    1:      '3',
    2:      '4',
    3:      '5',
    4:      '6',
    5:      '7',
    6:      '8',
    7:      '9',
    8:      'T',
    9:      'J',
    10:     'Q',
    11:     'K',
    12:     'A'}

# inverted card figures
CF_I = {
    '2':     0,
    '3':     1,
    '4':     2,
    '5':     3,
    '6':     4,
    '7':     5,
    '8':     6,
    '9':     7,
    'T':     8,
    'J':     9,
    'Q':     10,
    'K':     11,
    'A':     12}

# card colors
CRD_COL = {
    0:      'S',
    1:      'H',
    2:      'D',
    3:      'C'}

# inverted card colors
CC_I = {
    'S':    0,
    'H':    1,
    'D':    2,
    'C':    3}

# probabilities for each hand
C_Rank_Prob = {
    0:      0.501177,
    1:      0.422569,
    2:      0.047539,
    3:      0.021128,
    4:      0.003925,
    5:      0.001965,
    6:      0.001441,
    7:      0.000240,
    8:      0.000015}
