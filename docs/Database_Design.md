# Uni_Find — Database Design

## 1. Overview

Uni_Find is a university Lost & Found system designed to help students and staff report, search for, and recover lost and found items within the university community.

The database stores information about users, lost items, found items, item categories, and communication between users. It also maintains the status of reported items so that the system can track the recovery process.

The database is implemented using **PostgreSQL**, while **SQLAlchemy** is used in the FastAPI backend to communicate with the database.

---

# 2. Database Management System

The system uses:

* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Backend:** FastAPI
* **Database Migration Tool:** Alembic
* **Database Driver:** psycopg2-binary

Database name:

```text
unifind
```

---

# 3. Main Entities

The main entities of the Uni_Find database are:

1. User
2. Category
3. Lost Item
4. Found Item
5. Message

These entities support the main Lost & Found workflow of the system.

---

# 4. Entity Relationship Overview

The main relationships are:

```text
User
 │
 ├───────────────┐
 │               │
 │               │
 ▼               ▼
Lost Item      Found Item
 │               │
 │               │
 └───────┬───────┘
         │
         ▼
      Category


User
 │
 └───────────────┐
                 │
                 ▼
              Message
                 ▲
                 │
                 │
                 User
```

A user can report multiple lost or found items.

An item belongs to a category.

Users can communicate with each other through messages regarding lost or found items.

---

# 5. User Table

The `users` table stores registered users of the Uni_Find system.

## Attributes

| Attribute     | Data Type | Constraints      | Description                             |
| ------------- | --------- | ---------------- | --------------------------------------- |
| id            | Integer   | Primary Key      | Unique identifier for the user          |
| name          | VARCHAR   | NOT NULL         | User's name                             |
| email         | VARCHAR   | UNIQUE, NOT NULL | University/user email address           |
| password_hash | VARCHAR   | NOT NULL         | Hashed user password                    |
| created_at    | TIMESTAMP | NOT NULL         | Account creation time                   |
| is_active     | BOOLEAN   | NOT NULL         | Indicates whether the account is active |

## Purpose

The user table provides authentication and identifies the person who reports or interacts with an item.

A user can:

* Report a lost item
* Report a found item
* View their reports
* Communicate with other users
* Manage their account

---

# 6. Category Table

The `categories` table stores categories used to classify lost and found items.

Examples include:

* Electronics
* Documents
* Clothing
* Accessories
* Books
* Keys
* Other

## Attributes

| Attribute   | Data Type | Constraints      | Description                 |
| ----------- | --------- | ---------------- | --------------------------- |
| id          | Integer   | Primary Key      | Unique category identifier  |
| name        | VARCHAR   | UNIQUE, NOT NULL | Category name               |
| description | TEXT      | NULL             | Description of the category |

## Purpose

Categories make it easier to organize and search for lost and found items.

---

# 7. Lost Item Table

The `lost_items` table stores reports submitted by users who have lost an item.

## Attributes

| Attribute   | Data Type | Constraints | Description                      |
| ----------- | --------- | ----------- | -------------------------------- |
| id          | Integer   | Primary Key | Unique lost item identifier      |
| user_id     | Integer   | Foreign Key | User who reported the item       |
| category_id | Integer   | Foreign Key | Category of the item             |
| title       | VARCHAR   | NOT NULL    | Short title of the lost item     |
| description | TEXT      | NOT NULL    | Detailed description             |
| location    | VARCHAR   | NOT NULL    | Location where the item was lost |
| lost_date   | DATE      | NOT NULL    | Date the item was lost           |
| image_url   | VARCHAR   | NULL        | Optional image of the item       |
| status      | VARCHAR   | NOT NULL    | Current status of the report     |
| created_at  | TIMESTAMP | NOT NULL    | Report creation time             |
| updated_at  | TIMESTAMP | NULL        | Last update time                 |

## Possible Status Values

```text
ACTIVE
MATCHED
RECOVERED
CLOSED
```

## Relationships

Each lost item:

* Belongs to one user
* Belongs to one category

One user can report multiple lost items.

One category can contain multiple lost items.

---

# 8. Found Item Table

The `found_items` table stores reports submitted by users who have found an item.

## Attributes

| Attribute   | Data Type | Constraints | Description                       |
| ----------- | --------- | ----------- | --------------------------------- |
| id          | Integer   | Primary Key | Unique found item identifier      |
| user_id     | Integer   | Foreign Key | User who reported the found item  |
| category_id | Integer   | Foreign Key | Category of the item              |
| title       | VARCHAR   | NOT NULL    | Short title of the found item     |
| description | TEXT      | NOT NULL    | Detailed description              |
| location    | VARCHAR   | NOT NULL    | Location where the item was found |
| found_date  | DATE      | NOT NULL    | Date the item was found           |
| image_url   | VARCHAR   | NULL        | Optional image of the item        |
| status      | VARCHAR   | NOT NULL    | Current status of the report      |
| created_at  | TIMESTAMP | NOT NULL    | Report creation time              |
| updated_at  | TIMESTAMP | NULL        | Last update time                  |

## Possible Status Values

```text
AVAILABLE
MATCHED
RETURNED
CLOSED
```

## Relationships

Each found item:

* Belongs to one user
* Belongs to one category

One user can report multiple found items.

One category can contain multiple found items.

---

# 9. Message Table

The `messages` table stores communication between users.

This allows the owner of a lost item and the person who found an item to communicate.

## Attributes

| Attribute     | Data Type | Constraints       | Description                            |
| ------------- | --------- | ----------------- | -------------------------------------- |
| id            | Integer   | Primary Key       | Unique message identifier              |
| sender_id     | Integer   | Foreign Key       | User sending the message               |
| receiver_id   | Integer   | Foreign Key       | User receiving the message             |
| lost_item_id  | Integer   | Foreign Key, NULL | Related lost item                      |
| found_item_id | Integer   | Foreign Key, NULL | Related found item                     |
| content       | TEXT      | NOT NULL          | Message content                        |
| is_read       | BOOLEAN   | NOT NULL          | Indicates whether the message was read |
| created_at    | TIMESTAMP | NOT NULL          | Message creation time                  |

## Purpose

Messages allow users to communicate about an item without exposing unnecessary personal contact information.

Example:

```text
Owner
  |
  | "I think this is my wallet."
  |
  ▼
Uni_Find
  |
  ▼
Finder
```

---

# 10. Relationships

## 10.1 User → Lost Items

One user can report many lost items.

```text
User 1 ──────────── * LostItem
```

Foreign key:

```text
lost_items.user_id → users.id
```

---

## 10.2 User → Found Items

One user can report many found items.

```text
User 1 ──────────── * FoundItem
```

Foreign key:

```text
found_items.user_id → users.id
```

---

## 10.3 Category → Lost Items

One category can contain many lost item reports.

```text
Category 1 ──────────── * LostItem
```

Foreign key:

```text
lost_items.category_id → categories.id
```

---

## 10.4 Category → Found Items

One category can contain many found item reports.

```text
Category 1 ──────────── * FoundItem
```

Foreign key:

```text
found_items.category_id → categories.id
```

---

## 10.5 User → Messages

A user can send many messages.

A user can also receive many messages.

```text
User 1 ──────────── * Message
User 1 ──────────── * Message
```

The two relationships are represented by:

```text
messages.sender_id
messages.receiver_id
```

---

# 11. Primary Keys

Every major entity uses an integer primary key:

```text
users.id
categories.id
lost_items.id
found_items.id
messages.id
```

Primary keys uniquely identify each record.

---

# 12. Foreign Keys

Foreign keys establish relationships between tables.

```text
lost_items.user_id
        ↓
users.id
```

```text
lost_items.category_id
        ↓
categories.id
```

```text
found_items.user_id
        ↓
users.id
```

```text
found_items.category_id
        ↓
categories.id
```

```text
messages.sender_id
        ↓
users.id
```

```text
messages.receiver_id
        ↓
users.id
```

---

# 13. Simplified ER Diagram

```text
                         ┌──────────────┐
                         │    USERS     │
                         ├──────────────┤
                         │ id PK        │
                         │ name         │
                         │ email        │
                         │ password_hash│
                         │ created_at   │
                         │ is_active    │
                         └──────┬───────┘
                                │
                ┌───────────────┼────────────────┐
                │               │                │
                │               │                │
                ▼               ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │ LOST_ITEMS   │ │ FOUND_ITEMS  │ │   MESSAGES   │
        ├──────────────┤ ├──────────────┤ ├──────────────┤
        │ id PK        │ │ id PK        │ │ id PK        │
        │ user_id FK   │ │ user_id FK   │ │ sender_id FK │
        │ category_id  │ │ category_id  │ │ receiver_id  │
        │ title        │ │ title        │ │ content      │
        │ description  │ │ description  │ │ created_at   │
        │ location     │ │ location     │ └──────────────┘
        │ lost_date    │ │ found_date   │
        │ status       │ │ status       │
        └──────┬───────┘ └──────┬───────┘
               │                │
               └────────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  CATEGORIES  │
                 ├──────────────┤
                 │ id PK        │
                 │ name         │
                 │ description  │
                 └──────────────┘
```

---

# 14. Database Design Principles

The Uni_Find database follows these principles:

### 14.1 Data Integrity

Primary keys and foreign keys are used to maintain valid relationships between records.

### 14.2 Avoiding Duplicate Data

Common information such as user details and category information is stored separately rather than repeatedly in item records.

### 14.3 Security

Passwords are stored as hashes rather than plain-text passwords.

### 14.4 Scalability

The database structure allows additional features and entities to be added later without redesigning the entire database.

### 14.5 Timestamps

Important records include timestamps to track when reports and messages were created or updated.

---

# 15. SQLAlchemy Implementation

The database tables will be represented as SQLAlchemy models.

The structure will be approximately:

```text
backend/app/models/
├── user.py
├── category.py
├── lost_item.py
├── found_item.py
└── message.py
```

Each model will inherit from the SQLAlchemy `Base`:

```python
class User(Base):
    ...
```

The models will use the database configuration defined in:

```text
backend/app/database/database.py
```

and the SQLAlchemy `Base` defined in:

```text
backend/app/database/base.py
```

---

# 16. Database Migration

Alembic will be used to manage database schema changes.

The development workflow will be:

```text
SQLAlchemy Model
       ↓
Alembic Migration
       ↓
PostgreSQL
       ↓
Database Table
```

This allows database changes to be tracked safely throughout development.

---

# 17. Future Considerations

Additional database entities may be introduced if required by the system requirements, such as:

* Item matching records
* Notifications
* User verification
* Reports
* Audit logs

These should only be added when they are required by the Uni_Find functional requirements.
