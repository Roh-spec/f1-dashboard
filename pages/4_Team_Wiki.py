import streamlit as st
import pandas as pd
import sessions
from ui import get_team_color


get_teams_for_season = getattr(sessions, "get_teams_for_season", None)
get_team_wiki_profile = getattr(sessions, "get_team_wiki_profile", None)


def render_team_box(team_profile, selected_season):
    team_color = get_team_color(team_profile["name"])
    with st.container(border=True, key=f"dialog_team_{team_profile['constructorId']}"):
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; border-left: 4px solid {team_color}; padding-left: 12px;">
                <h2 style="margin: 0; padding: 0; color: #f0f3f6;">{team_profile['name']}</h2>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: {team_color}; background: rgba(255,255,255,0.04); border: 1px solid {team_color}; padding: 2px 8px; text-transform: uppercase;">TEAM DOSSIER</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_left, col_right = st.columns(2, gap="large")

        with col_left:
            st.markdown("**Overview**")
            overview_df = pd.DataFrame(
                [
                    {"Metric": "Debut", "Value": team_profile["debut"]},
                    {"Metric": "Team leader", "Value": team_profile["leader"]},
                    {"Metric": "Number of races", "Value": int(team_profile["races"])},
                    {"Metric": "WDC titles", "Value": int(team_profile["wdc_count"])},
                    {"Metric": "WCC titles", "Value": int(team_profile["wcc_count"])},
                ]
            )
            st.dataframe(overview_df, hide_index=True, use_container_width=True)

            st.markdown("---")
            st.markdown("**Previous names & Lineage**")
            if team_profile["previous_names"]:
                prev_df = pd.DataFrame({"Name": sorted(team_profile["previous_names"])})
                st.dataframe(prev_df, hide_index=True, use_container_width=True)
            else:
                st.caption("None recorded")

        with col_right:
            st.markdown(f"**Drivers in {selected_season}**")
            if team_profile["drivers"]:
                driver_rows = []
                for item in team_profile["drivers"]:
                    if "(" in item and item.endswith("pts)"):
                        name, points = item.rsplit("(", 1)
                        driver_rows.append(
                            {
                                "Driver": name.strip(),
                                "Points": points.replace("pts)", "").strip(),
                            }
                        )
                    else:
                        driver_rows.append({"Driver": item, "Points": "-"})

                drivers_df = pd.DataFrame(driver_rows)
                st.dataframe(drivers_df, hide_index=True, use_container_width=True)
            else:
                st.caption("Data unavailable")

            st.markdown("---")
            st.markdown("**Constructor Brief**")
            st.write(f"> {team_profile['history']}")

        st.markdown("---")
        title_col_left, title_col_right = st.columns(2, gap="large")

        with title_col_left:
            st.markdown(f"**🏆 WDC Titles ({team_profile['wdc_count']})**")
            if team_profile["wdc_entries"]:
                wdc_df = pd.DataFrame(team_profile["wdc_entries"])
                wdc_df = wdc_df.rename(columns={"season": "Season", "driver": "Champion Driver", "points": "Points"})
                st.dataframe(wdc_df, hide_index=True, use_container_width=True)
            else:
                st.caption("No WDC titles recorded")

        with title_col_right:
            st.markdown(f"**🏆 WCC Titles ({team_profile['wcc_count']})**")
            if team_profile["wcc_entries"]:
                wcc_df = pd.DataFrame(team_profile["wcc_entries"])
                wcc_df = wcc_df.rename(columns={"season": "Season", "points": "Points", "drivers": "Drivers"})
                st.dataframe(wcc_df, hide_index=True, use_container_width=True)
            else:
                st.caption("No WCC titles recorded")


def render_page():
    if get_teams_for_season is None or get_team_wiki_profile is None:
        st.error("Team wiki functions are unavailable in sessions.py.")
        return

    with st.container(border=True, key="dialog_team_wiki_header"):
        st.markdown("<p class='section-kicker'>Constructor Intelligence</p>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TEAM WIKI</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-subtitle'>Constructor encyclopedia with debut info, leaders, drivers, races, championship titles, and historical lineage.</p>",
            unsafe_allow_html=True,
        )

    with st.container(border=True, key="dialog_team_wiki_controls"):
        st.markdown("<p class='section-kicker'>Filter</p>", unsafe_allow_html=True)
        st.markdown("<h2>Season Scope</h2>", unsafe_allow_html=True)
        current_year = 2025
        season_options = list(range(current_year, 1999, -1))
        selected_season = st.selectbox("SEASON", season_options, index=1)

    teams_df = get_teams_for_season(int(selected_season))
    if teams_df.empty:
        st.warning("No teams found for the selected season.")
        return

    teams_df = teams_df.sort_values("name").reset_index(drop=True)

    with st.container(border=True, key="dialog_team_wiki_list"):
        st.markdown("<p class='section-kicker'>Alphabetical Team List</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p class='panel-note' style='color:#8e929b; font-size:20px;'>{len(teams_df)} teams participating in {selected_season}, sorted alphabetically.</p>",
            unsafe_allow_html=True,
        )

    for _, row in teams_df.iterrows():
        profile = get_team_wiki_profile(row["constructorId"], row["name"], int(selected_season))
        render_team_box(profile, int(selected_season))


render_page()
