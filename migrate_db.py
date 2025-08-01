from app import app, db, TractorWork
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        # Check if the new columns exist
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('tractor_work')]
        
        print("Current columns:", columns)
        
        if 'quantity' not in columns:
            print("Adding new columns to database...")
            
            # Add new columns
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE tractor_work ADD COLUMN quantity FLOAT"))
                conn.execute(text("ALTER TABLE tractor_work ADD COLUMN rate_per_unit FLOAT"))
                conn.execute(text("ALTER TABLE tractor_work ADD COLUMN unit_type VARCHAR(20)"))
                conn.commit()
            
            # Migrate existing data
            works = TractorWork.query.all()
            for work in works:
                work.quantity = work.hours_worked if hasattr(work, 'hours_worked') else 0
                work.rate_per_unit = work.rate_per_hour if hasattr(work, 'rate_per_hour') else 0
                
                # Set unit type based on work type
                if work.work_type in ['rotor', 'harvesting', 'seeding', 'irrigation']:
                    work.unit_type = 'hours'
                elif work.work_type == 'transport':
                    work.unit_type = 'trips'
                elif work.work_type == 'plough':
                    work.unit_type = 'acres'
                else:
                    work.unit_type = 'units'
            
            db.session.commit()
            print("Database migration completed successfully!")
        
        # Now handle the old columns - we need to drop them or make them nullable
        if 'hours_worked' in columns:
            print("Removing old columns...")
            try:
                with db.engine.connect() as conn:
                    # First, make sure all data is migrated
                    conn.execute(text("UPDATE tractor_work SET quantity = hours_worked WHERE quantity IS NULL"))
                    conn.execute(text("UPDATE tractor_work SET rate_per_unit = rate_per_hour WHERE rate_per_unit IS NULL"))
                    conn.commit()
                
                # Drop the old columns (SQLite doesn't support DROP COLUMN directly, so we'll recreate the table)
                print("Recreating table structure...")
                with db.engine.connect() as conn:
                    # Create new table with correct structure
                    conn.execute(text("""
                        CREATE TABLE tractor_work_new (
                            id INTEGER PRIMARY KEY,
                            work_type VARCHAR(50) NOT NULL,
                            description TEXT NOT NULL,
                            date DATE NOT NULL,
                            quantity FLOAT NOT NULL,
                            rate_per_unit FLOAT NOT NULL,
                            unit_type VARCHAR(20) NOT NULL,
                            total_amount FLOAT NOT NULL,
                            status VARCHAR(20) DEFAULT 'Pending',
                            farmer_id INTEGER NOT NULL,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (farmer_id) REFERENCES farmer (id)
                        )
                    """))
                    
                    # Copy data from old table to new table
                    conn.execute(text("""
                        INSERT INTO tractor_work_new 
                        (id, work_type, description, date, quantity, rate_per_unit, unit_type, 
                         total_amount, status, farmer_id, created_at)
                        SELECT id, work_type, description, date, quantity, rate_per_unit, unit_type,
                               total_amount, status, farmer_id, created_at
                        FROM tractor_work
                    """))
                    
                    # Drop old table and rename new table
                    conn.execute(text("DROP TABLE tractor_work"))
                    conn.execute(text("ALTER TABLE tractor_work_new RENAME TO tractor_work"))
                    conn.commit()
                
                print("Table structure updated successfully!")
                
            except Exception as e:
                print(f"Error updating table structure: {e}")
                print("Continuing with existing structure...")
        
        print("Database migration completed!")

if __name__ == '__main__':
    migrate_database() 