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

        _render_trophy_cabinet(team_profile["constructorId"], team_color)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

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
        _render_team_mount_rushmore(team_profile["constructorId"], team_profile["name"], team_color)

        st.markdown("---")
        _render_dominant_season_and_engine(team_profile["constructorId"], team_profile["name"], team_color)

        st.markdown("---")
        _render_team_driver_records(team_profile["constructorId"], team_profile["name"])


TEAM_TROPHY_CABINET = {
    "ferrari": {"wcc": 16, "wdc": 15, "one_two": 85, "streak": "10 Wins (2002)"},
    "mclaren": {"wcc": 9, "wdc": 12, "one_two": 49, "streak": "11 Wins (1988)"},
    "williams": {"wcc": 9, "wdc": 7, "one_two": 33, "streak": "7 Wins (1993)"},
    "mercedes": {"wcc": 8, "wdc": 9, "one_two": 59, "streak": "10 Wins (2016)"},
    "red_bull": {"wcc": 6, "wdc": 7, "one_two": 31, "streak": "15 Wins (2023)"},
    "alpine": {"wcc": 3, "wdc": 4, "one_two": 4, "streak": "4 Wins (2006)"},
    "aston_martin": {"wcc": 0, "wdc": 0, "one_two": 1, "streak": "1 Win (1998, 2020)"},
    "sauber": {"wcc": 0, "wdc": 0, "one_two": 1, "streak": "1 Win (2008)"},
    "rb": {"wcc": 0, "wdc": 0, "one_two": 0, "streak": "1 Win (2008, 2020)"},
    "haas": {"wcc": 0, "wdc": 0, "one_two": 0, "streak": "Best P4 (2018)"},
}

TEAM_MOUNT_RUSHMORE = {
    "ferrari": [
        {"name": "Michael Schumacher", "stats": "72 Wins &bull; 5 WDC Titles", "years": "1996 - 2006", "country": "GER"},
        {"name": "Niki Lauda", "stats": "15 Wins &bull; 2 WDC Titles", "years": "1974 - 1977", "country": "AUT"},
        {"name": "Alberto Ascari", "stats": "13 Wins &bull; 2 WDC Titles", "years": "1950 - 1954", "country": "ITA"},
        {"name": "Charles Leclerc", "stats": "8 Wins &bull; 26 Poles &bull; 2022 P2", "years": "2019 - Present", "country": "MON"},
    ],
    "mclaren": [
        {"name": "Ayrton Senna", "stats": "35 Wins &bull; 3 WDC Titles", "years": "1988 - 1993", "country": "BRA"},
        {"name": "Alain Prost", "stats": "30 Wins &bull; 3 WDC Titles", "years": "1980, 1984 - 1989", "country": "FRA"},
        {"name": "Lewis Hamilton", "stats": "21 Wins &bull; 1 WDC Title", "years": "2007 - 2012", "country": "GBR"},
        {"name": "Mika Häkkinen", "stats": "20 Wins &bull; 2 WDC Titles", "years": "1993 - 2001", "country": "FIN"},
    ],
    "red_bull": [
        {"name": "Max Verstappen", "stats": "63 Wins &bull; 4 WDC Titles", "years": "2016 - Present", "country": "NED"},
        {"name": "Sebastian Vettel", "stats": "38 Wins &bull; 4 WDC Titles", "years": "2009 - 2014", "country": "GER"},
        {"name": "Mark Webber", "stats": "9 Wins &bull; 42 Podiums &bull; 3x P3", "years": "2007 - 2013", "country": "AUS"},
        {"name": "Daniel Ricciardo", "stats": "7 Wins &bull; 29 Podiums &bull; 2x P3", "years": "2014 - 2018", "country": "AUS"},
    ],
    "mercedes": [
        {"name": "Lewis Hamilton", "stats": "84 Wins &bull; 6 WDC Titles", "years": "2013 - 2024", "country": "GBR"},
        {"name": "Nico Rosberg", "stats": "23 Wins &bull; 1 WDC Title", "years": "2010 - 2016", "country": "GER"},
        {"name": "Valtteri Bottas", "stats": "10 Wins &bull; 20 Poles &bull; 2x P2", "years": "2017 - 2021", "country": "FIN"},
        {"name": "Juan Manuel Fangio", "stats": "8 Wins &bull; 2 WDC Titles", "years": "1954 - 1955", "country": "ARG"},
    ],
    "williams": [
        {"name": "Nigel Mansell", "stats": "28 Wins &bull; 1 WDC Title", "years": "1985-88, 1991-92, 1994", "country": "GBR"},
        {"name": "Damon Hill", "stats": "21 Wins &bull; 1 WDC Title", "years": "1993 - 1996", "country": "GBR"},
        {"name": "Alan Jones", "stats": "11 Wins &bull; 1 WDC Title", "years": "1978 - 1981", "country": "AUS"},
        {"name": "Jacques Villeneuve", "stats": "11 Wins &bull; 1 WDC Title", "years": "1996 - 1997", "country": "CAN"},
    ],
    "aston_martin": [
        {"name": "Fernando Alonso", "stats": "8 Podiums &bull; 206 Pts &bull; 2023 P4", "years": "2023 - Present", "country": "ESP"},
        {"name": "Heinz-Harald Frentzen", "stats": "2 Wins &bull; 1999 Title Contender (P3)", "years": "1999 - 2001 (Jordan)", "country": "GER"},
        {"name": "Sergio Pérez", "stats": "1 Win &bull; 7 Podiums", "years": "2014 - 2020 (Force India / RP)", "country": "MEX"},
        {"name": "Giancarlo Fisichella", "stats": "1 Win &bull; 1 Pole &bull; 2 Podiums", "years": "1997, 2002-03, 2008-09", "country": "ITA"},
    ],
    "alpine": [
        {"name": "Fernando Alonso", "stats": "17 Wins &bull; 2 WDC Titles", "years": "2003-06, 2008-09, 2021-22", "country": "ESP"},
        {"name": "Michael Schumacher", "stats": "19 Wins &bull; 2 WDC Titles", "years": "1991 - 1995 (Benetton)", "country": "GER"},
        {"name": "Alain Prost", "stats": "9 Wins &bull; 1983 WDC Runner-Up", "years": "1981 - 1983 (Renault)", "country": "FRA"},
        {"name": "Kimi Räikkönen", "stats": "2 Wins &bull; 15 Podiums", "years": "2012 - 2013 (Lotus F1)", "country": "FIN"},
    ],
    "rb": [
        {"name": "Sebastian Vettel", "stats": "1 Win &bull; 1 Pole &bull; Historic Monza Victory", "years": "2007 - 2008 (Toro Rosso)", "country": "GER"},
        {"name": "Pierre Gasly", "stats": "1 Win &bull; 3 Podiums &bull; Monza 2020", "years": "2017-18, 2019-22", "country": "FRA"},
        {"name": "Daniil Kvyat", "stats": "1 Podium (Hockenheim 2019)", "years": "2014, 2016-17, 2019-20", "country": "RUS"},
        {"name": "Max Verstappen", "stats": "62 Pts &bull; P4 Debut Season Best", "years": "2015 - 2016 (Toro Rosso)", "country": "NED"},
    ],
    "sauber": [
        {"name": "Robert Kubica", "stats": "1 Win &bull; 1 Pole &bull; 9 Podiums &bull; 2008 P4", "years": "2006 - 2009 (BMW Sauber)", "country": "POL"},
        {"name": "Nick Heidfeld", "stats": "8 Podiums &bull; 2007 P5", "years": "2001-03, 2006-09", "country": "GER"},
        {"name": "Valtteri Bottas", "stats": "59 Pts &bull; Team Leader", "years": "2022 - 2024 (Alfa Romeo)", "country": "FIN"},
        {"name": "Kimi Räikkönen", "stats": "F1 Debut (2001) &bull; 57 Pts", "years": "2001, 2019 - 2021", "country": "FIN"},
    ],
    "haas": [
        {"name": "Kevin Magnussen", "stats": "1 Pole (São Paulo 2022) &bull; 131 Pts", "years": "2017-20, 2022-2024", "country": "DEN"},
        {"name": "Romain Grosjean", "stats": "102 Pts &bull; Best finish P4 (Austria 2018)", "years": "2016 - 2020", "country": "FRA"},
        {"name": "Nico Hülkenberg", "stats": "40 Pts &bull; Consecutive Top-6 Finishes", "years": "2023 - 2024", "country": "GER"},
        {"name": "Mick Schumacher", "stats": "12 Pts &bull; Best finish P6 (Austria 2022)", "years": "2021 - 2022", "country": "GER"},
    ],
}

TEAM_ENGINE_LINEAGE = {
    "ferrari": "Ferrari V12 (1950-80) ➔ Turbo V6 (1981-88) ➔ V12 (1989-95) ➔ V10 (1996-2005) ➔ V8 (2006-13) ➔ 1.6L V6 Turbo-Hybrid (2014-Present)",
    "mclaren": "Ford Cosworth (1968-83) ➔ TAG-Porsche (1983-87) ➔ Honda (1988-92) ➔ Ford/Peugeot (1993-94) ➔ Mercedes (1995-2014) ➔ Honda (2015-17) ➔ Renault (2018-20) ➔ Mercedes-AMG (2021-Present)",
    "williams": "Ford Cosworth (1977-83) ➔ Honda (1983-87) ➔ Judd (1988) ➔ Renault (1989-97) ➔ Mecachrome (1998-99) ➔ BMW (2000-05) ➔ Cosworth/Toyota (2006-11) ➔ Renault (2012-13) ➔ Mercedes-AMG (2014-Present)",
    "red_bull": "Cosworth (2005) ➔ Ferrari (2006) ➔ Renault V8/V6 (2007-18) ➔ Honda / Red Bull Powertrains (2019-Present)",
    "mercedes": "Mercedes-Benz Straight-8 (1954-55) ➔ Mercedes-Benz V8 (2010-13) ➔ Mercedes-AMG 1.6L V6 Turbo-Hybrid (2014-Present)",
    "aston_martin": "Jordan-Ford/Peugeot/Mugen (1991-2005) ➔ Midland/Spyker-Toyota/Ferrari (2006-08) ➔ Mercedes-Benz (2009-Present)",
    "alpine": "Renault V6 Turbo (1977-85) ➔ Benetton-Ford/Renault (1986-2001) ➔ Renault V10/V8 (2002-10) ➔ Lotus-Renault (2012-14) ➔ Renault E-Tech Turbo-Hybrid (2016-Present)",
    "rb": "Cosworth (2006) ➔ Ferrari (2007-13, 2016) ➔ Renault (2014-15, 2017) ➔ Honda / Red Bull Powertrains (2018-Present)",
    "sauber": "Ilmor/Mercedes (1993-94) ➔ Ford (1995-96) ➔ Ferrari/Petronas (1997-2005) ➔ BMW (2006-09) ➔ Ferrari (2010-Present)",
    "haas": "Ferrari 061/062 1.6L V6 Turbo-Hybrid (2016-Present)",
}

TEAM_DOMINANT_SEASONS = {
    "red_bull": {
        "season": 2023,
        "wins": "21 / 22 Wins",
        "win_rate": "95.5%",
        "points": "860.0 Pts",
        "margin": "+451 Pts over P2",
        "car": "RB19 (Adrian Newey)",
        "summary": "The most dominant season by any constructor in Formula 1 history, breaking the all-time consecutive wins record with 15 straight victories.",
    },
    "mclaren": {
        "season": 1988,
        "wins": "15 / 16 Wins",
        "win_rate": "93.8%",
        "points": "199.0 Pts",
        "margin": "+134 Pts over Ferrari",
        "car": "MP4/4 (Gordon Murray, Steve Nichols)",
        "summary": "Ayrton Senna and Alain Prost swept all but one race of the 1988 championship, setting the benchmark for total constructor supremacy.",
    },
    "mercedes": {
        "season": 2016,
        "wins": "19 / 21 Wins",
        "win_rate": "90.5%",
        "points": "765.0 Pts",
        "margin": "+297 Pts over Red Bull",
        "car": "F1 W07 Hybrid",
        "summary": "Lewis Hamilton and Nico Rosberg locked out 20 of 21 pole positions and won 19 Grands Prix in a legendary intra-team world title duel.",
    },
    "ferrari": {
        "season": 2002,
        "wins": "15 / 17 Wins",
        "win_rate": "88.2%",
        "points": "221.0 Pts",
        "margin": "+129 Pts over Williams",
        "car": "F2002 (Rory Byrne, Ross Brawn)",
        "summary": "Michael Schumacher achieved a podium in 100% of the races (17/17) and clinched the World Championship with 6 races to spare in France.",
    },
    "williams": {
        "season": 1992,
        "wins": "10 / 16 Wins",
        "win_rate": "62.5%",
        "points": "164.0 Pts",
        "margin": "+65 Pts over McLaren",
        "car": "FW14B (Patrick Head, Adrian Newey)",
        "summary": "A technological tour-de-force with active suspension and traction control, carrying Nigel Mansell to 9 wins and 14 pole positions.",
    },
    "alpine": {
        "season": 2005,
        "wins": "8 Wins &bull; 18 Podiums",
        "win_rate": "42.1%",
        "points": "191.0 Pts",
        "margin": "+9 Pts over McLaren",
        "car": "R25 (Flavio Briatore, Pat Symonds)",
        "summary": "Fernando Alonso dethroned Ferrari to claim the double World Championship titles with the iconic howling Renault V10.",
    },
    "aston_martin": {
        "season": 2023,
        "wins": "8 Podiums",
        "win_rate": "Podium Rate: 36.4%",
        "points": "280.0 Pts",
        "margin": "5th in WCC",
        "car": "AMR23 (Dan Fallows)",
        "summary": "Fernando Alonso took 6 podiums in the first 8 races, spearheading a historic resurgence for the Silverstone squad.",
    },
    "rb": {
        "season": 2021,
        "wins": "1 Podium &bull; 142 Pts",
        "win_rate": "P6 in WCC",
        "points": "142.0 Pts",
        "margin": "Highest points tally",
        "car": "AT02 (Jody Egginton)",
        "summary": "Pierre Gasly and Yuki Tsunoda amassed the Faenza team's highest ever championship points tally with consistent top-6 qualifying pace.",
    },
    "sauber": {
        "season": 2008,
        "wins": "1 Win &bull; 11 Podiums",
        "win_rate": "P3 in WCC",
        "points": "135.0 Pts",
        "margin": "1-2 Canadian GP Finish",
        "car": "F1.08 (Willy Rampf)",
        "summary": "Robert Kubica and Nick Heidfeld secured a historic 1-2 victory in Montreal, briefly leading both World Championships.",
    },
    "haas": {
        "season": 2018,
        "wins": "Best Finish: P4 (Austria)",
        "win_rate": "P5 in WCC",
        "points": "93.0 Pts",
        "margin": "5th in WCC",
        "car": "VF-18 (Guenther Steiner)",
        "summary": "In only their third season in Formula 1, Haas finished 5th in the Constructors' Championship with Kevin Magnussen and Romain Grosjean.",
    },
}


def _render_trophy_cabinet(constructor_id: str, team_color: str) -> None:
    key = ALIAS_MAP.get(constructor_id, constructor_id)
    cabinet = TEAM_TROPHY_CABINET.get(key, {"wcc": 0, "wdc": 0, "one_two": 0, "streak": "N/A"})

    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 10px 14px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.4rem;">🏆</span>
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #8e929b; text-transform: uppercase;">WCC TITLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #f5a623;">{cabinet['wcc']}</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.4rem;">🎖️</span>
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #8e929b; text-transform: uppercase;">DRIVERS' TITLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #00e5ff;">{cabinet['wdc']}</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.4rem;">🥇🥈</span>
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #8e929b; text-transform: uppercase;">1-2 FINISHES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #10b981;">{cabinet['one_two']}</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.4rem;">🔥</span>
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #8e929b; text-transform: uppercase;">WIN STREAK RECORD</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 800; color: #ffffff;">{cabinet['streak']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_team_mount_rushmore(constructor_id: str, constructor_name: str, team_color: str) -> None:
    key = ALIAS_MAP.get(constructor_id, constructor_id)
    legends = TEAM_MOUNT_RUSHMORE.get(key, [])
    if not legends:
        return

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #f5a623; letter-spacing: 0.06em; text-transform: uppercase;">HALL OF FAME</span>
                <h3 style="margin: 2px 0 0 0; color: #f0f3f6;">Constructor's All-Time Legends</h3>
            </div>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8e929b;">MOST SUCCESSFUL DRIVERS FOR {constructor_name.upper()}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(legends))
    for col, drv in zip(cols, legends):
        with col:
            st.markdown(
                f"""
                <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid {team_color}; border-radius: 6px; padding: 12px 14px; height: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #8e929b;">{drv['years']}</span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: {team_color}; background: rgba(255,255,255,0.04); border: 1px solid {team_color}; padding: 1px 5px; border-radius: 2px;">{drv['country']}</span>
                    </div>
                    <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.05rem; font-weight: 700; color: #f0f3f6; margin-bottom: 4px;">{drv['name']}</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600; color: #00e5ff;">{drv['stats']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_dominant_season_and_engine(constructor_id: str, constructor_name: str, team_color: str) -> None:
    key = ALIAS_MAP.get(constructor_id, constructor_id)
    dom = TEAM_DOMINANT_SEASONS.get(key)
    engine = TEAM_ENGINE_LINEAGE.get(key)

    col_dom, col_eng = st.columns([1.1, 1.3], gap="medium")

    with col_dom:
        if dom:
            st.markdown(
                f"""
                <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-left: 4px solid #f5a623; border-radius: 6px; padding: 14px 16px; height: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #f5a623; text-transform: uppercase;">PEAK DOMINANT SEASON &bull; {dom['season']}</span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 800; color: #ffffff; background: rgba(245,166,35,0.12); border: 1px solid #f5a623; padding: 1px 8px; border-radius: 2px;">{dom['win_rate']}</span>
                    </div>
                    <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.12rem; font-weight: 700; color: #f0f3f6; margin-bottom: 6px;">{dom['car']}</div>
                    <div style="display: flex; gap: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; margin-bottom: 8px;">
                        <span style="color: #00e5ff; font-weight: 700;">{dom['wins']}</span>
                        <span style="color: #8e929b;">&bull;</span>
                        <span style="color: #ffffff; font-weight: 700;">{dom['points']}</span>
                        <span style="color: #8e929b;">&bull;</span>
                        <span style="color: #10b981;">{dom['margin']}</span>
                    </div>
                    <p style="font-size: 0.82rem; color: #8e929b; margin: 0; line-height: 1.4;">{dom['summary']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_eng:
        if engine:
            st.markdown(
                f"""
                <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-left: 4px solid #00e5ff; border-radius: 6px; padding: 14px 16px; height: 100%;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #00e5ff; text-transform: uppercase; margin-bottom: 6px;">
                        ENGINE SUPPLIER & POWER UNIT HERITAGE
                    </div>
                    <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.05rem; font-weight: 700; color: #f0f3f6; margin-bottom: 8px;">
                        Power Unit Chronology
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #c9d1d9; line-height: 1.6; background: rgba(0,0,0,0.22); padding: 10px 12px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.04);">
                        {engine}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
