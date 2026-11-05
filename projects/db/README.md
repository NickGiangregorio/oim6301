# Database Project

## 1. The Scenario

A · BabsonAI Labs. BabsonAI Labs is a startup founded by Babson students that builds AI tools for small businesses. It has about 25 people and tracks its work in spreadsheets and chat threads. The founders want to see who works on what, where the money goes, and who is overloaded.

## 2. The ERD

```mermaid
erDiagram
  PERSON ||--o{ POSITION_HISTORY : has
  PERSON ||--o{ ASSIGNMENT : works_on
  PERSON |o--o{ TASK : assigned_to
  PERSON ||--o{ PERSON : manages
  PROJECT ||--o{ ASSIGNMENT : includes
  PROJECT ||--o{ TASK : has
  PROJECT ||--o{ EXPENSE : incurs

  PERSON {
    int person_id PK
    string first_name
    string last_name
    date start_date
    int manager_id FK
  }

  POSITION_HISTORY {
    int person_id PK, FK
    date effective_date PK
    string title
    string work_email
  }

  PROJECT {
    int project_id PK
    string name
    string client_name
    string category
    decimal budget
    date start_date
    string status
  }

  ASSIGNMENT {
    int person_id PK, FK
    int project_id PK, FK
    string role
    int hours_per_week
    date joined_date
  }

  TASK {
    int task_id PK
    int project_id FK
    int assignee_id FK
    string description
    date created_date
    date due_date
    date completed_date
  }

  EXPENSE {
    int expense_id PK
    int project_id FK
    date expense_date
    decimal amount
    string category
    string note
  }
```

## 3. What One Row Means

- **PERSON:** one employee. A row is a single person at BabsonAI Labs, with their name, start date and who they report to. There are about 25 rows.
- **POSITION_HISTORY:** one period in a person's career at the company. A row says "starting on this date, this person held this title and used this work email." A person who has changed title has several rows, and the latest one is their current title and email.
- **PROJECT:** one piece of work the company does. A row is a single project, with its client (if any), category, budget and status.
- **ASSIGNMENT:** one person working on one project. A row says "this person is on this project, in this role, committing this many hours a week since this date." It is the link between people and projects, so a person on three projects has three rows.
- **TASK:** one unit of work inside a project. A row is a single task, with who it's assigned to (or no one yet), when it was created and due, and when it was finished (empty until then).
- **EXPENSE:** one money spent on a project. A row is a single charge, with its date, amount, category and a short note.

## 4. Design Choices
