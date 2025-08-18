
# FRC ComponentHub API

FRC ComponentHub API is a secure, modern inventory management system for FIRST Robotics Competition (FRC) teams, built with FastAPI. Manage your team’s inventory, access a public component catalog, and collaborate efficiently with robust authentication and authorization.

---

## Live Demo

- **API:** [frc-components-api.onrender.com](https://frc-components-api.onrender.com)
- **Docs:** [Swagger UI](https://frc-components-api.onrender.com/docs)

---

## Features

- 46+ real FRC parts with pricing, vendor, availability, CAD files, and images
- Team inventory: track quantities, locations, notes, and link to public parts
- JWT authentication and team-based access
- Full CRUD for public/team components; utility endpoints for categories, vendors, etc.

---

## API Examples

**Get All Public Components**

```http
GET /public-components/
```

Response:
```json
[
  {
    "id": "NEO-550",
    "name": "NEO 550 Brushless Motor",
    "vendor": "REV Robotics",
    "category": "Motors",
    "cost": 39.99,
    "availability": "In Stock",
    "description": "Compact brushless motor for FRC robots"
  }
]
```

**Search Components**

```http
GET /public-components/search?category=Motors&max_cost=50
```

Query: `q`, `category`, `vendor`, `min_cost`, `max_cost`

**Add Team Component**

```http
POST /team-components/
```
```json
{
  "team_id": "1234",
  "public_component_id": "NEO-550",
  "name": "NEO 550 Motor",
  "vendor": "REV Robotics",
  "quantity": 4,
  "location": "Drivetrain Box",
  "notes": "For swerve modules"
}
```

---

## API Reference

**Public Components**
- `GET /public-components/` — List all
- `POST /public-components/` — Create
- `GET /public-components/search` — Search/filter
- `GET /public-components/{id}` — Get by ID
- `PUT /public-components/{id}` — Update
- `DELETE /public-components/{id}` — Delete

**Team Components**
- `POST /team-components/` — Add to team inventory
- `GET /teams/{id}/components` — Team inventory
- `GET /team-components/{id}` — Get by ID
- `PUT /team-components/{id}` — Update
- `DELETE /team-components/{id}` — Delete
- `GET /teams/{id}/inventory/summary` — Team stats

**Utility**
- `/categories`, `/vendors`, `/availability-statuses`, `/components/with-cad-files`, `/components/with-images`, `/teams/{id}/add-image`

---

## Getting Started

**Use Live API:** [Interactive Docs](https://frc-components-api.onrender.com/docs)

**Run Locally:**

```sh
git clone https://github.com/MNTadros/FRC_API
pip install -r requirements.txt
python run_server.py
```

Create a `.env` file:

```
SECRET_KEY=your-very-secret-key
DATABASE_URL=sqlite:///./frc_components.db
```

**Integrate:** Use with Python, JavaScript, cURL, or any HTTP client.

---

## Authentication Flow

1. Register via `/register`
2. Log in via `/token` to get a JWT
3. Use the "Authorize" button in docs or send `Authorization: Bearer <token>`
4. Use `/users/me` to check your account and team

---