from src.simulation import Simulation
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Union



def get_simulation_params() -> Dict[str, Union[int, float]]:
    st.subheader("Simulation parameters")
    simulation_params: Dict[str, Union[int, float]] = dict()
    simulation_params["population_size"] = int(st.number_input("Population", min_value=0, value=50, step=1))
    simulation_params["initial_sick"] = int(st.number_input("Sick people", min_value=0, max_value=simulation_params["population_size"], value=1, step=1))
    simulation_params["number_of_frames"] = int(st.number_input("Steps", min_value=0, value=10))
    simulation_params["contact_radius"] = st.slider("Contact range", min_value=0.0, max_value=1.0, value=0.03, step=0.01)
    return simulation_params

def get_person_params() -> Dict[str, Union[int, float]]:
    st.subheader("Person parameters")
    person_params: Dict[str, Union[int, float]] = dict()
    person_params["recovery_chance"] = st.number_input("Recovery Chance", min_value=0.0, max_value=1.0, step=0.01, value=0.03)
    person_params["immunity"] = int(st.number_input("Immunity", min_value=0, max_value=1, value=0, step=1))
    person_params["immunity_decrease_ratio"] = st.slider("Immunity decrease ratio", min_value=0.0, max_value=1.0, value=0.03)
    return person_params

def plot_animation(df):
    chart = alt.Chart(df) \
        .mark_circle(size=60) \
        .encode(x='x', y='y', color='c') \
        .properties(title="Simulation",
                    width=800, 
                    height=800) \
        .interactive()
    return chart


class Animation:
    
    def __init__(self, simulation):
        self.simulation = simulation
        self.chart = st.empty()
        self.frame_container= st.empty()
        self.color_encoding = {(0, 1, 0): "healthy",
                                (1, 0, 0): "sick",
                                (0.7, 0, 0.7): "recovered"}
    
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
        for i, frame in enumerate(self.simulation):
            self.frame_container.write(st.session_state.frame_idx)
            self.plot(frame)
            if st.session_state["frame_idx"] < self.simulation.population_size:
                st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1

        
    def stop(self):
        st.session_state["frame_idx"] = st.session_state["frame_idx"] - 1
        self.frame_container.write(st.session_state.frame_idx)
        stopped_frame = self.simulation[st.session_state["frame_idx"]]
        self.plot(stopped_frame)
      
    def next(self):
        st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1
        self.frame_container.write(st.session_state.frame_idx)
        st.progress(st.session_state["frame_idx"])
        next_frame = self.simulation[st.session_state["frame_idx"]]
        self.plot(next_frame)
    
    def previous(self):
        st.session_state["frame_idx"] = st.session_state["frame_idx"] - 1
        self.frame_container.write(st.session_state.frame_idx)
        st.progress(st.session_state["frame_idx"])
        previous_frame = self.simulation[st.session_state["frame_idx"]]
        self.plot(previous_frame)
        
    def resume(self):
        for i in range(st.session_state["frame_idx"], self.simulation.population_size + 1):
            self.frame_container.write(st.session_state.frame_idx)
            current_frame = self.simulation[i]
            self.plot(current_frame)
            if st.session_state["frame_idx"] < self.simulation.population_size:
                st.session_state["frame_idx"] = st.session_state["frame_idx"] + 1


    def plot(self, frame):
        x, y, c = frame
        df = pd.DataFrame({"x": x, "y": y, "c": c})
        color_encoding = {(0, 1, 0): "healthy",
                    (1, 0, 0): "sick",
                    (0.7, 0, 0.7): "recovered"}
        df["c"] = df["c"].apply(lambda x: color_encoding[x])
        scatter_chart = plot_animation(df)
        self.chart.write(scatter_chart)
        


@st.experimental_memo   
def create_simulation(simulation_params, person_kwargs):
    simulation = Simulation(**simulation_params, person_kwargs=person_kwargs)
    return simulation

if __name__ == "__main__":
    st.title("Epidemic Simulation")
    if "frame_idx" not in st.session_state:
        st.session_state.frame_idx = 0
    
    st.header("Set parameters")
    simulation_params = get_simulation_params()
    person_kwargs = get_person_params()
    simulation = create_simulation(simulation_params, person_kwargs)
    animation = Animation(simulation)
    
    st.header("Simulation")  
    col1, col2, col3, col4, col5 = st.columns([0.25, 0.25, 0.25, 0.25, 0.1])

    
    actions = {"start": col1.button("Start"),
                "pause": col2.button("Pause"),
                "resume": col3.button("Resume"),
                "next": col4.button("Next"),
                "previous": col5.button("Previous")
                }

    if any(actions.values()):
        current_action = list({action_name: action for action_name, action in actions.items() if action == True})[0]
        animation(current_action)

