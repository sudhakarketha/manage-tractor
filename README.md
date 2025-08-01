# Tractor Management System

A Flask web application for tractor owners to manage work details such as harvesting, transport, rotor, and plough operations.

## Features

- **Farmer Management**: Add, view, and delete farmers
- **Work Tracking**: Record different types of tractor work (harvesting, transport, rotor, plough, etc.)
- **Dynamic Units**: Different work types use appropriate units (hours, trips, acres)
- **Status Management**: Track work status (Pending, Completed, Paid)
- **Reports**: View statistics and charts
- **Responsive Design**: Modern UI with Bootstrap 5

## Local Development

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd manage-tractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000`

## Deployment on Render

### Step 1: Prepare Your Repository

Make sure your repository contains these files:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration (optional)
- `Procfile` - Process file for Render

### Step 2: Deploy on Render

1. **Sign up/Login to Render**:
   - Go to [render.com](https://render.com)
   - Sign up or login to your account

2. **Create New Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure the Service**:
   - **Name**: `tractor-management` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Choose Free or Paid plan

4. **Environment Variables** (Optional):
   - `SECRET_KEY`: A secure random string for Flask sessions
   - `DATABASE_URL`: Database connection string (Render will provide this)

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Step 3: Database Setup

The application will automatically create the database tables on first run. No additional setup required.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key-here` |
| `DATABASE_URL` | Database connection string | `sqlite:///tractor_management.db` |
| `PORT` | Port number for the application | `5000` |

## File Structure

```
manage-tractor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render configuration
├── Procfile             # Process file for Render
├── init_db.py           # Database initialization script
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── farmers.html
│   ├── add_farmer.html
│   ├── farmer_detail.html
│   ├── works.html
│   ├── add_work.html
│   └── reports.html
└── README.md            # This file
```

## Features in Detail

### Farmer Management
- Add farmers with name, phone, email (optional), and address
- Unique farmer names validation
- View all farmers in a list
- Delete farmers (with confirmation)
- View individual farmer details and work history

### Work Management
- Add work entries with different types (harvesting, transport, rotor, plough, etc.)
- Dynamic units based on work type:
  - Rotor/Harvesting/Seeding/Irrigation: hours
  - Transport: trips
  - Plough: acres
  - Other: units
- Track work status (Pending → Completed → Paid)
- Delete work entries (with confirmation)

### Dashboard
- Overview statistics
- Recent work entries
- Quick access to all features

### Reports
- Total revenue
- Work distribution by type
- Work distribution by status
- Interactive charts using Chart.js

## Validation Features

- **Farmer Name Uniqueness**: Prevents duplicate farmer names
- **No Farmers Check**: Redirects to add farmer page when no farmers exist
- **Email Validation**: Optional email with proper format validation
- **Required Fields**: All essential fields are validated

## Technologies Used

- **Backend**: Flask, SQLAlchemy, WTForms
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js
- **Database**: SQLite (local) / PostgreSQL (production)
- **Deployment**: Render, Gunicorn

## Support

For issues or questions:
1. Check the application logs in Render dashboard
2. Ensure all environment variables are set correctly
3. Verify the database is properly initialized

## License

This project is open source and available under the MIT License.