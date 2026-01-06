# Flask-MongoDB Application

A full-stack web application with a Flask backend connected to MongoDB Atlas and an HTML frontend with user registration capabilities.

## Project Structure

```
flask-mongo/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables (MongoDB URI)
├── frontend/
│   ├── index.html         # User registration form page
│   ├── success.html       # Success page
│   └── styles.css         # CSS styling
├── .env.example           # Example environment variables
└── .gitignore            # Git ignore file
```

## Setup Instructions

### 1. Configure MongoDB Atlas

1. Create a MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. Get your connection string
4. Update `backend/.env` with your MongoDB connection string

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `backend/.env` and add your MongoDB Atlas connection string:

```
MONGODB_URI=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/flask_mongo_db?retryWrites=true&w=majority
DATABASE_NAME=flask_mongo_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 4. Run the Application

```bash
cd backend
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- **GET /** - Serves the user registration form
- **GET /api** - Returns all users from MongoDB as JSON
- **POST /submit** - Handles user registration (expects JSON with name, email, password)
- **GET /success** - Shows success page after registration

## Features

- ✅ User registration with name, email, and password
- ✅ MongoDB Atlas integration
- ✅ Form validation (client-side and server-side)
- ✅ Error handling without page redirection
- ✅ Premium modern UI with animations
- ✅ Responsive design
- ✅ Success page redirect after submission

## Security Notes

⚠️ **Important**: This is a demo application. In production:
- Hash passwords before storing (use bcrypt or similar)
- Implement proper authentication and authorization
- Use HTTPS
- Add CSRF protection
- Implement rate limiting
- Validate and sanitize all inputs

## Technologies Used

- **Backend**: Flask, PyMongo
- **Database**: MongoDB Atlas
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with modern design patterns
