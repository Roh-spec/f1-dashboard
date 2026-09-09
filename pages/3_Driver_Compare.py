import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import streamlit as st
import sessions
from ui import get_team_color


get_driver_directory = getattr(sessions, "get_driver_directory", None)
get_drivers_for_season = getattr(sessions, "get_drivers_for_season", None)
get_driver_history_blurb = getattr(sessions, "get_driver_history_blurb", None)
get_driver_profile = getattr(sessions, "get_driver_profile", None)
get_driver_season_results = getattr(sessions, "get_driver_season_results", None)
get_season_race_calendar = getattr(sessions, "get_season_race_calendar", None)


def _render_driver_profile(driver_id: str) -> None:
    if get_driver_profile is None or get_driver_history_blurb is None:
        st.error("Driver data functions are unavailable in sessions.py.")
        return

    if not driver_id:
        st.warning("Driver profile unavailable.")
        return

    profile = get_driver_profile(driver_id)
    if not profile:
        st.warning("Driver profile unavailable.")
        return

    st.markdown("<p class='section-kicker'>Driver Dossier</p>", unsafe_allow_html=True)
    st.markdown(f"<h2>{profile['fullName']}</h2>", unsafe_allow_html=True)
    st.markdown(
        "\n".join(
            [
                f"- **Nationality:** {profile['nationality']}",
                f"- **Races:** {profile['races']}",
                f"- **Wins:** {profile['wins']}",
                f"- **Points:** {profile['points']:.1f}",
                f"- **Debut race:** {profile['debut']}",
                f"- **Most points in a season:** {profile['most_points']}",
                f"- **Least points in a season:** {profile['least_points']}",
            ]
        )
    )

    history_blurb = get_driver_history_blurb(profile['fullName'])
    st.markdown("<h3>Career Brief</h3>", unsafe_allow_html=True)
    st.write(f"> {history_blurb}")


def _build_comparison_series(driver_id: str, series_name: str, season: int) -> pd.DataFrame:
    if get_driver_season_results is None:
        return pd.DataFrame(columns=["Round", "RaceName", series_name])

    season_results = get_driver_season_results(driver_id, int(season))
    if season_results.empty:
        return pd.DataFrame(columns=["Round", "RaceName", series_name])

    series = season_results[["Round", "RaceName", "points"]].copy()
    series = series.sort_values("Round").reset_index(drop=True)
    series[series_name] = pd.to_numeric(series["points"], errors="coerce").fillna(0.0).cumsum()
    series = series[["Round", "RaceName", series_name]]
    return series


def render_page() -> None:
    if (
        get_driver_directory is None
        or get_drivers_for_season is None
        or get_driver_season_results is None
    ):
        st.error("Driver directory function is unavailable in sessions.py.")
        return

    with st.container(border=True, key="dialog_driver_compare_header"):
        st.markdown("<p class='section-kicker'>Driver Intelligence</p>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>DRIVER COMPARISON & HISTORY</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-subtitle'>Compare two Formula 1 drivers by career profile and cumulative round-by-round points.</p>",
            unsafe_allow_html=True,
        )

    with st.container(border=True, key="dialog_driver_select"):
        st.markdown("<p class='section-kicker'>Comparison Setup</p>", unsafe_allow_html=True)
        st.markdown("<h2>Select Drivers</h2>", unsafe_allow_html=True)
        current_year = 2025
        season_options = list(range(current_year, 1999, -1))
        selected_season = st.selectbox("SEASON", season_options, index=1)

        season_directory = get_drivers_for_season(int(selected_season))
        if season_directory.empty:
            st.error("No drivers found for the selected season.")
            return

        driver_names = season_directory["fullName"].tolist()
        if len(driver_names) < 2:
            st.error("Not enough drivers in this season for comparison.")
            return

        name_to_id = dict(zip(season_directory["fullName"], season_directory["driverId"]))

        default_one = driver_names[0]
        default_two = driver_names[1]

        col1, col2 = st.columns(2)

        with col1:
            driver_one = st.selectbox("DRIVER A", driver_names, index=0)

        with col2:
            alt_names = [name for name in driver_names if name != driver_one]
            alt_default = default_two if default_two in alt_names else alt_names[0]
            driver_two = st.selectbox("DRIVER B", alt_names, index=alt_names.index(alt_default))

    driver_one_id = name_to_id.get(driver_one)
    driver_two_id = name_to_id.get(driver_two)

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True, key="dialog_driver_profile_a"):
            st.markdown("<p class='section-kicker'>Driver A</p>", unsafe_allow_html=True)
            _render_driver_profile(driver_one_id)
    with col_b:
        with st.container(border=True, key="dialog_driver_profile_b"):
            st.markdown("<p class='section-kicker'>Driver B</p>", unsafe_allow_html=True)
            _render_driver_profile(driver_two_id)

    with st.container(border=True, key="dialog_driver_points_compare"):
        st.markdown("<p class='section-kicker'>Points Comparison</p>", unsafe_allow_html=True)
        st.markdown("<h2>Championship Points vs Races</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<p class='panel-note' style='color:#8e929b; font-size:20px;'>Running championship points by round for season {selected_season}.</p>",
            unsafe_allow_html=True,
        )

        series_a = _build_comparison_series(driver_one_id, driver_one, int(selected_season))
        series_b = _build_comparison_series(driver_two_id, driver_two, int(selected_season))

        if series_a.empty or series_b.empty:
            st.info("Selected season does not contain race data for both drivers.")
            return

        race_rounds = pd.concat(
            [series_a[["Round"]], series_b[["Round"]]],
            ignore_index=True,
        ).drop_duplicates()
        race_rounds = race_rounds.sort_values("Round").reset_index(drop=True)

        chart_df = race_rounds.copy()
        chart_df = chart_df.merge(series_a[["Round", driver_one]], how="left", on="Round")
        chart_df = chart_df.merge(series_b[["Round", driver_two]], how="left", on="Round")
        chart_df[driver_one] = pd.to_numeric(chart_df[driver_one], errors="coerce").ffill().fillna(0.0)
        chart_df[driver_two] = pd.to_numeric(chart_df[driver_two], errors="coerce").ffill().fillna(0.0)
        chart_df = chart_df.sort_values("Round").reset_index(drop=True)

        if chart_df.empty:
            st.info("No chart data available for the selected drivers and season.")
            return

        race_names = pd.concat(
            [
                series_a[["Round", "RaceName"]],
                series_b[["Round", "RaceName"]],
            ],
            ignore_index=True,
        )
        race_names = race_names.sort_values("Round").drop_duplicates(subset=["Round"], keep="first")
        chart_df = chart_df.merge(race_names, how="left", on="Round")
        chart_df["RaceName"] = chart_df["RaceName"].fillna("Unknown Race")

        long_df = chart_df.melt(
            id_vars=["Round", "RaceName"],
            value_vars=[driver_one, driver_two],
            var_name="Driver",
            value_name="ChampionshipPoints",
        )
        long_df = long_df.sort_values(["Driver", "Round"]).reset_index(drop=True)
        long_df["PointsGained"] = (
            long_df.groupby("Driver")["ChampionshipPoints"].diff().fillna(long_df["ChampionshipPoints"])
        )

        color_a = get_team_color(driver_one, default="#ff8000")
        color_b = get_team_color(driver_two, default="#1e41ff")
        if color_a.lower() == color_b.lower():
            color_b = "#f5a623" if color_a != "#f5a623" else "#ffffff"

        try:
            import altair as alt

            hover = alt.selection_point(fields=["Round"], nearest=True, on="mouseover", empty=False)

            color_scale = alt.Scale(domain=[driver_one, driver_two], range=[color_a, color_b])

            line = (
                alt.Chart(long_df)
                .mark_line(strokeWidth=3)
                .encode(
                    x=alt.X("Round:Q", axis=alt.Axis(title="Race Round", tickMinStep=1, labelAngle=0, labelColor="#8b949e", titleColor="#f0f3f6", gridColor="#262c36")),
                    y=alt.Y("ChampionshipPoints:Q", axis=alt.Axis(title="Championship Points", labelColor="#8b949e", titleColor="#f0f3f6", gridColor="#262c36")),
                    color=alt.Color("Driver:N", scale=color_scale, legend=alt.Legend(title="Driver", labelColor="#f0f3f6", titleColor="#ffffff")),
                )
            )

            points = (
                alt.Chart(long_df)
                .mark_circle(size=70)
                .encode(
                    x="Round:Q",
                    y="ChampionshipPoints:Q",
                    color=alt.Color("Driver:N", scale=color_scale),
                    tooltip=[
                        alt.Tooltip("Driver:N", title="Driver"),
                        alt.Tooltip("Round:Q", title="Round", format=".0f"),
                        alt.Tooltip("RaceName:N", title="Race"),
                        alt.Tooltip("ChampionshipPoints:Q", title="Total Points", format=".1f"),
                        alt.Tooltip("PointsGained:Q", title="Round Points", format=".1f"),
                    ],
                    opacity=alt.condition(hover, alt.value(1.0), alt.value(0.7)),
                )
                .add_params(hover)
            )

            rule = (
                alt.Chart(long_df)
                .mark_rule(color="#e10600", strokeDash=[4, 4], opacity=0.7)
                .encode(x="Round:Q")
                .transform_filter(hover)
            )

            interactive_chart = (
                (line + points + rule)
                .properties(
                    height=460,
                    title=f"{selected_season} Championship Points Progression",
                )
                .configure_view(strokeWidth=0)
                .configure_title(color="#f0f3f6", font="monospace", fontSize=13)
                .interactive()
            )

            st.altair_chart(interactive_chart, use_container_width=True)
            st.caption("Hover points for round details. Drag to pan and use scroll to zoom.")
            return
        except Exception:
            pass

        # Matplotlib fallback
        fig, ax = plt.subplots(figsize=(11, 5.2))
        fig.patch.set_facecolor("#161b22")
        ax.set_facecolor("#161b22")

        ax.plot(
            chart_df["Round"],
            chart_df[driver_one],
            marker="o",
            markersize=6,
            linewidth=2.4,
            color=color_a,
            label=driver_one,
            zorder=3,
        )
        ax.plot(
            chart_df["Round"],
            chart_df[driver_two],
            marker="o",
            markersize=6,
            linewidth=2.4,
            color=color_b,
            label=driver_two,
            zorder=3,
        )

        ax.set_title(
            f"{selected_season} Championship Points Progression",
            color="#f0f3f6",
            fontsize=12,
            pad=10,
            fontweight="bold",
        )
        ax.set_xlabel("Race Round", color="#8b949e", fontsize=10)
        ax.set_ylabel("Championship Points", color="#8b949e", fontsize=10)

        for spine in ax.spines.values():
            spine.set_color("#262c36")

        ax.tick_params(axis="x", colors="#8b949e", labelsize=9)
        ax.tick_params(axis="y", colors="#8b949e", labelsize=9)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        y_max = float(max(chart_df[driver_one].max(), chart_df[driver_two].max(), 1.0))
        y_step = 5 if y_max <= 60 else 10
        ax.yaxis.set_major_locator(MultipleLocator(y_step))

        x_min = int(chart_df["Round"].min()) if not chart_df.empty else 1
        x_max = int(chart_df["Round"].max()) if not chart_df.empty else 1
        ax.set_xlim(max(1, x_min - 0.3), x_max + 0.3)
        ax.set_ylim(0, y_max * 1.08)

        ax.grid(which="major", color="#262833", linestyle="--", linewidth=0.8, alpha=0.5)
        ax.set_axisbelow(True)

        ax.legend(
            loc="upper left",
            frameon=True,
            facecolor="#161820",
            edgecolor="#262833",
            labelcolor="#f5f5f7",
            fontsize=9,
        )

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


render_page()
