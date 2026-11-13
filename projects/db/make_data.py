"""Writes fake data for the BabsonAI Labs database.

Run with: uv run python projects/db/make_data.py

It writes one CSV file per table into projects/db/data/. The random seed is
fixed, so running it again writes the exact same files.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # fixed seed so this script writes the same data every time

AS_OF = date(2026, 11, 8)  # the "today" this data is built around
WINDOW_START = AS_OF - timedelta(days=365)  # the 12 months the data covers

DATA_DIR = Path(__file__).parent / "data"

FIRST_NAMES = [
    "Olivia", "Liam", "Emma", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "Lucas", "Mia", "Elijah", "Charlotte", "James", "Amelia",
    "Benjamin", "Harper", "Henry", "Evelyn", "Alexander", "Abigail",
    "Michael", "Emily", "Daniel", "Ella",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris",
]
TITLE_LADDER = [
    "Associate", "Engineer", "Senior Engineer", "Manager", "Director",
]
PROJECT_CATEGORIES = ["LLM app", "data pipeline", "internal tool"]
PROJECT_STATUSES = ["planned", "active", "paused", "done"]
ROLES = ["engineer", "data scientist", "designer", "PM", "analyst"]
EXPENSE_CATEGORIES = ["GPU cloud", "data labeling", "software", "travel"]
CLIENT_NAMES = [
    "Acme Retail", "Northfield Bank", "Riverside Health", "Carter Logistics",
    "Bellwether Foods", "Hawkeye Insurance", "Summit Realty", "Union Freight",
]


def random_date(start, end):
    days_between = (end - start).days
    offset = random.randint(0, days_between)
    return start + timedelta(days=offset)


def random_weekday_date(start, end):
    # Builds the list of weekdays (Monday-Friday) between start and end, then
    # picks one at random, so a task's created_date lands on a business day
    # the way it would at a real company.
    candidates = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            candidates.append(current)
        current = current + timedelta(days=1)
    if len(candidates) == 0:
        return random_date(start, end)  # no weekday in range, fall back
    return random.choice(candidates)


def make_people():
    rows = []
    history_rows = []
    num_people = 25
    for person_id in range(1, num_people + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        start_date = random_date(WINDOW_START - timedelta(days=700), AS_OF - timedelta(days=30))

        if person_id <= 2:
            manager_id = ""  # the two founders report to nobody
        else:
            manager_id = random.randint(1, person_id - 1)  # always an earlier id, so a manager always loads first

        rows.append({
            "person_id": person_id,
            "first_name": first_name,
            "last_name": last_name,
            "start_date": start_date.isoformat(),
            "manager_id": manager_id,
        })

        # Position history: founders keep one title. Everyone else gets one
        # title to start, and about one in three get a second, later title
        # (with a new work email, since the scenario says emails change
        # with title).
        if person_id <= 2:
            titles = ["Founder"]
        else:
            rung = random.randint(0, len(TITLE_LADDER) - 2)
            titles = [TITLE_LADDER[rung]]
            if random.random() < 0.33:
                titles.append(TITLE_LADDER[rung + 1])

        effective_date = start_date
        for period, title in enumerate(titles):
            if period > 0:
                effective_date = random_date(effective_date + timedelta(days=60), AS_OF)
            email_name = f"{first_name.lower()}.{last_name.lower()}"
            if period > 0:
                email_name += str(period + 1)
            history_rows.append({
                "person_id": person_id,
                "effective_date": effective_date.isoformat(),
                "title": title,
                "work_email": f"{email_name}@babsonailabs.com",
            })

    return rows, history_rows


def make_projects():
    rows = []
    num_projects = 14
    for project_id in range(1, num_projects + 1):
        category = random.choice(PROJECT_CATEGORIES)
        if category == "internal tool":
            client_name = ""
            name = f"Internal Tool {project_id}"
        else:
            client_name = random.choice(CLIENT_NAMES)
            name = f"{client_name} {category.title()}"
        start_date = random_date(WINDOW_START, AS_OF - timedelta(days=14))
        rows.append({
            "project_id": project_id,
            "name": name,
            "client_name": client_name,
            "category": category,
            "budget": round(random.uniform(20000, 450000), 2),
            "start_date": start_date.isoformat(),
            "status": random.choice(PROJECT_STATUSES),
        })
    return rows


def make_assignments(people, projects):
    rows = []
    # people_by_id lets us look up a person's start_date when picking a join date
    people_by_id = {}
    for person in people:
        people_by_id[person["person_id"]] = person

    # assignments_by_project tracks who is on each project, and the date they
    # joined it, so tasks can pick a valid assignee (and a created_date no
    # earlier than that person's join date) later
    assignments_by_project = {}
    for project in projects:
        project_id = project["project_id"]
        assignments_by_project[project_id] = []
        project_start = date.fromisoformat(project["start_date"])
        team_size = random.randint(2, 6)
        chosen_people = random.sample(people, team_size)
        for person in chosen_people:
            person_start = date.fromisoformat(person["start_date"])
            joined_earliest = max(project_start, person_start)
            if joined_earliest > AS_OF:
                continue
            joined_date = random_date(joined_earliest, AS_OF)
            rows.append({
                "person_id": person["person_id"],
                "project_id": project_id,
                "role": random.choice(ROLES),
                "hours_per_week": random.randint(1, 40),
                "joined_date": joined_date.isoformat(),
            })
            assignments_by_project[project_id].append({
                "person_id": person["person_id"],
                "joined_date": joined_date,
            })
    return rows, assignments_by_project


def make_tasks(projects, assignments_by_project, people_by_id):
    rows = []
    task_id = 1
    num_tasks = 700
    all_person_ids = []
    for project_id, team in assignments_by_project.items():
        for member in team:
            if member["person_id"] not in all_person_ids:
                all_person_ids.append(member["person_id"])

    # pick two task rows in advance to break the rule on purpose: their
    # assignee will be a real person who does not work on that task's project
    broken_rule_tasks = set(random.sample(range(1, num_tasks + 1), 2))
    broken_rows = []

    for task_id in range(1, num_tasks + 1):
        project = random.choice(projects)
        project_id = project["project_id"]
        project_start = date.fromisoformat(project["start_date"])
        team = assignments_by_project[project_id]
        team_ids = [member["person_id"] for member in team]

        # Pick the assignee first, then bound created_date by whatever makes
        # that choice valid: a team member can't have a task before they
        # joined the project, and someone off the project's team (the
        # on-purpose broken rows) still can't have a task before they
        # started at the company.
        if task_id in broken_rule_tasks:
            # assign to someone real, but not on this project's team
            other_people = [p for p in all_person_ids if p not in team_ids]
            if other_people:
                assignee_id = random.choice(other_people)
                broken_rows.append(task_id)
                person_start = date.fromisoformat(people_by_id[assignee_id]["start_date"])
                earliest = max(project_start, person_start)
            else:
                assignee_id = ""
                earliest = project_start
        elif team_ids and random.random() > 0.15:
            member = random.choice(team)
            assignee_id = member["person_id"]
            earliest = max(project_start, member["joined_date"])
        else:
            assignee_id = ""  # about 15% of tasks start unassigned
            earliest = project_start

        created_date = random_weekday_date(earliest, AS_OF)
        due_date = created_date + timedelta(days=random.randint(3, 45))

        if due_date < AS_OF and random.random() < 0.6:
            completed_date = random_date(created_date, min(due_date, AS_OF))
        else:
            completed_date = ""

        rows.append({
            "task_id": task_id,
            "project_id": project_id,
            "assignee_id": assignee_id,
            "description": f"Task {task_id} for project {project_id}",
            "created_date": created_date.isoformat(),
            "due_date": due_date.isoformat(),
            "completed_date": completed_date.isoformat() if completed_date else "",
        })

    print(f"Rows that break the 'assignee works on its project' rule on purpose: tasks {broken_rows}")
    return rows


def make_expenses(projects):
    rows = []
    num_expenses = 300

    # a project that is only "planned" hasn't started real work yet, so it
    # shouldn't have any spending recorded against it
    spending_projects = []
    for project in projects:
        if project["status"] != "planned":
            spending_projects.append(project)

    for expense_id in range(1, num_expenses + 1):
        project = random.choice(spending_projects)
        project_start = date.fromisoformat(project["start_date"])
        expense_date = random_date(project_start, AS_OF)
        rows.append({
            "expense_id": expense_id,
            "project_id": project["project_id"],
            "expense_date": expense_date.isoformat(),
            "amount": round(random.uniform(50, 15000), 2),
            "category": random.choice(EXPENSE_CATEGORIES),
            "note": "",
        })
    return rows


def write_csv(file_name, rows, field_names):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / file_name
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {len(rows)} rows to {path}")


def main():
    people, history_rows = make_people()
    people_by_id = {person["person_id"]: person for person in people}
    projects = make_projects()
    assignment_rows, assignments_by_project = make_assignments(people, projects)
    task_rows = make_tasks(projects, assignments_by_project, people_by_id)
    expense_rows = make_expenses(projects)

    write_csv("person.csv", people, ["person_id", "first_name", "last_name", "start_date", "manager_id"])
    write_csv("position_history.csv", history_rows, ["person_id", "effective_date", "title", "work_email"])
    write_csv("project.csv", projects, ["project_id", "name", "client_name", "category", "budget", "start_date", "status"])
    write_csv("assignment.csv", assignment_rows, ["person_id", "project_id", "role", "hours_per_week", "joined_date"])
    write_csv("task.csv", task_rows, ["task_id", "project_id", "assignee_id", "description", "created_date", "due_date", "completed_date"])
    write_csv("expense.csv", expense_rows, ["expense_id", "project_id", "expense_date", "amount", "category", "note"])


if __name__ == "__main__":
    main()
