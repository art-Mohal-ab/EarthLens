# EarthLens 

An AI-powered platform for environmental awareness and community-driven climate action. EarthLens empowers citizens to report environmental issues, analyze them with AI, and take meaningful action for a healthier planet.

**Aligned with UN SDG 13 (Climate Action)** - EarthLens combines user engagement, environmental education, and technology to drive real-world sustainability awareness.

## 🌐 Live Demo

**Frontend**: [https://earth-lens-9mgz-git-main-art-mohal-abs-projects.vercel.app](https://earth-lens-9mgz-git-main-art-mohal-abs-projects.vercel.app)  
**Backend API**: [https://earthlens-2.onrender.com](https://earthlens-2.onrender.com)

## Features

### Core Functionality
- **Environmental Reporting**: Submit detailed reports with photos, location data, and descriptions
- **AI-Powered Analysis**: Automatic categorization and actionable advice using OpenAI GPT
- **Community Dashboard**: View public reports and track environmental trends
- **User Authentication**: Secure JWT-based authentication system
- **Profile Management**: Personal dashboard for managing your reports and impact

### AI Features
- **Smart Categorization**: Automatically classify environmental issues (pollution, deforestation, water issues, etc.)
- **Personalized Advice**: Get tailored recommendations for addressing specific problems
- **Green Action Generator**: AI-generated sustainable tasks and challenges
- **Confidence Scoring**: Reliability metrics for AI analysis

### Technical Features
- **File Upload**: Support for image attachments with secure cloud storage
- **Location Services**: GPS-based reporting and nearby issue discovery
- **Real-time Updates**: Live dashboard with filtering and pagination
- **Responsive Design**: Mobile-first approach with modern UI/UX

##  Architecture

### Tech Stack

#### Frontend (Client)
- **React 19** - Modern React with hooks and concurrent features
- **Vite** - Fast build tool and development server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **CSS Modules** - Scoped styling
- **Vitest** - Unit testing framework
- **ESLint** - Code linting

#### Backend (Server)
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **JWT** - JSON Web Token authentication
- **OpenAI API** - AI-powered analysis
- **Marshmallow** - Data serialization/validation
- **Flask-CORS** - Cross-origin resource sharing

#### Database
- **SQLite** (development) / **PostgreSQL** (production)
- **Alembic** - Database migration tool

## Project Structure

```
EarthLens/
├── Client/                    # React Frontend
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   ├── styles/          # CSS stylesheets
│   │   └── tests/           # Unit tests
│   ├── package.json
│   └── vite.config.js
├── server/                   # Flask Backend
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Data validation
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utilities
│   │   └── middleware/      # Custom middleware
│   ├── migrations/          # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── run.py              # Application entry point
└── README.md               
```

## Installation & Setup

### Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Git**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EarthLens
   ```

2. **Set up Python environment**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   ```

   Configure the following environment variables:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key
   DATABASE_URL=sqlite:///earthlens.db
   JWT_SECRET_KEY=your-jwt-secret
   ```

5. **Database setup**
   ```bash
   flask db upgrade
   python seed.py  # Optional: seed with sample data
   ```

6. **Run the backend**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to client directory**
   ```bash
   cd ../Client
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment configuration**
   ```bash
   cp .env.example .env  # If needed
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

##  Usage

### For Users
1. **Sign Up/Login**: Create an account or log in
2. **Report Issues**: Use the report form to submit environmental concerns with photos and location
3. **View Dashboard**: Browse community reports and track environmental trends
4. **Get AI Advice**: Receive personalized recommendations for addressing issues
5. **Take Action**: Complete AI-generated green tasks and challenges

### For Developers
- **API Documentation**: Available at `/api/health` endpoint
- **Testing**: Run `npm test` (frontend) and `python -m pytest` (backend)
- **Linting**: Run `npm run lint` (frontend)

##  API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

### Reports
- `GET /api/reports` - Get public reports
- `POST /api/reports` - Create new report
- `GET /api/reports/{id}` - Get specific report
- `PUT /api/reports/{id}` - Update report
- `DELETE /api/reports/{id}` - Delete report

### AI Services
- `POST /api/ai/analyze-report/{id}` - Analyze report with AI
- `GET /api/ai/green-advice` - Get green action advice
- `GET /api/ai/generate-task` - Generate AI-powered task

### Users
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user profile

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React
- Write tests for new features
- Update documentation as needed

## Testing

### Frontend Tests
```bash
cd Client
npm test
npm run test:coverage  # With coverage report
```

### Backend Tests
```bash
cd server
python -m pytest
```

## Deployment

### Backend Deployment
1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server (gunicorn, uwsgi)
3. Configure PostgreSQL database
4. Set up proper environment variables

### Frontend Deployment
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `dist/` folder with any static server
3. Configure API base URL for production

##  Security

- JWT-based authentication with secure secrets
- Input validation using Marshmallow schemas
- CORS configuration for cross-origin requests
- Secure file upload handling
- Environment variable management

##  Acknowledgments

- OpenAI for AI analysis capabilities
- React and Flask communities
- Environmental organizations worldwide
- All contributors and users

##  Support

For support, email support@earthlens.com or join our community forum.

---

##  Acknowledgments

- OpenAI for AI analysis capabilities
- React and Flask communities
- Environmental organizations worldwide
- All contributors and users

##  Support

For support, email support@earthlens.com or join our community forum.

---


