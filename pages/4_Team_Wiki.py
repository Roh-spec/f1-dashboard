import streamlit as st
import pandas as pd
import sessions


get_teams_for_season = getattr(sessions, "get_teams_for_season", None)
get_team_wiki_profile = getattr(sessions, "get_team_wiki_profile", None)


def render_team_box(team_profile, selected_season):
    with st.container(border=True, key=f"dialog_team_{team_profile['constructorId']}"):
        st.markdown(f"<h2>{team_profile['name']}</h2>", unsafe_allow_html=True)
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
            st.markdown("**Previous names**")
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
            st.markdown("**Brief history**")
            st.write(f"> {team_profile['history']}")

        st.markdown("---")
        title_col_left, title_col_right = st.columns(2, gap="large")

        with title_col_left:
            st.markdown("**WDC title years**")
            if team_profile["wdc_entries"]:
                wdc_df = pd.DataFrame(team_profile["wdc_entries"])
                wdc_df = wdc_df.rename(columns={"season": "Season", "driver": "Driver", "points": "Points"})
                st.dataframe(wdc_df, hide_index=True, use_container_width=True)
            else:
                st.caption("No WDC titles recorded")

        with title_col_right:
            st.markdown("**WCC title years**")
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
            "<p class='hero-subtitle'>Team encyclopedia with debut info, leaders, drivers, races, championships, and naming history.</p>",
            unsafe_allow_html=True,
        )
        st.warning(
            "INCOMPLETE: Some historical team lineage and title-era attribution may be partial depending on source data coverage."
        )

    with st.container(border=True, key="dialog_team_wiki_controls"):
        st.markdown("<p class='section-kicker'>Filter</p>", unsafe_allow_html=True)
        st.markdown("<h2>Season Scope</h2>", unsafe_allow_html=True)
        current_year = 2026
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
            f"<p class='panel-note'>{len(teams_df)} teams found for {selected_season}, sorted alphabetically.</p>",
            unsafe_allow_html=True,
        )

    for _, row in teams_df.iterrows():
        profile = get_team_wiki_profile(row["constructorId"], row["name"], int(selected_season))
        render_team_box(profile, int(selected_season))


if st.button("<- RETURN TO RACE SELECT"):
    st.switch_page("pages/1_Race_Select.py")

render_page()
