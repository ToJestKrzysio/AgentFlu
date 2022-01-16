from src.simulation import Simulation
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Union, Tuple
import time


def get_simulation_params() -> Tuple[Dict[str, Union[int, float]], Dict[str, Union[int, float]]]:
    st.subheader("Simulation parameters")
    simulation_params: Dict[str, Union[int, float]] = dict()
    simulation_params["population_size"] = int(st.number_input(
        "Population", min_value=0, value=620, max_value=2000, step=10))
    simulation_params["initial_sick"] = int(st.number_input(
        "Sick people", min_value=0, max_value=50, value=10, step=1))
    simulation_params["number_of_frames"] = int(st.number_input(
        "Steps", min_value=0, value=60, step=5))
    simulation_params["contact_radius"] = st.number_input(
        "Contact range [m]", min_value=0, max_value=20, value=3, step=1)

    st.subheader("Person parameters")
    person_params: Dict[str, Union[int, float]] = dict()
    person_params["recovery_chance"] = st.number_input(
        "Recovery Chance", min_value=0.0, max_value=1.0, step=0.01, value=0.01)
    person_params["immunity"] = st.number_input(
        "Initial Immunity", min_value=0.0, max_value=1.0, value=0.0, step=0.005)
    person_params["immunity_decrease_ratio"] = st.number_input(
        "Immunity Decrease Ratio", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    person_params["incubation_period"] = int(st.number_input(
        "Incubation Period", min_value=0, max_value=30, value=20, step=1))
    person_params["mobility_min"] = st.number_input(
        "Lowest Mobility", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    person_params["mobility_max"] = st.number_input(
        "Highest Mobility", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

    return simulation_params, person_params


def plot_animation(df):
    chart = alt.Chart(df) \
        .mark_circle(size=60) \
        .encode(x='x', y='y', color='c') \
        .properties(title="Simulation",
                    width=640,
                    height=480) \
        .interactive()
    return chart


def plot_status(df):
    lines = alt.Chart(df).mark_line().encode(
        x=alt.X('Status:Q', axis=alt.Axis(title='Steps')),
        y=alt.Y('Count:Q', axis=alt.Axis(title='Number of people'),
                color="Status"),
    ).properties(
        width=600,
        height=300
    )
    return lines


class Animation:

    def __init__(self, simulation):
        self.simulation = simulation
        self.chart = st.empty()
        self.status = st.empty()
        self.frame_container = st.empty()

    def __call__(self, action):
        actions = {"start": self.start,
                   "pause": self.stop,
                   "resume": self.resume,
                   "next": self.next,
                   "previous": self.previous
                   }
        actions[action]()

    def start(self):
        st.session_state.frame_idx = 0
        for i in range(self.simulation.number_of_frames + 1):
            self.frame_container.write(st.session_state.frame_idx)
            self.chart.write(self.simulation.sim_animations[i])
            self.status.write(self.simulation.status_animations[i])
            time.sleep(0.1)
            if st.session_state["frame_idx"] < self.simulation.population_size:
                st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1

    def stop(self):
        # st.session_state["frame_idx"] = st.session_state["frame_idx"] - 1
        self.frame_container.write(st.session_state.frame_idx)
        self.chart.write(self.simulation.sim_animations[st.session_state["frame_idx"]])
        self.status.write(self.simulation.status_animations[st.session_state["frame_idx"]])

    def next(self):
        st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1
        self.frame_container.write(st.session_state.frame_idx)
        self.chart.write(self.simulation.sim_animations[st.session_state["frame_idx"]])
        self.status.write(self.simulation.status_animations[st.session_state["frame_idx"]])

    def previous(self):
        st.session_state["frame_idx"] = st.session_state["frame_idx"] - 1
        self.frame_container.write(st.session_state.frame_idx)
        self.chart.write(self.simulation.sim_animations[st.session_state["frame_idx"]])
        self.status.write(self.simulation.status_animations[st.session_state["frame_idx"]])

    def resume(self):
        for i in range(st.session_state["frame_idx"], self.simulation.population_size + 1):
            self.frame_container.write(st.session_state.frame_idx)
            self.chart.write(self.simulation.sim_animations[st.session_state["frame_idx"]])
            self.status.write(self.simulation.status_animations[st.session_state["frame_idx"]])
            if st.session_state["frame_idx"] < self.simulation.population_size:
                st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1


@st.experimental_memo(suppress_st_warning=True)
def create_simulation(simulation_params, person_kwargs):
    simulation = Simulation(**simulation_params, person_kwargs=person_kwargs)
    return simulation


def create_animation(simulation):
    animation = Animation(simulation)
    return animation


if __name__ == "__main__":
    st.title("Epidemic Simulation")
    if "frame_idx" not in st.session_state:
        st.session_state.frame_idx = 0

    st.header("Set parameters")
    simulation_params, person_kwargs = get_simulation_params()

    simulation = create_simulation(simulation_params, person_kwargs)
    animation = create_animation(simulation)

    col1, col2, col3, col4, col5 = st.columns([0.25, 0.25, 0.25, 0.25, 0.1])

    actions = {"start": col1.button("Start"),
               "pause": col2.button("Pause"),
               "resume": col3.button("Resume"),
               "next": col4.button("Next"),
               "previous": col5.button("Previous")
               }

    if any(actions.values()):
        current_action = \
        list({action_name: action for action_name, action in actions.items() if action == True})[0]
        animation(current_action)
