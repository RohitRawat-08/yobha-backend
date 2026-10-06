# YOBHA Django Backend

This directory contains the Django REST Framework backend for the Youth of Bharat Foundation website.

## Local Setup

1. Copy `.env.example` to `.env` and add a unique `SECRET_KEY` plus MySQL connection values.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create the MySQL database named by `DATABASE_NAME`.
4. Apply schema changes with `python manage.py migrate`.
5. Export the current React content from the repository root with `node scripts/export-react-content.mjs`.
6. Import it with `python manage.py import_react_content`.
7. Create an admin user with `python manage.py createsuperuser`.
8. Start Django with `python manage.py runserver`.

For a local smoke test only, set `DATABASE_ENGINE=django.db.backends.sqlite3` and `DATABASE_NAME=backend/db.sqlite3`. Production must use MySQL.

## Main Endpoints

- `/api/v1/publications/`
- `/api/v1/issue-briefs/`
- `/api/v1/bill-briefs/`
- `/api/v1/books/`
- `/api/v1/reports/`
- `/api/v1/initiative-groups/<slug>/`
- `/api/v1/initiatives/<slug>/`
- `/api/v1/events/?timing=upcoming`
- `/api/v1/podcast/`
- `/api/v1/people-categories/<slug>/`
- `/api/v1/testimonials/`
- `/api/v1/partners/`
- `/api/v1/site-settings/`

Public `GET` requests only return published content. Django Admin at `/admin/` is the supported first-version CMS for content creation, editing, uploads, publishing, and unpublishing.

## Content Import

The importer is repeatable. It updates records by slug, refreshes ordered site content, and copies referenced React assets into `backend/media/imported/`. It does not delete the original React data files; remove only verified duplicate content after every relevant page has moved to the API.
