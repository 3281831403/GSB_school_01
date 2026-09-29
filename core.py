"""学校核心逻辑：学生、班级、教材和学分。"""

import json


BOOKS_PER_STUDENT = 10
ON_LEAVE_TEACHERS = frozenset({"T2"})


def new_game():
    return {
        "students": {},
        "class_load": 0,
        "class_capacity": 2,
        "enrolled": [],
        "books": 100,
        "credits": 0,
        "day": 1,
        "student_id": 0,
        "teachers_on_leave": sorted(ON_LEAVE_TEACHERS),
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    defaults = new_game()
    for key, value in defaults.items():
        state.setdefault(key, value)
    return state


def register(state, student_id):
    if student_id in state["students"]:
        return False
    state["students"][student_id] = {"credits": 0}
    return True


def enroll(state, student_id):
    enrolled = state.setdefault("enrolled", [])
    if student_id in enrolled:
        return False
    if state["class_load"] >= state["class_capacity"]:
        return False
    enrolled.append(student_id)
    state["class_load"] += 1
    return True


def fee(state, student_id, end_day):
    return max(0, end_day - state["day"])


def cancel_course(state, student_id):
    cancelled = state.setdefault("cancelled", [])
    if student_id in cancelled:
        return False
    cancelled.append(student_id)
    enrolled = state.setdefault("enrolled", [])
    if student_id in enrolled:
        enrolled.remove(student_id)
        state["class_load"] = max(0, state["class_load"] - 1)
    state["books"] += BOOKS_PER_STUDENT
    return True


def assign_teacher(state, student_id, teacher):
    if student_id not in state["students"]:
        return False
    if teacher in state.get("teachers_on_leave", ON_LEAVE_TEACHERS):
        return False
    state["students"][student_id]["teacher"] = teacher
    return True


def exam(state, student_id):
    if state["students"][student_id].get("failed"):
        return False
    state["credits"] += 1
    return True


def absence(state, student_id):
    if student_id not in state["students"]:
        return False
    student = state["students"][student_id]
    if student.get("absent_today"):
        return False
    student["absent_today"] = True
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
