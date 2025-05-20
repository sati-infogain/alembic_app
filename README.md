# FastAPI + SQLAlchemy + Alembic Project Setup

This project demonstrates a modular FastAPI application with SQLAlchemy models, Alembic migrations, and a service layer for clean architecture. It supports many-to-many relationships, UUID primary keys, and includes seed data and API documentation.

---

## 1. **Project Setup**

### **Clone and Install Dependencies**

```sh
git clone <your-repo-url>
cd <your-project-folder>
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

---

## 2. **Environment Configuration**

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+psycopg2://postgres:admin@localhost:5432/test
```

---

## 3. **Alembic Initialization and Configuration**

### **Initialize Alembic**

```sh
alembic init alembic
```

### **Configure Alembic**

- In `alembic.ini`, set:
  ```
  sqlalchemy.url = postgresql+psycopg2://postgres:admin@localhost:5432/test
  ```
- In `alembic/env.py`, import your models and set metadata:
  ```python
  from models.base import Base
  from models.user import User
  from models.flow import Flow
  from models.user_flows import user_flows
  target_metadata = Base.metadata
  ```

---

## 4. **Creating and Running Migrations**

### **Autogenerate a Migration**

```sh
alembic revision --autogenerate -m "Initial migration"
```

### **Apply Migrations**

```sh
alembic upgrade head
```

### **Rolling Back Migrations**

- To undo the last migration:
  ```sh
  alembic downgrade -1
  ```
- To downgrade to a specific revision:
  ```sh
  alembic downgrade <revision_id>
  ```

---

## 5. **Altering Schemas**

- **Modify your SQLAlchemy models** (add/remove columns, tables, relationships).
- **Autogenerate and apply a new migration**:
  ```sh
  alembic revision --autogenerate -m "Describe your change"
  alembic upgrade head
  ```

---

## 6. **Seeding the Database**

Create a `seed.py` script (example provided in this repo) to insert initial data:

```sh
python seed.py
```

---

## 7. **Project Structure**

```
.
├── api/
│   ├── users.py
│   ├── flows.py
│   └── user_flows.py
├── models/
│   ├── base.py
│   ├── user.py
│   ├── flow.py
│   └── user_flows.py
├── service/
│   ├── user_service.py
│   ├── flow_service.py
│   └── user_flows_service.py
├── db.py
├── main.py
├── seed.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
└── .env
```

---

## 8. **Running the API**

```sh
uvicorn main:app --reload
```

- **Swagger/OpenAPI docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 9. **Build, Compile, and Run**

- **No compilation needed** (Python project).
- Use `uvicorn` for development and production.
- For production, consider using a process manager (e.g., Gunicorn with Uvicorn workers).

---

## 10. **Best Practices**

- Use the `service/` layer for all DB logic.
- Keep models, API routers, and services modular.
- Use Alembic for all schema changes.
- Use `.env` for secrets and configuration.
- Write and run seed scripts for test data.

---

## 11. **API Usage**

- All endpoints are documented in Swagger UI.
- Example endpoints:
  - `POST /users/` - Create user
  - `GET /users/` - List users
  - `POST /flows/` - Create flow
  - `POST /user_flows/` - Associate user and flow

---

## 12. **SPI (Service Provider Interface) Details**

- The `service/` modules act as the SPI between your API layer and the database.
- All business logic and DB access are encapsulated in these service modules.
- API routers only call service functions, never access the DB session directly.

---

**You're ready to develop, migrate, seed, and run your FastAPI project with best practices!**