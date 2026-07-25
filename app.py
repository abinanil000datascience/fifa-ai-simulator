import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Dynamically set the backend URL based on environment (Docker container vs local machine)
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="FIFA 2026 Enterprise Simulator",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2026 — Enterprise AI Analytics")

menu = st.sidebar.radio("Navigation Hub", [
    "🏆 48-Team Group Standings", 
    "📊 Stage-Aware Match Predictor", 
    "💬 AI Agent Intelligence"
])

# -------------------------------------------------------------
# TAB 1: 48-Team Standings with Group Filtering
# -------------------------------------------------------------
if menu == "🏆 48-Team Group Standings":
    st.header("Tournament Standings & Group Metrics")
    try:
        res = requests.get(f"{API_URL}/teams")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df = df.rename(columns={
                    "team_name": "Team", "group_letter": "Group",
                    "total_points": "Points", "goals_scored": "GF", "goals_conceded": "GA"
                })

                # Group Filter Bar
                groups = sorted(df["Group"].unique())
                selected_group = st.selectbox("Filter by Group (A - L)", ["All Groups"] + groups)

                if selected_group != "All Groups":
                    filtered_df = df[df["Group"] == selected_group]
                else:
                    filtered_df = df

                st.dataframe(filtered_df[["Team", "Group", "Points", "GF", "GA"]], use_container_width=True)

                # Interactive Plotly Chart
                fig = px.bar(
                    filtered_df, x="Team", y="Points", color="Group",
                    title="Points Distribution Across Teams",
                    text="Points"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Database is empty. Please run the seed script to populate the 48 teams.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# -------------------------------------------------------------
# TAB 2: Advanced Stage-Aware Monte Carlo Predictor
# -------------------------------------------------------------
elif menu == "📊 Stage-Aware Match Predictor":
    st.header("Predictive Match Simulation Engine")
    
    try:
        teams_res = requests.get(f"{API_URL}/teams")
        all_teams = sorted([t["team_name"] for t in teams_res.json()]) if teams_res.status_code == 200 else ["Argentina", "France"]
    except:
        all_teams = ["Argentina", "France", "Brazil", "Spain", "Germany"]

    col1, col2, col3 = st.columns(3)
    with col1:
        home = st.selectbox("Select Home Team", all_teams, index=0)
    with col2:
        away = st.selectbox("Select Away Team", all_teams, index=1 if len(all_teams) > 1 else 0)
    with col3:
        stage = st.selectbox("Tournament Stage", [
            "group", 
            "round_of_32", 
            "round_of_16", 
            "quarterfinal", 
            "semifinal", 
            "final"
        ])

    sims = st.slider("Monte Carlo Iterations", 1000, 25000, 5000, 1000)

    if st.button("Simulate Matchup", type="primary"):
        with st.spinner(f"Running {sims:,} Monte Carlo simulations for the {stage.replace('_', ' ').title()} stage..."):
            res = requests.get(f"{API_URL}/simulate", params={"home_team": home, "away_team": away, "simulations": sims, "stage": stage})
            if res.status_code == 200:
                data = res.json()
                probs = data["probabilities"]
                
                # Convert percentage strings to numeric values for plotting
                home_win_val = float(probs.get(f"{home}_win", "0").replace("%", ""))
                draw_val = float(probs.get("draw", "0").replace("%", "").replace(" (Knockout)", ""))
                away_win_val = float(probs.get(f"{away}_win", "0").replace("%", ""))

                # Display key statistics
                st.subheader(f"Matchup: {data['matchup']}")
                m1, m2, m3 = st.columns(3)
                m1.metric(f"{home} Win", f"{home_win_val}%")
                
                # Explicitly clarify draw scenario
                if stage == "group":
                    m2.metric("Draw Likelihood", f"{draw_val}%")
                else:
                    m2.metric("Draw Likelihood", "0.0% (Knockout)")
                    
                m3.metric(f"{away} Win", f"{away_win_val}%")

                # Plot Probability Breakdown
                prob_df = pd.DataFrame({
                    "Outcome": [f"{home} Win", "Draw", f"{away} Win"],
                    "Probability (%)": [home_win_val, draw_val, away_win_val]
                })
                fig_prob = px.bar(
                    prob_df, x="Outcome", y="Probability (%)", color="Outcome",
                    color_discrete_sequence=["#2ca02c", "#ff7f0e", "#d62728"],
                    title=f"Simulation Probability Distribution ({sims:,} runs)"
                )
                st.plotly_chart(fig_prob, use_container_width=True)
            else:
                st.error("Simulation failed. Please check the backend API.")

# -------------------------------------------------------------
# TAB 3: AI Agent Assistant
# -------------------------------------------------------------
elif menu == "💬 AI Agent Intelligence":
    st.header("Autonomous AI Sports Analyst")
    st.caption("Ask questions about any of the 48 teams, request tactical summaries, or execute match simulations")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("e.g. Simulate a quarterfinal match between Japan and Brazil, and explain Japan's tactics."):
        
        # Append and display user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process and display AI response
        with st.chat_message("assistant"):
            with st.spinner("AI Agent routing query and running tools..."):
                try:
                    res = requests.post(f"{API_URL}/agent/chat", json={"prompt": prompt})
                    
                    if res.status_code == 200:
                        response_data = res.json()
                        
                        if response_data and "response" in response_data:
                            ans = response_data["response"]
                            st.markdown(ans)
                            st.session_state.messages.append({"role": "assistant", "content": ans})
                        else:
                            st.warning("Received an empty response from the AI Agent.")
                    else:
                        st.error(f"Error connecting to the AI Agent endpoint. Status Code: {res.status_code}")
                        
                except Exception as e:
                    st.error(f"Failed to connect to backend server: {e}")