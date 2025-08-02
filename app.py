from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Ensure the instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

# Database configuration - Support SQLite (local) and MySQL (Clever Cloud deployment)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('mysql://'):
    # Convert mysql:// to mysql+pymysql:// for Clever Cloud
    database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///tractor_management.db'
if database_url:
    print(f"🌐 Using MySQL database: {database_url}")
else:
    print(f"💻 Using SQLite database: sqlite:///tractor_management.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ensure database is initialized
def ensure_database():
    """Ensure database tables exist"""
    with app.app_context():
        try:
            db.create_all()
            print(f"✅ Database ready at: {app.config['SQLALCHEMY_DATABASE_URI']}")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")

# Initialize database on import
ensure_database()

# Database Models
class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    works = db.relationship('TractorWork', backref='farmer', lazy=True)

class TractorWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    rate_per_unit = db.Column(db.Float, nullable=False)
    unit_type = db.Column(db.String(20), nullable=False)  # hours, trips, acres, etc.
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Completed, Paid
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Custom validator for unique farmer names
def validate_unique_farmer_name(form, field):
    # Check if a farmer with this name already exists
    existing_farmer = Farmer.query.filter_by(name=field.data.strip()).first()
    if existing_farmer:
        raise ValidationError('A farmer with this name already exists. Please choose a different name.')

# Forms
class FarmerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), validate_unique_farmer_name])
    phone = StringField('Phone', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address', validators=[Optional()])
    submit = SubmitField('Add Farmer')

class TractorWorkForm(FlaskForm):
    work_type = SelectField('Work Type', choices=[
        ('harvesting', 'Harvesting'),
        ('transport', 'Transport'),
        ('rotor', 'Rotor'),
        ('plough', 'Plough'),
        ('seeding', 'Seeding'),
        ('irrigation', 'Irrigation'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    rate_per_unit = DecimalField('Rate per Unit', validators=[DataRequired()])
    farmer_id = SelectField('Farmer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Work')

# Routes
@app.route('/')
def index():
    total_farmers = Farmer.query.count()
    total_works = TractorWork.query.count()
    pending_works = TractorWork.query.filter_by(status='Pending').count()
    completed_works = TractorWork.query.filter_by(status='Completed').count()
    
    # Count farmers who have at least one paid work
    paid_farmers = db.session.query(Farmer).join(TractorWork).filter(TractorWork.status == 'Paid').distinct().count()
    
    recent_works = TractorWork.query.order_by(TractorWork.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_farmers=total_farmers,
                         total_works=total_works,
                         pending_works=pending_works,
                         completed_works=completed_works,
                         paid_farmers=paid_farmers,
                         recent_works=recent_works)

@app.route('/farmers')
def farmers():
    farmers_list = Farmer.query.order_by(Farmer.name).all()
    return render_template('farmers.html', farmers=farmers_list)

@app.route('/farmers/add', methods=['GET', 'POST'])
def add_farmer():
    form = FarmerForm()
    if form.validate_on_submit():
        try:
            # Convert empty fields to None to avoid constraint issues
            email = form.email.data.strip() if form.email.data else None
            phone = form.phone.data.strip() if form.phone.data else None
            address = form.address.data.strip() if form.address.data else None
            
            farmer = Farmer(
                name=form.name.data,
                phone=phone,
                email=email,
                address=address
            )
            db.session.add(farmer)
            db.session.commit()
            flash('Farmer added successfully!', 'success')
            return redirect(url_for('farmers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding farmer: {str(e)}', 'error')
            print(f"Error adding farmer: {e}")
    else:
        # Show form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    return render_template('add_farmer.html', form=form)

@app.route('/farmers/<int:farmer_id>')
def farmer_detail(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    works = TractorWork.query.filter_by(farmer_id=farmer_id).order_by(TractorWork.date.desc()).all()
    return render_template('farmer_detail.html', farmer=farmer, works=works)

@app.route('/farmers/<int:farmer_id>/delete', methods=['POST'])
def delete_farmer(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    
    # Delete all works associated with this farmer first
    TractorWork.query.filter_by(farmer_id=farmer_id).delete()
    
    # Delete the farmer
    db.session.delete(farmer)
    db.session.commit()
    
    flash(f'Farmer "{farmer.name}" and all associated works have been deleted successfully!', 'success')
    return redirect(url_for('farmers'))

@app.route('/works')
def works():
    # Check if there are any farmers in the database
    farmers_count = Farmer.query.count()
    if farmers_count == 0:
        flash('No farmers found! Please add at least one farmer before viewing work entries.', 'warning')
        return redirect(url_for('add_farmer'))
    
    works_list = TractorWork.query.order_by(TractorWork.date.desc()).all()
    return render_template('works.html', works=works_list)

@app.route('/works/add', methods=['GET', 'POST'])
def add_work():
    # Check if there are any farmers in the database
    farmers_count = Farmer.query.count()
    if farmers_count == 0:
        flash('No farmers found! Please add at least one farmer before creating work entries.', 'warning')
        return redirect(url_for('add_farmer'))
    
    form = TractorWorkForm()
    form.farmer_id.choices = [(f.id, f.name) for f in Farmer.query.order_by(Farmer.name).all()]
    
    if form.validate_on_submit():
        # Determine unit type based on work type
        unit_type_map = {
            'rotor': 'hours',
            'harvesting': 'hours',
            'seeding': 'hours',
            'irrigation': 'hours',
            'transport': 'trips',
            'plough': 'acres',
            'other': 'units'
        }
        unit_type = unit_type_map.get(form.work_type.data, 'units')
        
        total_amount = float(form.quantity.data) * float(form.rate_per_unit.data)
        work = TractorWork(
            work_type=form.work_type.data,
            description=form.description.data,
            date=form.date.data,
            quantity=float(form.quantity.data),
            rate_per_unit=float(form.rate_per_unit.data),
            unit_type=unit_type,
            total_amount=total_amount,
            farmer_id=form.farmer_id.data
        )
        db.session.add(work)
        db.session.commit()
        flash('Work added successfully!', 'success')
        return redirect(url_for('works'))
    return render_template('add_work.html', form=form)

@app.route('/works/<int:work_id>/update_status', methods=['POST'])
def update_work_status(work_id):
    work = TractorWork.query.get_or_404(work_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Completed', 'Paid']:
        work.status = new_status
        db.session.commit()
        flash('Work status updated successfully!', 'success')
    return redirect(url_for('works'))

@app.route('/works/<int:work_id>/delete', methods=['POST'])
def delete_work(work_id):
    work = TractorWork.query.get_or_404(work_id)
    work_description = work.description[:30] + "..." if len(work.description) > 30 else work.description
    
    db.session.delete(work)
    db.session.commit()
    
    flash(f'Work "{work_description}" has been deleted successfully!', 'success')
    return redirect(url_for('works'))

@app.route('/reports')
def reports():
    # Check if there are any farmers in the database
    farmers_count = Farmer.query.count()
    if farmers_count == 0:
        flash('No farmers found! Please add at least one farmer before viewing reports.', 'warning')
        return redirect(url_for('add_farmer'))
    
    # Get statistics for reports
    total_revenue = db.session.query(db.func.sum(TractorWork.total_amount)).scalar() or 0
    works_by_type = db.session.query(
        TractorWork.work_type, 
        db.func.count(TractorWork.id)
    ).group_by(TractorWork.work_type).all()
    
    works_by_status = db.session.query(
        TractorWork.status, 
        db.func.count(TractorWork.id)
    ).group_by(TractorWork.status).all()
    
    return render_template('reports.html', 
                         total_revenue=total_revenue,
                         works_by_type=works_by_type,
                         works_by_status=works_by_status)

@app.route('/api/works')
def api_works():
    # Check if there are any farmers in the database
    farmers_count = Farmer.query.count()
    if farmers_count == 0:
        return jsonify({'error': 'No farmers found! Please add at least one farmer first.'}), 400
    
    works = TractorWork.query.all()
    return jsonify([{
        'id': work.id,
        'work_type': work.work_type,
        'description': work.description,
        'date': work.date.strftime('%Y-%m-%d'),
        'quantity': work.quantity,
        'rate_per_unit': work.rate_per_unit,
        'unit_type': work.unit_type,
        'total_amount': work.total_amount,
        'status': work.status,
        'farmer_name': work.farmer.name
    } for work in works])

@app.route('/api/farmers')
def api_farmers():
    """Get all farmers"""
    farmers = Farmer.query.all()
    return jsonify([{
        'id': farmer.id,
        'name': farmer.name,
        'phone': farmer.phone,
        'email': farmer.email,
        'address': farmer.address,
        'created_at': farmer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'total_works': len(farmer.works)
    } for farmer in farmers])

@app.route('/api/farmers', methods=['POST'])
def api_add_farmer():
    """Add a new farmer via API"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if farmer with same name exists
        existing_farmer = Farmer.query.filter_by(name=data['name'].strip()).first()
        if existing_farmer:
            return jsonify({'error': 'A farmer with this name already exists'}), 400
        
        # Create new farmer
        farmer = Farmer(
            name=data['name'].strip(),
            phone=data.get('phone', '').strip() or None,
            email=data.get('email', '').strip() or None,
            address=data.get('address', '').strip() or None
        )
        
        db.session.add(farmer)
        db.session.commit()
        
        return jsonify({
            'message': 'Farmer added successfully',
            'farmer': {
                'id': farmer.id,
                'name': farmer.name,
                'phone': farmer.phone,
                'email': farmer.email,
                'address': farmer.address
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding farmer: {str(e)}'}), 500

@app.route('/api/works', methods=['POST'])
def api_add_work():
    """Add a new work via API"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['work_type', 'description', 'date', 'quantity', 'rate_per_unit', 'farmer_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if farmer exists
        farmer = Farmer.query.get(data['farmer_id'])
        if not farmer:
            return jsonify({'error': 'Farmer not found'}), 404
        
        # Determine unit type based on work type
        unit_type_map = {
            'rotor': 'hours',
            'harvesting': 'hours',
            'seeding': 'hours',
            'irrigation': 'hours',
            'transport': 'trips',
            'plough': 'acres',
            'other': 'units'
        }
        unit_type = unit_type_map.get(data['work_type'], 'units')
        
        # Calculate total amount
        total_amount = float(data['quantity']) * float(data['rate_per_unit'])
        
        # Create new work
        work = TractorWork(
            work_type=data['work_type'],
            description=data['description'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            quantity=float(data['quantity']),
            rate_per_unit=float(data['rate_per_unit']),
            unit_type=unit_type,
            total_amount=total_amount,
            farmer_id=data['farmer_id']
        )
        
        db.session.add(work)
        db.session.commit()
        
        return jsonify({
            'message': 'Work added successfully',
            'work': {
                'id': work.id,
                'work_type': work.work_type,
                'description': work.description,
                'date': work.date.strftime('%Y-%m-%d'),
                'quantity': work.quantity,
                'rate_per_unit': work.rate_per_unit,
                'unit_type': work.unit_type,
                'total_amount': work.total_amount,
                'status': work.status,
                'farmer_name': work.farmer.name
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding work: {str(e)}'}), 500

@app.route('/api/farmers/<int:farmer_id>', methods=['PUT'])
def api_update_farmer(farmer_id):
    """Update a farmer via API"""
    try:
        farmer = Farmer.query.get_or_404(farmer_id)
        data = request.get_json()
        
        if 'name' in data:
            # Check if new name conflicts with existing farmer
            existing = Farmer.query.filter_by(name=data['name'].strip()).first()
            if existing and existing.id != farmer_id:
                return jsonify({'error': 'A farmer with this name already exists'}), 400
            farmer.name = data['name'].strip()
        
        if 'phone' in data:
            farmer.phone = data['phone'].strip() or None
        if 'email' in data:
            farmer.email = data['email'].strip() or None
        if 'address' in data:
            farmer.address = data['address'].strip() or None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Farmer updated successfully',
            'farmer': {
                'id': farmer.id,
                'name': farmer.name,
                'phone': farmer.phone,
                'email': farmer.email,
                'address': farmer.address
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating farmer: {str(e)}'}), 500

@app.route('/api/farmers/<int:farmer_id>', methods=['DELETE'])
def api_delete_farmer(farmer_id):
    """Delete a farmer via API"""
    try:
        farmer = Farmer.query.get_or_404(farmer_id)
        
        # Delete all works associated with this farmer first
        TractorWork.query.filter_by(farmer_id=farmer_id).delete()
        
        # Delete the farmer
        db.session.delete(farmer)
        db.session.commit()
        
        return jsonify({'message': f'Farmer "{farmer.name}" and all associated works deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting farmer: {str(e)}'}), 500

@app.route('/api/works/<int:work_id>', methods=['PUT'])
def api_update_work(work_id):
    """Update work status via API"""
    try:
        work = TractorWork.query.get_or_404(work_id)
        data = request.get_json()
        
        if 'status' in data and data['status'] in ['Pending', 'Completed', 'Paid']:
            work.status = data['status']
            db.session.commit()
            
            return jsonify({
                'message': 'Work status updated successfully',
                'work': {
                    'id': work.id,
                    'status': work.status
                }
            })
        else:
            return jsonify({'error': 'Invalid status. Must be Pending, Completed, or Paid'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating work: {str(e)}'}), 500

@app.route('/api/works/<int:work_id>', methods=['DELETE'])
def api_delete_work(work_id):
    """Delete a work via API"""
    try:
        work = TractorWork.query.get_or_404(work_id)
        work_description = work.description[:30] + "..." if len(work.description) > 30 else work.description
        
        db.session.delete(work)
        db.session.commit()
        
        return jsonify({'message': f'Work "{work_description}" deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting work: {str(e)}'}), 500

@app.route('/test-db')
def test_db():
    """Test database connection and functionality"""
    try:
        farmer_count = Farmer.query.count()
        work_count = TractorWork.query.count()
        
        # Determine database type
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'mysql' in db_url.lower():
            database_type = 'MySQL'
            database_info = {
                'type': 'MySQL',
                'url': db_url,
                'host': os.environ.get('DATABASE_HOST', 'Unknown'),
                'database': os.environ.get('DATABASE_NAME', 'Unknown')
            }
        else:
            database_type = 'SQLite'
            db_path = 'tractor_management.db'
            db_exists = os.path.exists(db_path)
            db_size = os.path.getsize(db_path) if db_exists else 0
            database_info = {
                'type': 'SQLite',
                'url': db_url,
                'file': db_path,
                'exists': db_exists,
                'size_bytes': db_size
            }
        
        return jsonify({
            'status': 'success',
            'database_type': database_type,
            'database_info': database_info,
            'farmer_count': farmer_count,
            'work_count': work_count,
            'message': f'{database_type} database connection working',
            'environment': os.environ.get('FLASK_ENV', 'development')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database_type': 'Unknown',
            'database_url': app.config['SQLALCHEMY_DATABASE_URI'],
            'error': str(e),
            'environment': os.environ.get('FLASK_ENV', 'development')
        }), 500

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print(f"Database initialized at: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Test database connection after models are defined
        try:
            farmer_count = Farmer.query.count()
            work_count = TractorWork.query.count()
            print(f"✅ Database test successful - {farmer_count} farmers, {work_count} works")
        except Exception as e:
            print(f"⚠️  Database test failed: {e}")
        
        # Show database info
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'mysql' in db_url.lower():
            print(f"🌐 MySQL database configured")
        else:
            print(f"💻 SQLite database: {os.path.abspath('tractor_management.db')}")

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 