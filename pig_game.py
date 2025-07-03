import streamlit as st
import random
import time

st.set_page_config(page_title="Pig Dice Game", layout="centered")
st.title("🐷 Pig Dice Game")
st.caption("Roll the dice, accumulate points, and try to reach 100 before the computer!")

if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "current_turn_total" not in st.session_state:
    st.session_state.current_turn_total = 0
if "current_player" not in st.session_state:
    st.session_state.current_player = "human"
if "last_roll" not in st.session_state:
    st.session_state.last_roll = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "message" not in st.session_state:
    st.session_state.message = "Your turn! Roll the dice to start."

def roll_dice():
    roll = random.randint(1, 6)
    st.session_state.last_roll = roll
    
    if roll == 1:
        st.session_state.current_turn_total = 0
        st.session_state.message = "Oh no! You rolled a 1. Your turn is over."
        st.session_state.current_player = "computer"
    else:
        st.session_state.current_turn_total += roll
        st.session_state.message = f"You rolled a {roll}! Your turn total is {st.session_state.current_turn_total}."

def hold():
    st.session_state.player_score += st.session_state.current_turn_total
    st.session_state.current_turn_total = 0
    st.session_state.message = "You held! Turn over."
    st.session_state.current_player = "computer"
    
    if st.session_state.player_score >= 100:
        st.session_state.game_over = True
        st.session_state.winner = "human"

def computer_turn():
    turn_total = 0
    computer_message = ""
    
    rolls = random.randint(1, 4)
    for i in range(rolls):
        roll = random.randint(1, 6)
        time.sleep(0.7)
        
        if roll == 1:
            computer_message += f"Computer rolled a 1. Turn lost! "
            turn_total = 0
            break
        else:
            turn_total += roll
            computer_message += f"Computer rolled a {roll}. "
            
            if (turn_total >= 20) or (st.session_state.computer_score + turn_total >= 80):
                computer_message += f"Computer holds with {turn_total} points this turn."
                break
    
    st.session_state.computer_score += turn_total
    st.session_state.message = computer_message
    st.session_state.last_roll = roll
    
    if st.session_state.computer_score >= 100:
        st.session_state.game_over = True
        st.session_state.winner = "computer"
    else:
        st.session_state.current_player = "human"
        st.session_state.current_turn_total = 0

def reset_game():
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.current_turn_total = 0
    st.session_state.current_player = "human"
    st.session_state.last_roll = 1
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.message = "New game! Your turn - roll the dice to start."

col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 Your Score")
    st.header(f"{st.session_state.player_score}")

with col2:
    st.subheader("🤖 Computer Score")
    st.header(f"{st.session_state.computer_score}")

dice_emoji = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚄",
    6: "⚅"
}

st.header(f"{dice_emoji[st.session_state.last_roll]}")
st.caption("Last roll")

st.subheader(f"Current Turn: {st.session_state.current_turn_total} points")
st.info(st.session_state.message)

if st.session_state.game_over:
    if st.session_state.winner == "human":
        st.success("🎉 Congratulations! You won the game!")
    else:
        st.error("😢 Computer won! Better luck next time!")
    
    st.button("🔄 Play Again", on_click=reset_game)
else:
    if st.session_state.current_player == "human":
        col1, col2 = st.columns([1, 2])
        with col1:
            st.button("🎲 Roll Dice", on_click=roll_dice, use_container_width=True)
        with col2:
            st.button("🤚 Hold", on_click=hold, use_container_width=True)
    else:
        if st.button("⏳ Computer's Turn", use_container_width=True):
            computer_turn()

with st.expander("📖 How to Play"):
    st.write("""
    **Pig Dice Game Rules:**
    1. Players take turns rolling a single die
    2. Roll as many times as you want to accumulate points
    3. If you roll a 1, you lose all points from that turn
    4. Choose "Hold" to add your turn points to your total score
    5. First to reach 100 points wins!
    
    **Computer Strategy:**
    - The computer will roll 1-4 times per turn
    - It will stop rolling if it accumulates 20+ points in one turn
    - It plays more aggressively when close to winning
    """)

st.divider()
st.subheader("Game Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Target Score", "100")
col2.metric("Your Turn Total", st.session_state.current_turn_total)
col3.metric("Current Player", "You" if st.session_state.current_player == "human" else "Computer")

st.divider()
st.caption("Developed with Streamlit | Pig Dice Game")