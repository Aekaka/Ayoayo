class Player:
    """Just a simple way to remember a player's name."""
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

class Ayoayo:
    """
    This is where the main Ayoayo game happens.
    It keeps track of the board, players, and how the game is played.
    """
    def __init__(self):
        # Board setup: 6 pits for each player, plus a store for each.
        # Player 1: pits 0-5, store 6
        # Player 2: pits 7-12, store 13
        # Starts with 4 seeds in each pit.
        self._board = [4] * 6 + [0] + [4] * 6 + [0]
        self._players = []
        self._current_player_turn_index = 0 # Player 1 (index 0) starts
        self._game_over = False
        self._winner_message = "Game has not ended"
        self._extra_turn_message = "" # For messages like "player X take another turn"

    def _get_player_details(self, player_1_based_idx: int):
        """Little helper to figure out which pits and store belong to a player."""
        if player_1_based_idx == 1:
            return list(range(0, 6)), 6 # P1's pits, P1's store
        else:
            return list(range(7, 13)), 13 # P2's pits, P2's store

    def _is_side_empty(self, player_1_based_idx: int) -> bool:
        """Checks if a player has any seeds left in their pits."""
        pit_indices, _ = self._get_player_details(player_1_based_idx)
        return all(self._board[pit_idx] == 0 for pit_idx in pit_indices)

    def _collect_remaining_seeds_at_game_end(self):
        """
        When the game ends because one player's pits are empty,
        the other player gets to collect all seeds from their own pits.
        """
        if self._is_side_empty(1): # If P1's side is empty
            p2_pits, p2_store = self._get_player_details(2)
            for pit_idx in p2_pits:
                self._board[p2_store] += self._board[pit_idx]
                self._board[pit_idx] = 0
        elif self._is_side_empty(2): # If P2's side is empty
            p1_pits, p1_store = self._get_player_details(1)
            for pit_idx in p1_pits:
                self._board[p1_store] += self._board[pit_idx]
                self._board[pit_idx] = 0

    def _check_game_end_conditions(self):
        """
        Sees if the game is over and figures out who won.
        Game ends if a player's side is totally empty.
        """
        if self._is_side_empty(1) or self._is_side_empty(2):
            if not self._game_over: # Only process end game once
                self._game_over = True
                self._collect_remaining_seeds_at_game_end()

                p1_score = self._board[6]
                p2_score = self._board[13]

                if p1_score > p2_score:
                    self._winner_message = f"Winner is player 1: {self._players[0].get_name()}"
                elif p2_score > p1_score:
                    self._winner_message = f"Winner is player 2: {self._players[1].get_name()}"
                else:
                    self._winner_message = "It's a tie"
        return self._game_over

    def createPlayer(self, player_name: str) -> Player:
        """Lets us add players to the game."""
        if len(self._players) < 2:
            player = Player(player_name)
            self._players.append(player)
            return player
        return None # Max 2 players

    def printBoard(self):
        """Shows what the board looks like in the console."""
        if len(self._players) < 2:
            print("Need two players to show the board properly!")
            return

        # Player 2 (top)
        print(f"\n{self._players[1].get_name()} (Player 2):")
        print(f" Pits: {list(self._board[i] for i in self._get_player_details(2)[0])}")
        print(f" Store: {self._board[self._get_player_details(2)[1]]}")
        
        # Player 1 (bottom)
        print(f"{self._players[0].get_name()} (Player 1):")
        print(f" Pits: {list(self._board[i] for i in self._get_player_details(1)[0])}")
        print(f" Store: {self._board[self._get_player_details(1)[1]]}")
        print("-" * 20)

    def returnWinner(self) -> str:
        """Tells us who won, or if the game is still going."""
        # Make sure to check end conditions if not already flagged
        if not self._game_over:
            # Game can end if current player has no moves
            if self._is_side_empty(self._current_player_turn_index + 1):
                self._check_game_end_conditions()

        return self._winner_message if self._game_over else "Game has not ended"

    def playGame(self, player_1_based_idx: int, pit_1_to_6_idx: int) -> str:
        """This is where a player makes their move."""
        self._extra_turn_message = "" # Reset message each turn

        if self._game_over:
            return "Game is ended"

        # The assignment allows not enforcing strict turns for testing.
        # For actual play, ensure player_1_based_idx matches self._current_player_turn_index + 1.
        self._current_player_turn_index = player_1_based_idx - 1

        if not (1 <= pit_1_to_6_idx <= 6):
            return "Invalid number for pit index" # As per assignment PDF

        player_pit_indices, player_store_idx = self._get_player_details(player_1_based_idx)
        actual_board_pit_idx = player_pit_indices[pit_1_to_6_idx - 1] # Convert 1-6 to 0-5 for list index

        if self._board[actual_board_pit_idx] == 0:
            return "Chosen pit is empty. Please select a pit with seeds."

        seeds_in_hand = self._board[actual_board_pit_idx]
        self._board[actual_board_pit_idx] = 0 # Pick up all seeds
        
        current_sow_pit_idx = actual_board_pit_idx
        
        # Sowing seeds one by one, counter-clockwise
        for _ in range(seeds_in_hand):
            current_sow_pit_idx = (current_sow_pit_idx + 1) % 14 # Move to the next spot (12 pits + 2 stores)
            
            # Skip opponent's store
            opponent_store_idx = 13 if player_1_based_idx == 1 else 6
            if current_sow_pit_idx == opponent_store_idx:
                current_sow_pit_idx = (current_sow_pit_idx + 1) % 14 # Skip it and move again
            
            self._board[current_sow_pit_idx] += 1 # Drop a seed
        
        final_landing_pit_idx = current_sow_pit_idx
        earned_extra_turn = False

        # Special Rule 1: Extra turn if last seed lands in own store
        if final_landing_pit_idx == player_store_idx:
            earned_extra_turn = True
            self._extra_turn_message = f"player {player_1_based_idx} take another turn"

        # Special Rule 2: Capture seeds
        # This happens if the last seed lands in an empty pit on the player's own side.
        # (And an extra turn wasn't earned by landing in the store)
        elif final_landing_pit_idx in player_pit_indices and self._board[final_landing_pit_idx] == 1:
            # The pit was empty before this seed landed, making its count 1.
            
            opposite_pit_idx = -1
            if player_1_based_idx == 1: # Player 1 (pits 0-5 on board)
                # Example: P1's pit 0 is opposite P2's pit 12 (board index)
                opposite_pit_idx = (5 - final_landing_pit_idx) + 7
            else: # Player 2 (pits 7-12 on board)
                # Example: P2's pit 7 (their first) is opposite P1's pit 5 (board index)
                relative_idx_p2 = final_landing_pit_idx - 7 # Convert P2's board index to 0-5 range
                opposite_pit_idx = 5 - relative_idx_p2
            
            # If opponent's opposite pit has seeds, capture them
            if self._board[opposite_pit_idx] > 0:
                captured_seeds = self._board[opposite_pit_idx]
                self._board[opposite_pit_idx] = 0 # Empty opponent's pit
                
                # Add captured seeds and the triggering seed to player's store
                self._board[player_store_idx] += captured_seeds
                self._board[player_store_idx] += self._board[final_landing_pit_idx] # This is the 1 triggering seed
                self._board[final_landing_pit_idx] = 0 # Empty the triggering pit

        # Switch player if no extra turn was earned
        if not earned_extra_turn:
            self._current_player_turn_index = 1 - self._current_player_turn_index # Flips between 0 and 1

        # Check if the game ended after this move
        if self._check_game_end_conditions():
            # If game ended, `_winner_message` is set.
            # `playGame` still returns the board state as per assignment examples.
            pass 
        
        # Return the board state as a list of numbers (as a string, like in the PDF example output)
        return str(self._board[0:7] + self._board[7:14])
    
    def get_extra_turn_message(self) -> str:
        """Just a way for the Streamlit app to see if an extra turn message was set."""
        return self._extra_turn_message
