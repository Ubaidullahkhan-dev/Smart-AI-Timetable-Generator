# =========================================
# AI TIME TABLE GENERATOR USING STREAMLIT
# =========================================

# ---------- IMPORT LIBRARIES ----------

import streamlit as st
import random
import pandas as pd


# ---------- PAGE TITLE ----------

st.title("AI Time Table Generator")


# ---------- USER INPUT SECTION ----------

st.header("Enter Timetable Information")

# Subjects input
subjects_input = st.text_area(
    "Enter Subjects (comma separated)",
    "Math,Physics,Programming,English"
)

# Teachers input
teachers_input = st.text_area(
    "Enter Teachers (comma separated)",
    "Ali,Ahmed,Sara,Ayesha"
)

# Rooms input
rooms_input = st.text_area(
    "Enter Rooms (comma separated)",
    "R1,R2,Lab1"
)

# Days input
days_input = st.text_area(
    "Enter Days (comma separated)",
    "Monday,Tuesday,Wednesday,Thursday,Friday"
)

# Time slots input
slots_input = st.text_area(
    "Enter Time Slots (comma separated)",
    "9-10,10-11,11-12,1-2,2-3"
)


# ---------- CONVERT INPUTS TO LISTS ----------

SUBJECTS = [s.strip() for s in subjects_input.split(",")]

TEACHERS = [t.strip() for t in teachers_input.split(",")]

ROOMS = [r.strip() for r in rooms_input.split(",")]

DAYS = [d.strip() for d in days_input.split(",")]

TIME_SLOTS = [t.strip() for t in slots_input.split(",")]


# ---------- CREATE SUBJECT-TEACHER MAP ----------

teacher_map = {}

for i in range(min(len(SUBJECTS), len(TEACHERS))):
    teacher_map[SUBJECTS[i]] = TEACHERS[i]


# ---------- RANDOM TIMETABLE FUNCTION ----------

def create_random_timetable():

    timetable = {}

    for day in DAYS:

        timetable[day] = {}

        for slot in TIME_SLOTS:

            subject = random.choice(SUBJECTS)

            teacher = teacher_map[subject]

            room = random.choice(ROOMS)

            timetable[day][slot] = {
                "Subject": subject,
                "Teacher": teacher,
                "Room": room
            }

    return timetable


# ---------- CLASH DETECTION ----------

def calculate_clashes(timetable):

    clashes = 0

    for slot in TIME_SLOTS:

        used_teachers = []
        used_rooms = []

        for day in DAYS:

            lecture = timetable[day][slot]

            teacher = lecture["Teacher"]
            room = lecture["Room"]

            # Teacher clash
            if teacher in used_teachers:
                clashes += 1
            else:
                used_teachers.append(teacher)

            # Room clash
            if room in used_rooms:
                clashes += 1
            else:
                used_rooms.append(room)

    return clashes


# ---------- FITNESS FUNCTION ----------

def fitness(timetable):

    clashes = calculate_clashes(timetable)

    score = 100 - (clashes * 10)

    return score


# ---------- CREATE POPULATION ----------

def create_population(size):

    population = []

    for _ in range(size):

        timetable = create_random_timetable()

        population.append(timetable)

    return population


# ---------- SELECTION ----------

def selection(population):

    population.sort(key=fitness, reverse=True)

    return population[:2]


# ---------- CROSSOVER ----------

def crossover(parent1, parent2):

    child = {}

    for day in DAYS:

        if random.random() > 0.5:
            child[day] = parent1[day]
        else:
            child[day] = parent2[day]

    return child


# ---------- MUTATION ----------

def mutate(timetable):

    day = random.choice(DAYS)

    slot = random.choice(TIME_SLOTS)

    new_subject = random.choice(SUBJECTS)

    timetable[day][slot]["Subject"] = new_subject

    timetable[day][slot]["Teacher"] = teacher_map[new_subject]

    timetable[day][slot]["Room"] = random.choice(ROOMS)

    return timetable


# ---------- GENETIC ALGORITHM ----------

def genetic_algorithm(generations=100, population_size=10):

    population = create_population(population_size)

    for generation in range(generations):

        parents = selection(population)

        new_population = []

        for _ in range(population_size):

            child = crossover(parents[0], parents[1])

            child = mutate(child)

            new_population.append(child)

        population = new_population

    best = selection(population)[0]

    return best


# ---------- DISPLAY TIMETABLE ----------

def display_timetable(timetable):

    data = []

    for day in DAYS:

        for slot in TIME_SLOTS:

            lecture = timetable[day][slot]

            data.append({
                "Day": day,
                "Time Slot": slot,
                "Subject": lecture["Subject"],
                "Teacher": lecture["Teacher"],
                "Room": lecture["Room"]
            })

    df = pd.DataFrame(data)

    st.dataframe(df)


# ---------- GENERATE BUTTON ----------

if st.button("Generate Timetable"):

    best_timetable = genetic_algorithm()

    st.success("Timetable Generated Successfully")

    # Display fitness score
    st.subheader("Fitness Score")

    st.write(fitness(best_timetable))

    # Display timetable
    st.subheader("Generated Timetable")

    display_timetable(best_timetable)