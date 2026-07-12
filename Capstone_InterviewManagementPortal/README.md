# Interview Management Portal

A web application for managing the complete hiring pipeline. HR creates job openings, registers candidates, uploads resumes and schedules interviews. Interviewers submit structured feedback with ratings, and the candidate's status moves automatically based on the recommendation. Admins manage user accounts, and both HR and interviewers get their own dashboard.

Built as a capstone project with FastAPI, MongoDB and React.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.10+ |
| Database | MongoDB (resumes stored in GridFS) |
| Auth | JWT bearer tokens, bcrypt password hashing |
| Frontend | React 19, React Router 7, Axios |
| Testing | Pytest + pytest-cov (runs on in-memory mongomock, no local DB needed) |
| API docs | Swagger UI at `/api/docs` |

## Getting started

### Prerequisites

- Python 3.10 or newer
- Node.js 18+
- MongoDB running locally on the default port (only needed to run the app, tests don't need it)

### Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
copy .env.example .env       # adjust values if needed

# creates the initial admin account (admin@nucleusteq.com / admin123)
python -m src.seed

uvicorn src.main:app --reload
```

API runs at `http://localhost:8000`, Swagger docs at `http://localhost:8000/api/docs`.

### Frontend setup

```bash
cd frontend
npm install
npm start
```

Opens at `http://localhost:3000` and talks to the backend on port 8000.

## Testing and code coverage

```bash
cd backend
pytest                  # run all tests
pytest --cov=src        # run with coverage report
```

The test suite uses mongomock (an in-memory MongoDB), so it runs on any machine or CI runner without a database installed.

**Current results: 55 tests passing, ~80% overall line coverage** (target from the spec is 80-90%).

Coverage by area (from `pytest --cov=src`):

| Area | Coverage | Notes |
|---|---|---|
| Services (business logic) | 52% - 100% | dashboard 100%, interview 98%, feedback 97% |
| Routers | 75% - 100% | dashboard, feedback, interview at 100% |
| Repositories | 61% - 90% | feedback and interview repos at 90% |
| Schemas (request/response) | 60% - 100% | all response schemas at 100% |
| Core (config, security, middleware) | 50% - 100% | middleware 84%, security 80% |
| Enums / constants / utils | 100% | |
| **Total** | **80%** | 1314 statements, 267 missed |

What the tests cover: login success and failure, first-login reset flow, old password rejection after reset, password hashing verification, user CRUD with DB-state assertions, default password behaviour, candidate CRUD with unique email/mobile checks, name and email character validation, resume upload validation (wrong extension, empty, too small, too big, fake PDF), resume download permissions per role, status history tracking, interview scheduling with role and double-booking checks, reassignment conflicts, feedback submission rules and both dashboards.

## Architecture

The backend follows a three-layer design:

```
Router  ->  Service  ->  Repository  ->  MongoDB
```

- **Routers** handle HTTP only: request parsing, role guards, response models. They never contain business logic and never raise exceptions themselves.
- **Services** hold the business rules: who can do what, status transitions, double-booking checks, assigned-interviewer checks.
- **Repositories** are the only layer that touches MongoDB (including GridFS for resume files).

Errors are raised as typed exceptions (`NotFoundException`, `ValidationException`, `DuplicateException`, etc.) anywhere in the stack and converted to a consistent JSON error response by a centralized exception handler. An auth middleware validates the JWT once per request for all protected paths; role checks are done per route since required roles differ per endpoint.

### Project structure

```
backend/
├── src/
│   ├── routers/          # HTTP endpoints, role guards
│   ├── services/         # business logic
│   ├── repositories/     # all MongoDB access (incl. GridFS)
│   ├── schemas/
│   │   ├── request/      # pydantic request models + validators
│   │   └── response/     # pydantic response models
│   ├── core/             # config, database client, security, middleware, dependencies
│   ├── enums/            # roles, statuses, recommendation values
│   ├── exceptions/       # typed exceptions + central handler
│   ├── utils/            # logger, small shared helpers
│   ├── main.py           # app factory, middleware, router registration
│   └── seed.py           # creates the initial admin account
├── tests/                # pytest suite (mongomock based)
├── requirements.txt
├── .env.example
└── .env                  # local only, not committed

frontend/
└── src/
    ├── pages/            # one component per screen
    ├── components/       # shared UI (inputs, buttons, alerts, layout, sidebar)
    ├── api/              # axios instance + per-module API services
    ├── hooks/            # shared hooks (e.g. delayed navigation)
    ├── constants/        # roles, candidate statuses, badge mappings
    ├── utils/            # validation, error handling, formatting helpers
    └── styles/           # global stylesheet (Kite-inspired theme)
```

## Roles and permissions

| Feature | Admin | HR | Interviewer |
|---|---|---|---|
| Dashboard | HR view | HR view | Own stats |
| Manage system users | Yes | No | No |
| Create / edit jobs | No | Yes | View only |
| Create / edit candidates, upload resumes | No | Yes | View assigned only |
| Download resume PDFs | No | Yes | Assigned candidates only |
| Schedule / edit / reassign interviews | No | Yes | Sees own only |
| Submit feedback and ratings | No | No | Own interviews, once each |
| Selection decision (Selected / Rejected) | No | Yes | Via recommendation only |

Admin is deliberately separated from hiring operations: it administers accounts and sees the metrics while HR owns the pipeline. All rules are enforced in the backend (service layer + route guards), not just hidden in the UI.

Other rules that hold everywhere:

- **First login forces a password reset.** New users are created with the default password `admin123` and cannot get a token until they change it.
- **Disabled accounts cannot log in**, even with the right password.
- **No double-booking.** Every interview has a start and end time, and an interviewer cannot be scheduled or reassigned into a time range that overlaps one of their existing scheduled interviews. Back-to-back interviews are fine; completed or cancelled ones free the slot. The scheduling form also filters the interviewer dropdown to whoever is actually free in the chosen window.
- **Feedback drives candidate status.** SELECT sets `SELECTED`, REJECT sets `REJECTED`, NEXT_ROUND sets `INTERVIEW_COMPLETED`. Every status change, manual or automatic, is recorded in the candidate's history with who changed it and when.
- **Newest first.** All listings (users, jobs, candidates, interviews) show the most recently created records on top.

## Candidate lifecycle

```
PROFILE_CREATED -> INTERVIEW_SCHEDULED -> INTERVIEW_COMPLETED -> SELECTED / REJECTED
```

History entries are written automatically at every step: profile creation, interview scheduling, feedback submission and manual status updates.

## API overview

All endpoints except login and reset-password require a Bearer token. List endpoints are paginated with 10 records per page by default.

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/login`, `POST /auth/reset-password`, `POST /auth/logout` |
| Users | `POST/GET /users`, `GET /users/interviewers`, `GET/PUT /users/{id}`, `PATCH /users/{id}/disable` |
| Jobs | `POST/GET /jobs`, `GET/PUT /jobs/{id}` |
| Candidates | `POST/GET /candidates`, `GET/PUT /candidates/{id}`, `POST/GET /candidates/{id}/resume`, `PATCH /candidates/{id}/status`, `GET /candidates/{id}/status-history` |
| Interviews | `POST/GET /interviews`, `GET/PUT /interviews/{id}` |
| Feedback | `POST /feedbacks`, `GET /feedbacks/interview/{id}` |
| Dashboard | `GET /dashboard/hr`, `GET /dashboard/interviewer` |

`GET /users/interviewers` accepts optional `interview_date`, `start_time` and `end_time` query params and then returns only interviewers who are free in that window. Full request/response schemas are in Swagger.

## Validation rules

- **User emails** must be on the `nucleusteq.com` domain and may only contain letters, digits, dot or underscore before the `@`. Same rule for candidate emails.
- **Names** (user and candidate first/last name) may only contain letters and spaces.
- **Passwords** are 6-12 characters, letters/digits/special characters, stored as bcrypt hashes. Plaintext is never stored or returned.
- **Mobile numbers** are exactly 10 digits and unique across candidates. Candidate emails are unique too.
- **Resumes** must be PDFs, checked by extension and `%PDF` magic bytes, minimum 100 bytes, maximum 10 MB, stored in GridFS.
- **Feedback ratings** (technical, communication, problem solving) must each be between 1 and 5.
- **Interview times** are HH:MM (24 hour), end time must be after start time, and the interviewer must actually have the interviewer role and be free in that range.

Validation happens on both sides: pydantic validators return 422 from the API, and the React forms run the same rules client-side for instant feedback.

## Error handling and logging

Every error returns the same JSON shape:

```json
{ "success": false, "message": "Interviewer already has an interview in this time range", "status_code": 409 }
```

Application and error logs go to `logs/app.log` and stdout. Logs contain only the method, path and status code. No request bodies, emails or other personal data are written to logs.

## Configuration

All backend settings live in `backend/.env` (see `.env.example`):

| Variable | Purpose | Default |
|---|---|---|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGO_DB_NAME` | Database name | `interview_portal` |
| `SECRET_KEY` | JWT signing key (change it) | - |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | 30 |
| `LOG_LEVEL` / `LOG_FILE` | Logging | `INFO` / `logs/app.log` |

The app pings MongoDB once at startup and fails fast with a clear log message if the database is unreachable.

## Default credentials

After running the seed script:

| Account | Email | Password |
|---|---|---|
| Admin | `admin@nucleusteq.com` | `admin123` |

Users created by the admin get the default password `admin123` and are forced to set their own on first sign-in.
