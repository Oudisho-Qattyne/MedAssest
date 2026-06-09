# MedAssest API Documentation

**Base URL:** `http://localhost:8000/api/`  
**Auth:** `Authorization: Bearer <access_token>`  
**Pagination:** `?page=1` (20 items/page, response wrapped in `{count, next, previous, results: [...]}`)  
**Filter params:** `?search=term` (text search), `?ordering=field` (prefix `-` for desc), `?field=value` (exact match)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Patients](#patients)
4. [Family Members](#family-members)
5. [Aid Provider Categories](#aid-provider-categories)
6. [Aid Providers](#aid-providers)
7. [Aid Request Types](#aid-request-types)
8. [Aid Requests](#aid-requests)
9. [Aid Request Providers](#aid-request-providers)
10. [Role Matrix](#role-based-access-matrix)
11. [Quick Reference](#query-parameter-quick-reference)

---

## Authentication

### `POST /api/token/`

Obtain JWT access + refresh tokens. Returns `role` for frontend routing.

```
Request:
{
  "email": "doctor@example.com",
  "password": "string"
}

Response 200:
{
  "access": "eyJhbGciOi...",
  "refresh": "eyJhbGciOi...",
  "role": "doctor"
}
```

### `POST /api/token/refresh/`

```
Request:
{
  "refresh": "eyJhbGciOi..."
}

Response 200:
{
  "access": "eyJhbGciOi..."
}
```

---

## Users

All user endpoints require `admin` role.

### `GET /api/users/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `full_name`, `email` |
| `ordering` | field | `full_name`, `email`, `created_at` |
| `role` | exact | `admin`, `doctor`, `requests_processor` |

```json
[
  {
    "id": 1,
    "email": "doctor@example.com",
    "full_name": "Dr. Smith",
    "role": "doctor",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

### `POST /api/users/`

```json
{
  "email": "newuser@example.com",
  "full_name": "New User",
  "password": "securepass123",
  "role": "doctor"
}
```

### `GET /api/users/{id}/` · `PUT /api/users/{id}/` · `PATCH /api/users/{id}/` · `DELETE /api/users/{id}/`

---

## Patients

### `GET /api/patients/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `first_name`, `middle_name`, `last_name`, `national_number`, `phone_number`, `current_residence` |
| `ordering` | field | `first_name`, `last_name`, `birth_date`, `created_at` |
| `gender` | exact | `male`, `female` |
| `marital_status` | exact | `single`, `married`, `divorced`, `widowed` |
| `home_status` | exact | `owned`, `rented`, `family_owned` |

```json
[
  {
    "id": 1,
    "first_name": "John",
    "middle_name": "",
    "last_name": "Doe",
    "mother_full_name": "",
    "birth_date": "1990-05-15",
    "gender": "male",
    "national_number": "123456789",
    "family_booklet_no": "",
    "current_residence": "City Name",
    "phone_number": "0912345678",
    "telephone_number": "",
    "marital_status": "married",
    "home_status": "owned",
    "job_type": "Engineer",
    "job_title": "",
    "monthly_salary": "1500.00",
    "special_needs": "",
    "note": "",
    "created_by_user": 1,
    "created_by_user_email": "doctor@example.com",
    "created_at": "2025-01-01T00:00:00Z",
    "family_members": [
      {
        "id": 1,
        "patient": 1,
        "full_name": "Jane Doe",
        "relation": "spouse",
        "gender": "female",
        "birth_date": "1992-08-20",
        "note": ""
      }
    ]
  }
]
```

### `POST /api/patients/`

`created_by_user` auto-set to authenticated user. Roles: `admin`, `doctor`

```json
{
  "first_name": "John",
  "middle_name": "",
  "last_name": "Doe",
  "mother_full_name": "",
  "birth_date": "1990-05-15",
  "gender": "male",
  "national_number": "123456789",
  "family_booklet_no": "",
  "current_residence": "City Name",
  "phone_number": "0912345678",
  "telephone_number": "",
  "marital_status": "married",
  "home_status": "owned",
  "job_type": "Engineer",
  "job_title": "",
  "monthly_salary": 1500.00,
  "special_needs": "",
  "note": ""
}
```

**Enum values:**
- `gender`: `male`, `female`
- `marital_status`: `single`, `married`, `divorced`, `widowed`
- `home_status`: `owned`, `rented`, `family_owned`

### `GET /api/patients/{id}/`

### `PUT /api/patients/{id}/` · `PATCH /api/patients/{id}/` · `DELETE /api/patients/{id}/`
**Roles:** `admin` only for write/delete

---

## Family Members

Nested under patients. Write requires `admin` or `doctor`, edit/delete `admin` only.

### `GET /api/patients/{patient_pk}/family/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `full_name` |
| `ordering` | field | `full_name` |
| `relation` | exact | e.g. `spouse`, `child`, `parent` |
| `gender` | exact | `male`, `female` |

```json
[
  {
    "id": 1,
    "patient": 1,
    "full_name": "Jane Doe",
    "relation": "spouse",
    "gender": "female",
    "birth_date": "1992-08-20",
    "note": ""
  }
]
```

### `POST /api/patients/{patient_pk}/family/`

```json
{
  "full_name": "Jane Doe",
  "relation": "spouse",
  "gender": "female",
  "birth_date": "1992-08-20",
  "note": ""
}
```

### `GET /api/patients/family/{id}/`

### `PUT /api/patients/family/{id}/` · `PATCH /api/patients/family/{id}/` · `DELETE /api/patients/family/{id}/`
**Roles:** `admin` only for write/delete

---

## Aid Provider Categories

### `GET /api/aid-providers/categories/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `category_name` |
| `ordering` | field | `category_name` |

```json
[
  {
    "id": 1,
    "category_name": "Hospital"
  }
]
```

### `POST /api/aid-providers/categories/`
**Roles:** `admin` only
```json
{ "category_name": "Pharmacy" }
```

### `GET /api/aid-providers/categories/{id}/`

### `PUT /api/aid-providers/categories/{id}/` · `PATCH /api/aid-providers/categories/{id}/` · `DELETE /api/aid-providers/categories/{id}/`
**Roles:** `admin` only for write/delete

---

## Aid Providers

### `GET /api/aid-providers/providers/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `name`, `specialization`, `phone_number`, `email` |
| `ordering` | field | `name`, `created_at` |
| `category` | exact | Category ID (int) |

```json
[
  {
    "id": 1,
    "name": "City Hospital",
    "specialization": "Cardiology",
    "phone_number": "011234567",
    "email": "info@cityhospital.com",
    "category": {
      "id": 1,
      "name": "Hospital"
    },
    "logo_url": "https://example.com/logo.png",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

> **Note:** `category` on read returns `{id, name}`. On write, send `category: 1` (integer FK).

### `POST /api/aid-providers/providers/`
**Roles:** `admin` only
```json
{
  "name": "City Hospital",
  "specialization": "Cardiology",
  "phone_number": "011234567",
  "email": "info@cityhospital.com",
  "category": 1,
  "logo_url": ""
}
```

### `GET /api/aid-providers/providers/{id}/`

### `PUT /api/aid-providers/providers/{id}/` · `PATCH /api/aid-providers/providers/{id}/` · `DELETE /api/aid-providers/providers/{id}/`
**Roles:** `admin` only for write/delete

---

## Aid Request Types

### `GET /api/aid-requests/types/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `type_name`, `description` |
| `ordering` | field | `type_name` |

```json
[
  {
    "id": 1,
    "type_name": "Medical Treatment",
    "description": "Financial aid for medical procedures"
  }
]
```

### `POST /api/aid-requests/types/`
**Roles:** `admin`, `doctor`
```json
{
  "type_name": "Surgery",
  "description": "Surgical procedure assistance"
}
```

### `GET /api/aid-requests/types/{id}/`

### `PUT /api/aid-requests/types/{id}/` · `PATCH /api/aid-requests/types/{id}/` · `DELETE /api/aid-requests/types/{id}/`

---

## Aid Requests

### `GET /api/aid-requests/requests/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `description`, `place_of_aid` |
| `ordering` | field | `date_of_aid`, `estimated_cost`, `id` |
| `request_status` | exact | `pending`, `processing`, `rejected`, `completed` |
| `patient` | exact | Patient ID (int) |
| `aid_request_type` | exact | Request Type ID (int) |
| `date_of_aid` | exact | Date `YYYY-MM-DD` |

```json
[
  {
    "id": 1,
    "patient": 1,
    "patient_full_name": "John Doe",
    "request_status": "pending",
    "description": "Needs surgery assistance",
    "aid_request_type": {
      "id": 1,
      "type_name": "Medical Treatment"
    },
    "estimated_cost": "5000.00",
    "place_of_aid": "City Hospital",
    "date_of_aid": "2025-06-01",
    "total_provided_amount": 3500.00,
    "providers": [
      {
        "id": 1,
        "aid_request": 1,
        "aid_provider": 2,
        "provider_name": "Charity Fund",
        "aid_type": "financial",
        "aid_amount": "2500.00",
        "type_of_aid_amount": "fixed",
        "notes": "Full coverage approved"
      }
    ]
  }
]
```

> **Note:** `aid_request_type` on read returns `{id, type_name}`. On write, send `aid_request_type: 1` (integer FK).  
> `total_provided_amount` is computed: fixed amounts sum directly, percentage amounts apply against `estimated_cost`.

### `POST /api/aid-requests/requests/`

`request_status` defaults to `pending`. Roles: `admin`, `doctor`

```json
{
  "patient": 1,
  "description": "Needs surgery assistance",
  "aid_request_type": 1,
  "estimated_cost": 5000.00,
  "place_of_aid": "City Hospital",
  "date_of_aid": "2025-06-01"
}
```

### `GET /api/aid-requests/requests/{id}/`

### `PUT /api/aid-requests/requests/{id}/` · `PATCH /api/aid-requests/requests/{id}/`

**Status update** — changing `request_status` restricted to `admin` or `requests_processor`:
```json
{ "request_status": "processing" }
```
Status values: `pending`, `processing`, `rejected`, `completed`

### `DELETE /api/aid-requests/requests/{id}/`
**Roles:** `admin`, `doctor`

---

## Aid Request Providers

Links a provider to an aid request with amount details.

### `GET /api/aid-requests/requests/{request_pk}/providers/`

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number |
| `search` | string | `notes` |
| `ordering` | field | `aid_amount` |
| `aid_type` | exact | `medical`, `financial` |
| `type_of_aid_amount` | exact | `percentage`, `fixed` |
| `aid_provider` | exact | Provider ID (int) |

```json
[
  {
    "id": 1,
    "aid_request": 1,
    "aid_provider": 2,
    "provider_name": "Charity Fund",
    "aid_type": "financial",
    "aid_amount": "2500.00",
    "type_of_aid_amount": "fixed",
    "notes": "Approved partial coverage"
  }
]
```

### `POST /api/aid-requests/requests/{request_pk}/providers/`
**Roles:** `admin`, `doctor`
```json
{
  "aid_provider": 2,
  "aid_type": "financial",
  "aid_amount": 2500.00,
  "type_of_aid_amount": "fixed",
  "notes": "Approved partial coverage"
}
```

**Enum values:**
- `aid_type`: `medical`, `financial`
- `type_of_aid_amount`: `percentage`, `fixed`

### `GET /api/aid-requests/providers/{id}/`

### `PUT /api/aid-requests/providers/{id}/` · `PATCH /api/aid-requests/providers/{id}/` · `DELETE /api/aid-requests/providers/{id}/`
**Roles:** `admin`, `doctor`

---

## Role-Based Access Matrix

| Resource | Action | Admin | Doctor | Requests Processor |
|----------|--------|-------|--------|--------------------|
| Users | All | ✅ | ❌ | ❌ |
| Patients | List, Create | ✅ | ✅ | ❌ |
| Patients | Edit, Delete | ✅ | ❌ | ❌ |
| Family Members | List, Create | ✅ | ✅ | ❌ |
| Family Members | Edit, Delete | ✅ | ❌ | ❌ |
| Provider Categories | Read | ✅ | ✅ | ✅ |
| Provider Categories | Write | ✅ | ❌ | ❌ |
| Aid Providers | Read | ✅ | ✅ | ✅ |
| Aid Providers | Write | ✅ | ❌ | ❌ |
| Request Types | All | ✅ | ✅ | ❌ |
| Aid Requests | List, Create, Edit (non-status), Delete | ✅ | ✅ | ❌ |
| Aid Requests | Change Status | ✅ | ❌ | ✅ |
| Aid Requests | Read-only | ✅ | ✅ | ✅ |
| Request Providers | All | ✅ | ✅ | ❌ |

---

## Query Parameter Quick Reference

| Endpoint | `search` | `ordering` | `filterset_fields` |
|----------|----------|------------|-------------------|
| `GET /users/` | `full_name`, `email` | `full_name`, `email`, `created_at` | `role` |
| `GET /patients/` | `first_name`, `middle_name`, `last_name`, `national_number`, `phone_number`, `current_residence` | `first_name`, `last_name`, `birth_date`, `created_at` | `gender`, `marital_status`, `home_status` |
| `GET /patients/{id}/family/` | `full_name` | `full_name` | `relation`, `gender` |
| `GET /aid-providers/categories/` | `category_name` | `category_name` | — |
| `GET /aid-providers/providers/` | `name`, `specialization`, `phone_number`, `email` | `name`, `created_at` | `category` |
| `GET /aid-requests/types/` | `type_name`, `description` | `type_name` | — |
| `GET /aid-requests/requests/` | `description`, `place_of_aid` | `date_of_aid`, `estimated_cost`, `id` | `request_status`, `patient`, `aid_request_type`, `date_of_aid` |
| `GET /aid-requests/requests/{id}/providers/` | `notes` | `aid_amount` | `aid_type`, `type_of_aid_amount`, `aid_provider` |
