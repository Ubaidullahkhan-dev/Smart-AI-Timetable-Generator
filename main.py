import os
import random
from flask import Flask, render_template_string

app = Flask(__name__)

# Core data structures for the timetable generator
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "01:00 - 02:00", "02:00 - 03:00"]

COURSES = {
    "CS101": {"name": "Introduction to AI", "lectures_per_week": 3, "instructor": "Dr. Smith"},
    "CS102": {"name": "Data Structures", "lectures_per_week": 3, "instructor": "Prof. Johnson"},
    "CS103": {"name": "Machine Learning", "lectures_per_week": 2, "instructor": "Dr. Lee"},
    "CS104": {"name": "Database Systems", "lectures_per_week": 2, "instructor": "Prof. Davis"}
}

ROOMS = ["Room 101", "Room 102", "Lab 1"]

class TimetableGenerator:
    def __init__(self, courses, rooms, days, time_slots):
        self.courses = courses
        self.rooms = rooms
        self.days = days
        self.time_slots = time_slots

    def generate_schedule(self):
        schedule = []
        occupied_slots = set()
        instructor_slots = set()

        for course_code, course_info in self.courses.items():
            assigned_count = 0
            attempts = 0
            max_attempts = 100

            while assigned_count < course_info["lectures_per_week"] and attempts < max_attempts:
                attempts += 1
                day = random.choice(self.days)
                time_slot = random.choice(self.time_slots)
                room = random.choice(self.rooms)
                instructor = course_info["instructor"]

                room_conflict = (day, time_slot, room) in occupied_slots
                instructor_conflict = (day, time_slot, instructor) in instructor_slots

                if not room_conflict and not instructor_conflict:
                    occupied_slots.add((day, time_slot, room))
                    instructor_slots.add((day, time_slot, instructor))
                    schedule.append({
                        "Day": day,
                        "Time": time_slot,
                        "Course": f"{course_code} ({course_info['name']})",
                        "Instructor": instructor,
                        "Room": room
                    })
                    assigned_count += 1

        sorted_schedule = sorted(
            schedule, 
            key=lambda x: (self.days.index(x["Day"]), self.time_slots.index(x["Time"]))
        )
        return sorted_schedule


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Timetable Schedule</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 30px; }
        h1 { color: #333; text-align: center; }
        table { width: 90%; margin: 20px auto; border-collapse: collapse; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        th, td { padding: 12px 15px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #007bff; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .btn-container { text-align: center; margin-top: 20px; }
        .btn { padding: 10px 20px; background-color: #28a745; color: white; border: none; cursor: pointer; border-radius: 5px; text-decoration: none; }
        .btn:hover { background-color: #218838; }
    </style>
</head>
<body>
    <h1>AI Generated Timetable</h1>
    <table>
        <thead>
            <tr>
                <th>Day</th>
                <th>Time Slot</th>
                <th>Course</th>
                <th>Instructor</th>
                <th>Room</th>
            </tr>
        </thead>
        <tbody>
            {% for item in schedule %}
            <tr>
                <td>{{ item.Day }}</td>
                <td>{{ item.Time }}</td>
                <td>{{ item.Course }}</td>
                <td>{{ item.Instructor }}</td>
                <td>{{ item.Room }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="btn-container">
        <a href="/" class="btn">Regenerate Timetable</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    generator = TimetableGenerator(COURSES, ROOMS, DAYS, TIME_SLOTS)
    timetable = generator.generate_schedule()
    return render_template_string(HTML_TEMPLATE, schedule=timetable)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)