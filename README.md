# BLOOD – Blood Bank Application
## Milestone 1: Local Development

> "Donate Blood, Save Lives"

A complete Flask web application for managing blood donations and requests in a local development environment. This application allows donors to register and manage their donations, while requestors can create and manage blood requests with AI-powered blood type compatibility matching.

---

## 🩸 Features

### User Management
- **Two User Roles**: Donor and Requestor
- **Secure Registration**: Email-based account creation with password hashing
- **Session Management**: Flask sessions for authentication
- **Role-Based Access**: Separate dashboards and functionalities for each role

### Blood Donation Workflow
- **Blood Requests**: Requestors can create blood requests specifying blood group and units needed
- **Request Status Tracking**: Status lifecycle includes Requested → Accepted → Confirmed
- **Donor Matching**: AI engine automatically matches donors with compatible blood groups
- **Donation History**: Complete tracking of all donations made by each donor

### AI Compatibility Engine
- **Rule-Based Expert System**: Medical-standard blood type compatibility rules
- **Automatic Filtering**: Donors see only compatible requests
- **Real-time Matching**: Dynamic updates when new requests or donors join
- **Compatibility Labels**: "AI Recommended Compatible Donors" display throughout the app

### User Interfaces
- **Responsive Design**: Mobile-friendly layout with CSS Grid and Flexbox
- **Interactive Dashboards**: Role-specific views for donors and requestors
- **Flash Messages**: Real-time feedback for all user actions
- **Donor Profiles**: Detailed donor information with donation history

---

## 📁 Project Structure

```
BLOODBANK/
│
├── app.py                          # Main Flask application
├── ai_engine.py                   # Blood compatibility AI module
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── templates/                     # Jinja2 HTML templates
│   ├── index.html                # Home page
│   ├── register_type.html        # Role selection (Donor/Requestor)
│   ├── register.html             # Registration form
│   ├── login_type.html           # Login role selection
│   ├── login.html                # Login form
│   ├── dashboard.html            # Role-based dashboard
│   ├── request.html              # Create blood request
│   ├── donors.html               # View all donors
│   ├── donor_profile.html        # Donor profile & history
│   └── confirmation.html         # Donation confirmation
│
└── static/                        # Static assets
    └── css/
        └── style.css            # Application styling
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd path/to/BLOODBANK
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Start the Application
```bash
python app.py
```

### Expected Output
```
======================================================================
  BLOOD – Blood Bank Application
  Donate Blood, Save Lives
======================================================================

Starting Flask application in DEBUG mode...
Access the application at: http://127.0.0.1:5000

Press Ctrl+C to stop the server.
```

### Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📊 User Flows

### Donor Flow
1. **Register**: Click "Register" → Select "Register as Donor" → Enter details including blood group
2. **Login**: Click "Login" → Select "Login as Donor" → Enter credentials
3. **Dashboard**: View all compatible blood requests based on your blood group
4. **Accept Request**: Click "Accept & Donate" on a compatible request
5. **Track History**: View all your donations in the donation history section
6. **View Donors**: Browse other donors and their profiles

### Requestor Flow
1. **Register**: Click "Register" → Select "Register as Requestor" → Enter details
2. **Login**: Click "Login" → Select "Login as Requestor" → Enter credentials
3. **Create Request**: Click "Create Request" → Specify blood group and units needed
4. **Monitor Status**: View requests in dashboard with status updates:
   - 🔄 REQUESTED: Waiting for a donor
   - ✓ ACCEPTED: A donor has accepted
   - ✓✓ CONFIRMED: Donation received and confirmed
5. **Confirm Donation**: Once a donor accepts, confirm receipt of blood
6. **View Donors**: Browse compatible donors and their profiles

---

## 🤖 Blood Compatibility AI Engine

The application includes a rule-based expert system for blood type compatibility:

### Compatibility Rules
| Blood Group | Can Receive From |
|---|---|
| O+ | O+, O- |
| O- | O- (Universal Donor) |
| A+ | A+, A-, O+, O- |
| A- | A-, O- |
| B+ | B+, B-, O+, O- |
| B- | B-, O- |
| AB+ | All groups (Universal Recipient) |
| AB- | A-, B-, O-, AB- |

### How AI Integration Works
1. **Request Creation**: When a requestor creates a request, compatibility info is calculated
2. **Donor Filtering**: Donors see only requests compatible with their blood group
3. **Dashboard Display**: "🤖 AI-Recommended Compatible Requests" label shows AI matches
4. **Real-time Updates**: Compatibility updates dynamically as data changes

### AI Engine Functions
```python
# Get compatible blood groups for a requested group
get_compatible_blood_groups('A+')  # Returns: ['A+', 'A-', 'O+', 'O-']

# Filter donors by compatibility
filter_compatible_donors('A+', donor_list)

# Check if specific donor is compatible
is_compatible('O+', 'A+')  # Returns: True
```

---

## 💾 Data Storage (In-Memory)

All data is stored using Python dictionaries and lists in RAM:

### Users Storage
```python
users = {
    'email@example.com': {
        'id': 'donor_a1b2c3d4',
        'name': 'John Doe',
        'email': 'email@example.com',
        'password': 'hashed_password',
        'blood_group': 'A+',
        'role': 'Donor',
        'registered_at': '2026-01-29 10:30:00'
    }
}
```

### Blood Requests Storage
```python
requests_list = [
    {
        'id': 'req_1a2b3c4d',
        'blood_group': 'A+',
        'units': 2,
        'requestor_email': 'user@example.com',
        'requestor_name': 'Jane Smith',
        'donor_email': None,
        'donor_name': None,
        'status': 'Requested',
        'timestamp': '2026-01-29 11:00:00',
        'compatibility_info': ['A+', 'A-', 'O+', 'O-']
    }
]
```

### Donation History Storage
```python
donation_history = {
    'donor@example.com': [
        {
            'request_id': 'req_1a2b3c4d',
            'blood_group': 'A+',
            'requestor_email': 'user@example.com',
            'date_time': '2026-01-29 12:00:00'
        }
    ]
}
```

---

## 🔐 Security Features

- **Password Hashing**: Werkzeug's `generate_password_hash()` for secure password storage
- **Session Management**: Flask session management with secure secret key
- **Input Validation**: All user inputs are validated before processing
- **Role-Based Access**: Routes check user role before allowing access
- **CSRF Protection Ready**: Flask session structure supports CSRF tokens (future enhancement)

---

## 🛣️ API Routes

### Authentication Routes
- `GET /` – Home page
- `GET /register-type` – Select registration role
- `GET/POST /register/<user_type>` – Register new user
- `GET /login-type` – Select login role
- `GET/POST /login/<user_type>` – Login user
- `GET /logout` – Logout user

### Dashboard & Management
- `GET /dashboard` – User dashboard (role-specific)
- `GET/POST /request` – Create blood request (Requestor only)
- `GET /donors` – View all donors
- `GET /donor/<donor_email>` – View donor profile

### Donation Workflow
- `GET/POST /donate-blood/<request_id>` – Accept request and donate
- `GET/POST /confirm/<request_id>` – Confirm donation received

---

## 🧪 Testing the Application

### Sample Test Scenario

1. **Register Test User (Donor)**
   - Email: donor@test.com
   - Password: password123
   - Blood Group: O+

2. **Register Test User (Requestor)**
   - Email: requestor@test.com
   - Password: password123

3. **Create Request**
   - Blood Group: A+
   - Units: 2

4. **Accept Request**
   - Login as donor
   - View compatible requests
   - Accept the A+ request (O+ is compatible)
   - Check donation history

5. **Confirm Donation**
   - Login as requestor
   - View request status (should show ACCEPTED)
   - Click "Confirm Donation Received"
   - Status updates to CONFIRMED

---

## 📚 Technology Stack

| Technology | Purpose |
|---|---|
| **Flask 2.3.3** | Web framework |
| **Python 3.7+** | Programming language |
| **Jinja2** | Template engine (included with Flask) |
| **Werkzeug 2.3.7** | Security utilities (password hashing) |
| **HTML5** | Markup |
| **CSS3** | Styling & responsive design |
| **UUID** | Unique ID generation |
| **datetime** | Date/time handling |

---

## 🔮 Future Enhancements

### Milestone 2 & Beyond
- **Database Integration**
  - AWS RDS or DynamoDB
  - SQLAlchemy ORM
  - Data persistence

- **Cloud Deployment**
  - AWS EC2 or Lambda
  - Docker containerization
  - CI/CD pipeline

- **Advanced Features**
  - Email notifications for donors/requestors
  - Real-time updates with WebSockets
  - Admin dashboard for system monitoring
  - Blood inventory management
  - Advanced search and filtering
  - Rating and review system for donors
  - Geographic location-based matching

- **Analytics & Reporting**
  - Donor statistics dashboard
  - Blood type availability charts
  - Request fulfillment rates
  - Export functionality

- **Security Enhancements**
  - Two-factor authentication
  - OAuth2 integration
  - API rate limiting
  - CSRF token implementation

---

## 🐛 Troubleshooting

### Issue: "Address already in use"
**Solution**: Port 5000 is already in use. Either:
- Kill the process using port 5000
- Modify port in `app.py`: `app.run(..., port=5001)`

### Issue: "Module not found: Flask"
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Data not persisting after restart
**Expected Behavior**: In-memory storage means data is lost on restart. This is by design for Milestone 1. Add a database in Milestone 2.

---

## 📝 Code Comments

The codebase includes comprehensive comments explaining:
- Function purposes and parameters
- Business logic and algorithms
- AI engine compatibility rules
- Data structure definitions
- Route handlers and their purposes

---

## 👨‍💻 Development

### Project Configuration
```python
# app.py configuration
app.secret_key = 'BLOOD_BANK_SECRET_KEY_2026_SECURE'
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Adding New Features
1. Add route handler in `app.py`
2. Create template in `templates/`
3. Add styling to `static/css/style.css`
4. Test with sample data

---

## 📄 License

This project is created for educational and demonstration purposes.

---

## 🤝 Support & Contribution

For issues, suggestions, or improvements:
1. Review the code comments
2. Check the troubleshooting section
3. Verify all dependencies are installed
4. Test with the sample scenario

---

## 📞 Project Metadata

- **Project Name**: BLOOD – Blood Bank Application
- **Version**: 1.0.0 (Milestone 1)
- **Date**: January 2026
- **Environment**: Local Development
- **Status**: Fully Functional

---

## 🙏 Acknowledgments

This application demonstrates:
- Clean MVC-style Flask architecture
- Rule-based AI system for medical compatibility
- In-memory data management
- Responsive web design
- Secure authentication practices
- Real-world business logic implementation

---

**Remember**: "Donate Blood, Save Lives" 🩸

For the next milestone, we'll add database persistence and cloud deployment capabilities!
