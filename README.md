# Tractor Management System

A comprehensive web application for tractor owners to manage their work details, farmer information, and track revenue from various agricultural operations.

## Features

### 🚜 Core Functionality
- **Farmer Management**: Add and manage farmer details with contact information
- **Work Tracking**: Record different types of tractor work (harvesting, transport, rotor, plough, etc.)
- **Status Management**: Track work status (Pending, Completed, Paid)
- **Revenue Tracking**: Automatic calculation of work costs and total revenue
- **Reports & Analytics**: Visual charts and statistics for business insights

### 📊 Work Types Supported
- **Harvesting**: Crop harvesting operations
- **Transport**: Transportation of goods/materials
- **Rotor**: Rotor tiller operations
- **Plough**: Ploughing operations
- **Seeding**: Seeding operations
- **Irrigation**: Irrigation operations
- **Other**: Custom work types

### 🎨 Modern UI Features
- Responsive design that works on desktop and mobile
- Beautiful gradient sidebar navigation
- Interactive charts and statistics
- Clean, modern Bootstrap 5 interface
- Font Awesome icons for better UX

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd manage-tractor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will automatically create the database on first run

## Usage Guide

### Getting Started
1. **Add Farmers**: Start by adding farmer details through the "Farmers" section
2. **Record Works**: Add tractor work details for each farmer
3. **Track Status**: Update work status as jobs progress
4. **View Reports**: Monitor your business performance through the reports section

### Adding a Farmer
1. Click "Add New Farmer" from the Farmers page
2. Fill in the required information:
   - Name
   - Phone number
   - Email address
   - Complete address
3. Click "Add Farmer" to save

### Recording Tractor Work
1. Click "Add New Work" from the Works page
2. Select the farmer from the dropdown
3. Choose the work type (harvesting, transport, etc.)
4. Enter work details:
   - Description of the work
   - Date of work
   - Hours worked
   - Rate per hour
5. The total amount will be calculated automatically
6. Click "Add Work" to save

### Managing Work Status
- **Pending**: Work is scheduled but not started
- **Completed**: Work has been finished
- **Paid**: Payment has been received

## Database Schema

### Farmers Table
- `id`: Primary key
- `name`: Farmer's full name
- `phone`: Contact phone number
- `email`: Email address (unique)
- `address`: Complete address
- `created_at`: Registration timestamp

### TractorWork Table
- `id`: Primary key
- `work_type`: Type of work performed
- `description`: Detailed work description
- `date`: Date of work
- `hours_worked`: Number of hours
- `rate_per_hour`: Hourly rate
- `total_amount`: Calculated total cost
- `status`: Work status (Pending/Completed/Paid)
- `farmer_id`: Foreign key to Farmers table
- `created_at`: Record creation timestamp

## API Endpoints

### REST API
- `GET /api/works`: Get all works in JSON format
- `GET /`: Dashboard with statistics
- `GET /farmers`: List all farmers
- `GET /works`: List all works
- `GET /reports`: Analytics and reports

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Forms**: WTForms with validation

## File Structure

```
manage-tractor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Dashboard
│   ├── farmers.html      # Farmers list
│   ├── add_farmer.html   # Add farmer form
│   ├── farmer_detail.html # Farmer details and work history
│   ├── works.html        # Works list
│   ├── add_work.html     # Add work form
│   └── reports.html      # Analytics and reports
└── tractor_management.db # SQLite database (created automatically)
```

## Customization

### Adding New Work Types
To add new work types, modify the `TractorWorkForm` in `app.py`:

```python
work_type = SelectField('Work Type', choices=[
    ('harvesting', 'Harvesting'),
    ('transport', 'Transport'),
    ('rotor', 'Rotor'),
    ('plough', 'Plough'),
    ('seeding', 'Seeding'),
    ('irrigation', 'Irrigation'),
    ('your_new_type', 'Your New Type'),  # Add here
    ('other', 'Other')
], validators=[DataRequired()])
```

### Changing Currency
To change the currency symbol, update the templates where ₹ appears:

```html
<!-- Replace ₹ with your currency symbol -->
₹{{ "%.2f"|format(work.total_amount) }}
```

## Troubleshooting

### Common Issues

1. **Database not created**: The database is created automatically on first run. If issues occur, delete `tractor_management.db` and restart the application.

2. **Port already in use**: Change the port in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```

3. **Dependencies not found**: Ensure you're using the correct Python environment and have installed all requirements.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please create an issue in the repository or contact the development team.

---

**Happy Tractor Management! 🚜**