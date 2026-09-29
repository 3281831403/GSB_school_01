"""学校核心逻辑：学生、班级、教材和学分。"""

import json


def new_game():
    return {"students": {}, "class_load": 0, "class_capacity": 2, "books": 100, "credits": 0, "day": 1, "student_id": 0, "absent_teachers": ["T2"]}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def register(state, student_id):
    if student_id in state["students"]:
        return False
    state["students"][student_id] = {"credits": 0}
    return True


def enroll(state, student_id):
    if state["class_load"] >= state["class_capacity"]:
        return False
    state["class_load"] += 1
    return True


def fee(state, student_id, end_day):
    return end_day - state["day"]


def cancel_course(state, student_id):
    state["books"] = min(100, state["books"] + 10)
    return True


def assign_teacher(state, student_id, teacher):
    if teacher in state.get("absent_teachers", []):
        return False
    state["students"][student_id]["teacher"] = teacher
    return True


def exam(state, student_id):
    if state["students"][student_id].get("failed"):
        return False
    state["credits"] += 1
    return True


def absence(state, student_id):
    state["students"][student_id]["credits"] -= 1
    return True


def main():
    print("学校 - 命令: register/enroll/fee/cancel/teacher/exam/absence/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
