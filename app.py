import streamlit as st
from ayoayo import Ayoayo # Our game logic

st.set_page_config(page_title="Ayoayo Game", layout="wide")

def init_game():
    """Sets up a new game or resets the current one."""
    st.session_state.game = Ayoayo()
    st.session_state.players_created = False
    st.session_state.player_names = ["Player 1", "Player 2"] # Defaults
    st.session_state.game_log = []
    st.session_state.last_action_message = "" # For "extra turn" or errors

if 'game' not in st.session_state:
    init_game()

game = st.session_state.game

# --- Player Name Setup ---
if not st.session_state.players_created:
    st.header("👥 Who's Playing?")
    with st.form("player_form"):
        p1_name_input = st.text_input("Player 1 Name:", st.session_state.player_names[0])
        p2_name_input = st.text_input("Player 2 Name:", st.session_state.player_names[1])
        start_button = st.form_submit_button("Start Game!")

        if start_button:
            if p1_name_input and p2_name_input:
                st.session_state.player_names = [p1_name_input, p2_name_input]
                game.createPlayer(p1_name_input)
                game.createPlayer(p2_name_input)
                st.session_state.players_created = True
                st.session_state.game_log.append(f"Game started: {p1_name_input} vs {p2_name_input}.")
                st.experimental_rerun() # Refresh to show game board
            else:
                st.error("Please give both players a name.")
else:
    # --- Main Game Area ---
    p1_name, p2_name = st.session_state.player_names
    current_player_idx_0_based = game._current_player_turn_index
    current_player_name = st.session_state.player_names[current_player_idx_0_based]

    st.title(f"🪨 Ayoayo: {p1_name} vs {p2_name} 🪨")

    if st.session_state.last_action_message:
        st.info(st.session_state.last_action_message)

    # Displaying the board
    # Player 2 (Top)
    st.markdown(f"<h4 style='text-align: center;'>{p2_name}'s Pits (Player 2)</h4>", unsafe_allow_html=True)
    p2_pits_indices, p2_store_idx = game._get_player_details(2)
    cols_p2_pits = st.columns(6)
    for i, board_idx in enumerate(reversed(p2_pits_indices)): # Show P2's pits right-to-left
        cols_p2_pits[i].button(
            f"{game._board[board_idx]}", 
            key=f"p2_pit_display_{5-i}", 
            disabled=True, # Just for display
            use_container_width=True
        )
    
    # Stores and Game Status
    col_p1_store, col_status, col_p2_store = st.columns([2,3,2])
    with col_p1_store:
        st.metric(label=f"{p1_name}'s Store", value=game._board[game._get_player_details(1)[1]])
    with col_status:
        winner_status_msg = game.returnWinner()
        if game._game_over:
            st.success(f"🏆 Game Over! {winner_status_msg} 🏆")
        else:
            st.subheader(f"It's {current_player_name}'s turn!")
    with col_p2_store:
        st.metric(label=f"{p2_name}'s Store", value=game._board[p2_store_idx])
    
    # Player 1 (Bottom)
    st.markdown(f"<h4 style='text-align: center;'>{p1_name}'s Pits (Player 1)</h4>", unsafe_allow_html=True)
    p1_pits_indices, _ = game._get_player_details(1)
    cols_p1_pits = st.columns(6)
    for i, board_idx in enumerate(p1_pits_indices):
        cols_p1_pits[i].button(
            f"{game._board[board_idx]}",
            key=f"p1_pit_display_{i}",
            disabled=True, # Just for display
            use_container_width=True
        )
    st.markdown("---")

    # Player Action Area
    if not game._game_over:
        active_player_1_based_idx = current_player_idx_0_based + 1
        
        player_pits, _ = game._get_player_details(active_player_1_based_idx)
        available_moves_options = [] # (Display text, pit_index_1_to_6)
        for i in range(6):
            pit_board_idx = player_pits[i]
            if game._board[pit_board_idx] > 0: # Can only play non-empty pits
                available_moves_options.append(
                    (f"Pit {i+1} ({game._board[pit_board_idx]} seeds)", i + 1)
                )

        if not available_moves_options:
            st.warning(f"{current_player_name} has no moves! The game might end here.")
            # The game logic (returnWinner) will handle determining if this ends the game.
        else:
            selected_move_tuple = st.selectbox(
                f"{current_player_name}, choose a pit to play:",
                options=available_moves_options,
                format_func=lambda x: x[0] # Show only the display text
            )

            if st.button(f"Play Pit for {current_player_name}", disabled=not selected_move_tuple):
                if selected_move_tuple:
                    chosen_pit_1_idx = selected_move_tuple[1]
                    board_state_str = game.playGame(active_player_1_based_idx, chosen_pit_1_idx)
                    
                    st.session_state.last_action_message = game.get_extra_turn_message()
                    if not st.session_state.last_action_message and "empty" in board_state_str.lower(): # Crude check for error from playGame
                        st.session_state.last_action_message = board_state_str
                    
                    st.session_state.game_log.append(
                        f"{current_player_name} played pit {chosen_pit_1_idx}."
                    )
                    if game.get_extra_turn_message():
                         st.session_state.game_log.append(game.get_extra_turn_message())
                    
                    st.experimental_rerun()
    else: # Game is over
        if st.button("🔄 Play Again?"):
            init_game()
            st.experimental_rerun()

    # Game Log in Sidebar
    st.sidebar.header("📜 Game Log")
    st.sidebar.markdown(f"**Player 1:** {p1_name}")
    st.sidebar.markdown(f"**Player 2:** {p2_name}")
    st.sidebar.markdown("---")
    if st.session_state.game_log:
        for entry in reversed(st.session_state.game_log[-15:]): # Show recent logs
            st.sidebar.text(entry)
    else:
        st.sidebar.text("No moves made yet.")