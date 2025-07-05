# Blog API with Authentication

## Endpoints

| Endpoint                  | Method | Auth Required? | Description                 |
| ------------------------- | ------ | -------------- | --------------------------- |
| `/api/register/`          | POST   | ❌             | Register a new user         |
| `/api/login/`             | POST   | ❌             | Login                       |
| `/api/create-post/`       | POST   | ✅             | Create a blog post          |
| `/api/posts/`             | GET    | ❌             | List all posts              |
| `/api/post/<id>/`         | GET    | ❌             | Get post details + comments |
| `/api/post/<id>/comment/` | POST   | ✅             | Add a comment               |

## Setup

1. Clone the repo
2. Create virtualenv: `python -m venv venv`
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`
