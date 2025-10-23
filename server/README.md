# EarthLens Backend

A Flask-based backend for environmental reporting with AI analysis.

## Quick Setup

1. **Install and Setup**:
   ```bash
   python setup.py
   ```

2. **Start the Server**:
   ```bash
   python run.py
   ```

## Manual Setup (Alternative)

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**:
   ```bash
   python -c "from main import create_app; from database import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created')"
   ```

3. **Run Server**:
   ```bash
   python main.py
   ```

## Migration Commands

If you want to use Flask-Migrate:

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
FLASK_ENV=development
DATABASE_URI=sqlite:///dev.db
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `POST /api/reports` - Create report
- `GET /api/reports` - List reports
- `POST /api/ai/analyze` - AI analysis
- `GET /api/ai/categories` - Environmental categories

## Project Structure

```
server/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── schemas/         # Marshmallow schemas
│   ├── services/        # Business logic
│   └── middleware/      # Auth middleware
├── config.py           # Configuration
├── database.py         # Database setup
├── main.py            # Flask app factory
├── run.py             # Startup script
└── setup.py           # Setup script
```