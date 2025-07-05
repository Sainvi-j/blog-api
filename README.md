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

## Setup
1. Clone the repo:
   ```bash
   git clone https:/Sainvi-j/github.com//blog-api.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python manage.py runserver
   ```
