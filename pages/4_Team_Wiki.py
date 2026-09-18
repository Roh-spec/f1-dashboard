import streamlit as st
import pandas as pd
from datetime import date
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

        st.markdown("---")
        _render_team_driver_records(team_profile["constructorId"], team_profile["name"])


TEAM_DRIVER_RECORDS = {
    "ferrari": {
        "points": {"driver": "Charles Leclerc", "value": "356.0 pts", "year": "2024"},
        "podiums": {"driver": "Michael Schumacher", "value": "17 podiums", "year": "2002"},
        "wins": {"driver": "Michael Schumacher", "value": "13 wins", "year": "2004"},
        "poles": {"driver": "Michael Schumacher", "value": "11 poles", "year": "2001"},
    },
    "red_bull": {
        "points": {"driver": "Max Verstappen", "value": "575.0 pts", "year": "2023"},
        "podiums": {"driver": "Max Verstappen", "value": "21 podiums", "year": "2023"},
        "wins": {"driver": "Max Verstappen", "value": "19 wins", "year": "2023"},
        "poles": {"driver": "Sebastian Vettel", "value": "15 poles", "year": "2011"},
    },
    "mercedes": {
        "points": {"driver": "Lewis Hamilton", "value": "413.0 pts", "year": "2019"},
        "podiums": {"driver": "Lewis Hamilton", "value": "17 podiums", "year": "2015"},
        "wins": {"driver": "Lewis Hamilton", "value": "11 wins", "year": "2014"},
        "poles": {"driver": "Lewis Hamilton", "value": "12 poles", "year": "2016"},
    },
    "mclaren": {
        "points": {"driver": "Lando Norris", "value": "374.0 pts", "year": "2024"},
        "podiums": {"driver": "Alain Prost", "value": "14 podiums", "year": "1988"},
        "wins": {"driver": "Ayrton Senna", "value": "8 wins", "year": "1988"},
        "poles": {"driver": "Ayrton Senna", "value": "13 poles", "year": "1988"},
    },
    "williams": {
        "points": {"driver": "Valtteri Bottas", "value": "186.0 pts", "year": "2014"},
        "podiums": {"driver": "Nigel Mansell", "value": "12 podiums", "year": "1992"},
        "wins": {"driver": "Nigel Mansell", "value": "9 wins", "year": "1992"},
        "poles": {"driver": "Nigel Mansell", "value": "14 poles", "year": "1992"},
    },
    "aston_martin": {
        "points": {"driver": "Fernando Alonso", "value": "206.0 pts", "year": "2023"},
        "podiums": {"driver": "Fernando Alonso", "value": "8 podiums", "year": "2023"},
        "wins": {"driver": "Heinz-Harald Frentzen", "value": "2 wins", "year": "1999"},
        "poles": {"driver": "Lance Stroll", "value": "1 pole", "year": "2020"},
    },
    "alpine": {
        "points": {"driver": "Kimi Räikkönen", "value": "207.0 pts", "year": "2012"},
        "podiums": {"driver": "Fernando Alonso", "value": "15 podiums", "year": "2005"},
        "wins": {"driver": "Michael Schumacher", "value": "9 wins", "year": "1995"},
        "poles": {"driver": "Fernando Alonso", "value": "6 poles", "year": "2005"},
    },
    "rb": {
        "points": {"driver": "Pierre Gasly", "value": "110.0 pts", "year": "2021"},
        "podiums": {"driver": "Pierre Gasly", "value": "1 podium", "year": "2020"},
        "wins": {"driver": "Sebastian Vettel", "value": "1 win", "year": "2008"},
        "poles": {"driver": "Sebastian Vettel", "value": "1 pole", "year": "2008"},
    },
    "sauber": {
        "points": {"driver": "Robert Kubica", "value": "75.0 pts", "year": "2008"},
        "podiums": {"driver": "Robert Kubica", "value": "7 podiums", "year": "2008"},
        "wins": {"driver": "Robert Kubica", "value": "1 win", "year": "2008"},
        "poles": {"driver": "Robert Kubica", "value": "1 pole", "year": "2008"},
    },
    "haas": {
        "points": {"driver": "Kevin Magnussen", "value": "56.0 pts", "year": "2018"},
        "podiums": {"driver": "Romain Grosjean", "value": "0 (P4 Best)", "year": "2018"},
        "wins": {"driver": "Romain Grosjean", "value": "0 (P4 Best)", "year": "2018"},
        "poles": {"driver": "Kevin Magnussen", "value": "1 pole", "year": "2022"},
    },
}

ALIAS_MAP = {
    "racing_point": "aston_martin",
    "force_india": "aston_martin",
    "jordan": "aston_martin",
    "spyker": "aston_martin",
    "midland": "aston_martin",
    "renault": "alpine",
    "lotus_f1": "alpine",
    "benetton": "alpine",
    "toleman": "alpine",
    "alphatauri": "rb",
    "toro_rosso": "rb",
    "minardi": "rb",
    "bmw_sauber": "sauber",
    "alfa": "sauber",
    "alfa_romeo": "sauber",
    "brawn": "mercedes",
    "tyrrell": "mercedes",
    "bar": "mercedes",
    "honda": "mercedes",
    "jaguar": "red_bull",
    "stewart": "red_bull",
}


def _render_team_driver_records(constructor_id: str, constructor_name: str) -> None:
    key = ALIAS_MAP.get(constructor_id, constructor_id)
    records = TEAM_DRIVER_RECORDS.get(key)
    if not records:
        return

    st.markdown(
        f"""
        <div style="margin-top: 8px; margin-bottom: 8px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #8e929b; letter-spacing: 0.06em; text-transform: uppercase;">
                Single-Season Driver Records &bull; {constructor_name}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    categories = [
        ("🎯 Most Points in a Season", records.get("points"), "#00e5ff"),
        ("🍾 Most Podiums in a Season", records.get("podiums"), "#10b981"),
        ("🏁 Most Wins in a Season", records.get("wins"), "#f5a623"),
        ("⏱️ Most Poles in a Season", records.get("poles"), "#a855f7"),
    ]

    cols = st.columns(4)
    for col, (label, rec, cat_color) in zip(cols, categories):
        with col:
            if rec:
                st.markdown(
                    f"""
                    <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid {cat_color}; border-radius: 4px; padding: 10px 12px; margin-bottom: 6px;">
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 700; color: #8e929b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">{label}</div>
                        <div style="font-family: 'Titillium Web', sans-serif; font-size: 0.95rem; font-weight: 700; color: #f0f3f6; margin-bottom: 2px;">{rec['driver']}</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; font-weight: 700; color: {cat_color};">{rec['value']} <span style="font-size: 0.70rem; color: #8e929b; font-weight: 400; margin-left: 4px;">({rec['year']})</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_top_constructors_summary() -> None:
    with st.container(border=True, key="dialog_team_wiki_top_constructors"):
        st.markdown("<p class='section-kicker'>Championship Heritage</p>", unsafe_allow_html=True)
        st.markdown("<h2>Top Constructors by World Championships</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-subtitle' style='font-size:0.85rem; margin-bottom:14px;'>All-time top three Formula 1 constructors ranked by World Constructors' Championships and total Grand Prix victories.</p>",
            unsafe_allow_html=True,
        )

        top_constructors = [
            {
                "rank": "01",
                "name": "Scuderia Ferrari",
                "titles": 16,
                "wins": 248,
                "color": "#e80020",
                "badge": "16 WCC TITLES",
                "era": "1961, 1964, 1975-77, 1979, 1982-83, 1999-2004, 2007-08",
            },
            {
                "rank": "02",
                "name": "Williams Racing",
                "titles": 9,
                "wins": 114,
                "color": "#64c4ff",
                "badge": "9 WCC TITLES",
                "era": "1980-81, 1986-87, 1992-94, 1996-97",
            },
            {
                "rank": "03",
                "name": "McLaren",
                "titles": 9,
                "wins": 188,
                "color": "#ff8000",
                "badge": "9 WCC TITLES",
                "era": "1974, 1984-85, 1988-91, 1998, 2024",
            },
        ]

        top_team_cols = st.columns(3)
        for col, team in zip(top_team_cols, top_constructors):
            with col:
                st.markdown(
                    f"""
                    <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid {team['color']}; border-radius: 6px; padding: 14px 16px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #8e929b; letter-spacing: 0.06em;">RANK {team['rank']}</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 700; color: {team['color']}; background: rgba(255,255,255,0.04); border: 1px solid {team['color']}; padding: 1px 6px; border-radius: 2px;">{team['badge']}</span>
                        </div>
                        <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.15rem; font-weight: 700; color: #f0f3f6; letter-spacing: 0.02em; margin-bottom: 8px;">{team['name']}</div>
                        <div style="display: flex; gap: 18px; align-items: baseline; margin-bottom: 6px;">
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 800; color: #ffffff;">{team['titles']}</span>
                                <span style="font-size: 0.72rem; color: #8e929b; text-transform: uppercase; margin-left: 3px;">Titles</span>
                            </div>
                            <div>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; font-weight: 700; color: #00e5ff;">{team['wins']}</span>
                                <span style="font-size: 0.72rem; color: #8e929b; text-transform: uppercase; margin-left: 3px;">Wins</span>
                            </div>
                        </div>
                        <div style="font-size: 0.70rem; color: #6b7280; font-family: 'JetBrains Mono', monospace;">Championship Years: {team['era']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


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

    _render_top_constructors_summary()

    current_year = date.today().year
    season_options = list(range(current_year, 1999, -1))

    with st.container(border=True, key="dialog_team_wiki_controls"):
        st.markdown("<p class='section-kicker'>Filter</p>", unsafe_allow_html=True)
        st.markdown("<h2>Scope & Constructor Select</h2>", unsafe_allow_html=True)
        col_season, col_team = st.columns(2)
        with col_season:
            selected_season = st.selectbox("SEASON", season_options, index=1)

        teams_df = get_teams_for_season(int(selected_season))
        if teams_df is None or teams_df.empty:
            st.warning("No teams found for the selected season.")
            return

        teams_df = teams_df.sort_values("name").reset_index(drop=True)
        team_names = teams_df["name"].tolist()
        team_options = team_names + ["All Teams"]

        with col_team:
            selected_team = st.selectbox("SELECT TEAM", team_options)

    if selected_team == "All Teams":
        for _, row in teams_df.iterrows():
            profile = get_team_wiki_profile(row["constructorId"], row["name"], int(selected_season))
            render_team_box(profile, int(selected_season))
    else:
        selected_row = teams_df[teams_df["name"] == selected_team]
        if not selected_row.empty:
            row = selected_row.iloc[0]
            profile = get_team_wiki_profile(row["constructorId"], row["name"], int(selected_season))
            render_team_box(profile, int(selected_season))


render_page()
