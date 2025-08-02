# 📡 API Documentation

Your Tractor Management System now has a complete REST API for saving and managing data!

## 🔗 Base URL
```
https://your-app-name.onrender.com/api
```

## 📋 Available Endpoints

### **👥 Farmers Management**

#### **GET /api/farmers**
Get all farmers
```bash
curl https://your-app-name.onrender.com/api/farmers
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com",
    "address": "123 Farm Road",
    "created_at": "2025-08-01 10:30:00",
    "total_works": 3
  }
]
```

#### **POST /api/farmers**
Add a new farmer
```bash
curl -X POST https://your-app-name.onrender.com/api/farmers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Farmer",
    "phone": "9876543210",
    "email": "farmer@example.com",
    "address": "456 Farm Street"
  }'
```

**Request Body:**
```json
{
  "name": "New Farmer",        // Required
  "phone": "9876543210",       // Optional
  "email": "farmer@example.com", // Optional
  "address": "456 Farm Street"   // Optional
}
```

**Response:**
```json
{
  "message": "Farmer added successfully",
  "farmer": {
    "id": 2,
    "name": "New Farmer",
    "phone": "9876543210",
    "email": "farmer@example.com",
    "address": "456 Farm Street"
  }
}
```

#### **PUT /api/farmers/{id}**
Update a farmer
```bash
curl -X PUT https://your-app-name.onrender.com/api/farmers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "1112223333",
    "email": "updated@example.com"
  }'
```

#### **DELETE /api/farmers/{id}**
Delete a farmer and all associated works
```bash
curl -X DELETE https://your-app-name.onrender.com/api/farmers/1
```

### **🚜 Works Management**

#### **GET /api/works**
Get all works
```bash
curl https://your-app-name.onrender.com/api/works
```

**Response:**
```json
[
  {
    "id": 1,
    "work_type": "harvesting",
    "description": "Wheat harvesting",
    "date": "2025-08-01",
    "quantity": 5.0,
    "rate_per_unit": 500.0,
    "unit_type": "hours",
    "total_amount": 2500.0,
    "status": "Pending",
    "farmer_name": "John Doe"
  }
]
```

#### **POST /api/works**
Add a new work
```bash
curl -X POST https://your-app-name.onrender.com/api/works \
  -H "Content-Type: application/json" \
  -d '{
    "work_type": "harvesting",
    "description": "Wheat harvesting work",
    "date": "2025-08-01",
    "quantity": 5.0,
    "rate_per_unit": 500.0,
    "farmer_id": 1
  }'
```

**Request Body:**
```json
{
  "work_type": "harvesting",     // Required: harvesting, transport, rotor, plough, seeding, irrigation, other
  "description": "Work description", // Required
  "date": "2025-08-01",         // Required: YYYY-MM-DD format
  "quantity": 5.0,              // Required: number
  "rate_per_unit": 500.0,       // Required: number
  "farmer_id": 1                // Required: existing farmer ID
}
```

**Response:**
```json
{
  "message": "Work added successfully",
  "work": {
    "id": 2,
    "work_type": "harvesting",
    "description": "Wheat harvesting work",
    "date": "2025-08-01",
    "quantity": 5.0,
    "rate_per_unit": 500.0,
    "unit_type": "hours",
    "total_amount": 2500.0,
    "status": "Pending",
    "farmer_name": "John Doe"
  }
}
```

#### **PUT /api/works/{id}**
Update work status
```bash
curl -X PUT https://your-app-name.onrender.com/api/works/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Completed"
  }'
```

**Status Options:** `Pending`, `Completed`, `Paid`

#### **DELETE /api/works/{id}**
Delete a work
```bash
curl -X DELETE https://your-app-name.onrender.com/api/works/1
```

## 🔧 Work Types and Units

| Work Type | Unit Type | Description |
|-----------|-----------|-------------|
| `harvesting` | `hours` | Crop harvesting operations |
| `transport` | `trips` | Transportation of goods |
| `rotor` | `hours` | Rotor tiller operations |
| `plough` | `acres` | Ploughing operations |
| `seeding` | `hours` | Seeding operations |
| `irrigation` | `hours` | Irrigation operations |
| `other` | `units` | Custom work types |

## 📱 Mobile App Integration

### **JavaScript Example:**
```javascript
// Add a new farmer
async function addFarmer(farmerData) {
  try {
    const response = await fetch('/api/farmers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(farmerData)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      console.log('Farmer added:', result.farmer);
      return result.farmer;
    } else {
      console.error('Error:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Network error:', error);
    throw error;
  }
}

// Add a new work
async function addWork(workData) {
  try {
    const response = await fetch('/api/works', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workData)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      console.log('Work added:', result.work);
      return result.work;
    } else {
      console.error('Error:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Network error:', error);
    throw error;
  }
}

// Usage examples
addFarmer({
  name: "John Doe",
  phone: "1234567890",
  email: "john@example.com",
  address: "123 Farm Road"
});

addWork({
  work_type: "harvesting",
  description: "Wheat harvesting",
  date: "2025-08-01",
  quantity: 5.0,
  rate_per_unit: 500.0,
  farmer_id: 1
});
```

## ✅ Data Persistence

### **All API operations:**
- ✅ **Save to Database**: Data is permanently stored
- ✅ **Error Handling**: Proper error responses
- ✅ **Validation**: Input validation and constraints
- ✅ **Transactions**: Database rollback on errors
- ✅ **JSON Responses**: Consistent API responses

### **Database Operations:**
- ✅ **CREATE**: POST endpoints save new data
- ✅ **READ**: GET endpoints retrieve data
- ✅ **UPDATE**: PUT endpoints modify data
- ✅ **DELETE**: DELETE endpoints remove data

## 🚨 Error Handling

### **Common Error Responses:**
```json
{
  "error": "Name is required"
}
```

### **HTTP Status Codes:**
- `200` - Success
- `201` - Created successfully
- `400` - Bad request (validation error)
- `404` - Not found
- `500` - Server error

## 🎯 Testing the API

### **Using curl:**
```bash
# Test adding a farmer
curl -X POST http://localhost:5000/api/farmers \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Farmer", "phone": "1234567890"}'

# Test adding a work
curl -X POST http://localhost:5000/api/works \
  -H "Content-Type: application/json" \
  -d '{"work_type": "harvesting", "description": "Test work", "date": "2025-08-01", "quantity": 2.0, "rate_per_unit": 300.0, "farmer_id": 1}'
```

### **Using Postman:**
1. Set method to POST
2. Set URL to `/api/farmers` or `/api/works`
3. Set Content-Type header to `application/json`
4. Add JSON body with required data
5. Send request

Your API is now fully functional for saving and managing data! 🎉 