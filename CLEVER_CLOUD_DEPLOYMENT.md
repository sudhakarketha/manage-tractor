# 🚀 Clever Cloud Deployment Guide with MySQL

## **🌐 Deploy to Clever Cloud with MySQL Database**

### **Step 1: Prepare Your Application**

Your application is now configured to use:
- **Local Development**: SQLite database
- **Clever Cloud Deployment**: MySQL database

### **Step 2: Create Clever Cloud Account**

1. **Visit**: https://www.clever-cloud.com/
2. **Sign up** for a free account
3. **Verify your email**

### **Step 3: Create MySQL Database**

1. **Go to Clever Cloud Dashboard**
2. **Click "Create" → "Add-on"**
3. **Select "MySQL"**
4. **Choose plan** (Free tier available)
5. **Name your database** (e.g., "tractor-management-db")
6. **Click "Create"**

### **Step 4: Create Web Application**

1. **Click "Create" → "Application"**
2. **Connect your Git repository**:
   - **GitHub**: Connect your GitHub account
   - **Select repository**: `manage-tractor`
   - **Branch**: `main`

3. **Configure Application**:
   - **Name**: `tractor-management-app`
   - **Region**: Choose closest to you
   - **Instance Type**: Free tier

### **Step 5: Link Database to Application**

1. **In your application dashboard**
2. **Go to "Environment Variables"**
3. **Add these variables**:
   ```
   MYSQL_ADDON_URI = (Copy from MySQL addon dashboard)
   SECRET_KEY = your-secret-key-here
   FLASK_ENV = production
   ```

### **Step 6: Configure Build Settings**

1. **Go to "Build & Deploy"**
2. **Set Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Start Command**:
   ```bash
   gunicorn app:app
   ```

### **Step 7: Deploy**

1. **Click "Deploy"**
2. **Wait for build to complete**
3. **Check logs** for any errors

## **🔧 Database Configuration**

### **Environment Variables**

Clever Cloud automatically provides:
- `MYSQL_ADDON_URI`: MySQL connection string
- `MYSQL_ADDON_HOST`: Database host
- `MYSQL_ADDON_PORT`: Database port
- `MYSQL_ADDON_DB`: Database name
- `MYSQL_ADDON_USER`: Database username
- `MYSQL_ADDON_PASSWORD`: Database password

### **Database Tables**

The application will automatically create these tables:

```sql
-- Farmer table
CREATE TABLE farmer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(120) UNIQUE,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tractor work table
CREATE TABLE tractor_work (
    id INT AUTO_INCREMENT PRIMARY KEY,
    work_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    quantity FLOAT NOT NULL,
    rate_per_unit FLOAT NOT NULL,
    unit_type VARCHAR(20) NOT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    farmer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(farmer_id) REFERENCES farmer(id)
);
```

## **✅ Verification Steps**

### **1. Check Application URL**
After deployment, visit your app URL:
```
https://your-app-name.cleverapps.io
```

### **2. Test Database Connection**
Visit: `https://your-app-name.cleverapps.io/test-db`

Should show:
```json
{
  "status": "success",
  "database_type": "MySQL",
  "farmer_count": 0,
  "work_count": 0,
  "message": "MySQL database connection working"
}
```

### **3. Test Data Saving**
1. **Add a farmer** via web form
2. **Add a work** via web form
3. **Check if data persists** after refresh

## **🔍 Troubleshooting**

### **Common Issues:**

#### **1. Database Connection Failed**
- **Check**: Environment variables are set correctly
- **Verify**: MySQL addon is running
- **Test**: Database connection in Clever Cloud dashboard

#### **2. Tables Not Created**
- **Check**: Application logs for errors
- **Verify**: Database permissions
- **Manual**: Create tables if needed

#### **3. Build Failed**
- **Check**: `requirements.txt` is correct
- **Verify**: Python version compatibility
- **Test**: Local build with same dependencies

### **Logs and Debugging**

1. **View Application Logs**:
   - Go to your app dashboard
   - Click "Logs" tab
   - Look for database connection messages

2. **View Database Logs**:
   - Go to MySQL addon dashboard
   - Click "Logs" tab
   - Check for connection issues

## **📊 Database Management**

### **Access MySQL Database**

1. **Via Clever Cloud Dashboard**:
   - Go to MySQL addon
   - Click "Open in phpMyAdmin"

2. **Via Command Line**:
   ```bash
   mysql -h host -P port -u username -p database_name
   ```

### **Backup Database**

1. **Export via phpMyAdmin**:
   - Select database
   - Click "Export"
   - Choose SQL format

2. **Automated Backups**:
   - Clever Cloud provides automatic backups
   - Check backup settings in addon dashboard

## **🚀 Performance Optimization**

### **MySQL Optimizations**

1. **Indexes**: Add indexes for frequently queried columns
2. **Connection Pooling**: Configure connection limits
3. **Query Optimization**: Monitor slow queries

### **Application Optimizations**

1. **Caching**: Implement Redis for session storage
2. **Static Files**: Use CDN for static assets
3. **Database Queries**: Optimize queries with JOINs

## **💰 Cost Management**

### **Free Tier Limits**
- **MySQL**: 256MB storage, 10 connections
- **Application**: 512MB RAM, shared CPU
- **Bandwidth**: 100GB/month

### **Scaling Options**
- **Upgrade MySQL**: More storage and connections
- **Upgrade Application**: More RAM and CPU
- **Add Redis**: For caching and sessions

## **🎉 Success Checklist**

- ✅ **Application deployed** to Clever Cloud
- ✅ **MySQL database** created and linked
- ✅ **Environment variables** configured
- ✅ **Database tables** created automatically
- ✅ **Data saving** working in production
- ✅ **Application accessible** via URL
- ✅ **Logs showing** successful database connections

Your tractor management application is now deployed on Clever Cloud with MySQL database! 🚀 