
# import statements
from random import shuffle

# import statements
from random import shuffle


# Function: get_user_input
def get_user_input(question):
    """Prompt the user with the given question and process the input."""
    while True:
        user_input = input(question).strip()
        if len(user_input) == 0:
            continue
        if user_input.isdigit():
            return int(user_input)
        return user_input.upper() if user_input.isalpha() else user_input.lower()


# Function: setup_water_cards
def setup_water_cards():
    """Create a shuffled list of water cards with specified values and quantities."""
    water_cards = [1] * 30 + [5] * 15 + [10] * 8
    shuffle(water_cards)
    return water_cards


# Function: setup_power_cards
def setup_power_cards():
    """Create a shuffled list of power cards with specified values and quantities."""
    power_cards = ['SOH'] * 10 + ['DOT'] * 2 + ['DMT'] * 3
    shuffle(power_cards)
    return power_cards


# Function: setup_cards
def setup_cards():
    """Set up both the water card and power card piles."""
    water_cards_pile = setup_water_cards()
    power_cards_pile = setup_power_cards()
    return (water_cards_pile, power_cards_pile)


# Function: get_card_from_pile
def get_card_from_pile(pile, index):
    """Remove and return the card at the specified index from the pile."""
    return pile.pop(index)


# Function: arrange_cards
def arrange_cards(cards_list):
    """Arrange the player's cards: water cards sorted first, followed by sorted power cards."""
    water_cards = sorted([card for card in cards_list if isinstance(card, int)])
    power_cards = sorted([card for card in cards_list if isinstance(card, str)])
    cards_list[:] = water_cards + power_cards


# Function: deal_cards
def deal_cards(water_cards_pile, power_cards_pile):
    """Deal cards to player 1 and player 2."""
    player_1_cards = []
    player_2_cards = []

    for i in range(3):
        player_1_cards.append(get_card_from_pile(water_cards_pile, 0))
        player_2_cards.append(get_card_from_pile(water_cards_pile, 0))
    for i in range(2):
        player_1_cards.append(get_card_from_pile(power_cards_pile, 0))
        player_2_cards.append(get_card_from_pile(power_cards_pile, 0))

    arrange_cards(player_1_cards)
    arrange_cards(player_2_cards)

    return (player_1_cards, player_2_cards)


# Function: apply_overflow
def apply_overflow(tank_level):
    """Apply overflow if necessary, adjusting tank level according to the rules."""
    MAX_TANK = 80
    if tank_level > MAX_TANK:
        overflow = tank_level - MAX_TANK
        tank_level = MAX_TANK - overflow
    return tank_level


# Function: use_card
def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    """Use a card, update tank levels, and handle overflow."""
    player_cards.remove(card_to_use)

    if isinstance(card_to_use, int):  # Water card
        player_tank += card_to_use
    elif card_to_use == 'SOH':  # Steal Opponent's Half
        stolen_water = opponent_tank // 2
        player_tank += stolen_water
        opponent_tank -= stolen_water
    elif card_to_use == 'DOT':  # Drain Opponent's Tank
        opponent_tank = 0
    elif card_to_use == 'DMT':  # Double My Tank
        player_tank *= 2

    player_tank = apply_overflow(player_tank)
    return (player_tank, opponent_tank)


# Function: discard_card
def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    """Discard a card and return it to the bottom of the appropriate pile."""
    player_cards.remove(card_to_discard)
    if isinstance(card_to_discard, int):  # Water card
        water_cards_pile.append(card_to_discard)
    else:  # Power card
        power_cards_pile.append(card_to_discard)


# Function: filled_tank
def filled_tank(tank):
    """Check if the tank level is between the minimum and maximum fill values."""
    return 75 <= tank <= 80


# Function: check_pile
def check_pile(pile, pile_type):
    """Check if a pile is empty and replenish it if necessary."""
    if not pile:
        if pile_type == 'water':
            pile.extend(setup_water_cards())
        elif pile_type == 'power':
            pile.extend(setup_power_cards())


# Function: human_play
def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """Simulate the human player's turn."""
    print(f"Your tank: {human_tank}, Computer's tank: {opponent_tank}")
    print(f"Your cards: {human_cards}")

    action = get_user_input("Do you want to 'use' or 'discard' a card? ")
    card = None

    while True:
        card = get_user_input(f"Enter the card to {action}: ")
        if card in human_cards:
            break
        print("Invalid card. Try again.")

    if action == 'use':
        human_tank, opponent_tank = use_card(human_tank, card, human_cards, opponent_tank)
    else:
        discard_card(card, human_cards, water_cards_pile, power_cards_pile)

    # Draw a new card from the corresponding pile
    if isinstance(card, int):
        check_pile(water_cards_pile, 'water')
        new_card = get_card_from_pile(water_cards_pile, 0)
    else:
        check_pile(power_cards_pile, 'power')
        new_card = get_card_from_pile(power_cards_pile, 0)

    human_cards.append(new_card)
    arrange_cards(human_cards)

    return (human_tank, opponent_tank)


# Function: computer_play
def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """Simulate the computer's turn."""
    # Strategy: If close to winning, use the most efficient water card. Use power cards wisely.
    card = None

    # Computer uses a water card if it is close to 75-80
    water_cards = [card for card in computer_cards if isinstance(card, int)]
    if water_cards:
        total_water = computer_tank + max(water_cards)
        if 75 <= total_water <= 80:
            card = max(water_cards)  # Best water card to win
        else:
            card = min(water_cards)  # Use smallest water card to avoid overflow

    # Otherwise, use a power card if beneficial
    power_cards = [card for card in computer_cards if isinstance(card, str)]
    if not card and power_cards:
        if 'DOT' in power_cards and opponent_tank > 0:
            card = 'DOT'
        elif 'SOH' in power_cards and opponent_tank > 0:
            card = 'SOH'
        elif 'DMT' in power_cards:
            card = 'DMT'

    # If no useful power card, discard a water card
    if not card:
        card = min(computer_cards)  # Discard smallest card

    if card in water_cards:
        computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)
    else:
        discard_card(card, computer_cards, water_cards_pile, power_cards_pile)

    # Draw a new card from the corresponding pile
    if isinstance(card, int):
        check_pile(water_cards_pile, 'water')
        new_card = get_card_from_pile(water_cards_pile, 0)
    else:
        check_pile(power_cards_pile, 'power')
        new_card = get_card_from_pile(power_cards_pile, 0)

    computer_cards.append(new_card)
    arrange_cards(computer_cards)

    print(f"Computer used/discarded: {card}")

    return (computer_tank, opponent_tank)


# Main game loop
def main():
    """Main function to run the game."""
    water_cards_pile, power_cards_pile = setup_cards()
    human_tank = computer_tank = 0

    # Deal cards to both players
    human_cards, computer_cards = deal_cards(water_cards_pile, power_cards_pile)

    # Choose a random player to go first
    from random import choice
    current_player = choice(['human', 'computer'])

    # Game loop
    while not (filled_tank(human_tank) or filled_tank(computer_tank)):
        if current_player == 'human':
            human_tank, computer_tank = human_play(human_tank, human_cards, water_cards_pile, power_cards_pile,
                                                   computer_tank)
            current_player = 'computer'
        else:
            computer_tank, human_tank = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile,
                                                      human_tank)
            current_player = 'human'

        # Display the tank levels
        print(f"\nHuman Tank: {human_tank}, Computer Tank: {computer_tank}\n")

    # Announce the winner
    if filled_tank(human_tank):
        print("Congratulations! You filled your tank first and won the game!")
    else:
        print("The computer won by filling its tank first!")


if __name__ == "__main__":
    main()
