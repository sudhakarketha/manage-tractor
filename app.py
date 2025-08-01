from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, Optional
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tractor_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=False)
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

# Forms
class FarmerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
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
        # Convert empty email to None to avoid unique constraint issues
        email = form.email.data.strip() if form.email.data else None
        
        farmer = Farmer(
            name=form.name.data,
            phone=form.phone.data,
            email=email,
            address=form.address.data
        )
        db.session.add(farmer)
        db.session.commit()
        flash('Farmer added successfully!', 'success')
        return redirect(url_for('farmers'))
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
    works_list = TractorWork.query.order_by(TractorWork.date.desc()).all()
    return render_template('works.html', works=works_list)

@app.route('/works/add', methods=['GET', 'POST'])
def add_work():
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 