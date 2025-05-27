# EricWriter

A minimalist, distraction-free writing application inspired by Zenwriter.app. EricWriter provides a clean, focused environment for your thoughts with powerful customization options and seamless document management.

## 👨‍💻 Author

**Eric Menzie** - Creator and Developer
Vibe coded with the help of "The Future Sound of London" and "Liquid Drum and Bass 2025 | Chill DnB" playlist. 
Check them out on Spotify, and my music at "liighthouse".

## ✨ Features

### 🎨 **Theme System**
- **5 Built-in Themes**: Minimalist, Cyberpunk, Beach Vacation, Major City, and Outer Space
- **Custom Theme Builder**: Create your own theme with:
  - Adjustable font size (12px - 24px)
  - Custom background colors with gradient effects
  - Personalized text and accent colors
  - Real-time preview as you customize

### 📝 **Writing Experience**
- **Distraction-Free Interface**: Clean, minimal design focused on your content
- **Auto-Save**: Your work is automatically saved as you type
- **Rich Text Editor**: Contenteditable interface with placeholder text
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 📁 **Document Management**
- **Sidebar Navigation**: Quick access to all your documents
- **Document Tiles**: Shows title and last modified date
- **Delete with Confirmation**: Safe deletion with "Are you sure?" modal
- **New Document**: Instantly create new documents with one click
- **Active Document Highlighting**: Visual indicator of currently open document

### 🔐 **User Authentication**
- **Secure Registration/Login**: Individual user accounts with password hashing
- **Session Management**: Persistent login sessions
- **CSRF Protection**: Security against cross-site request forgery
- **User-Specific Documents**: Each user sees only their own documents

### 🛠 **Technical Features**
- **Database Migrations**: Proper schema versioning with Flask-Migrate
- **RESTful API**: Clean API endpoints for document operations
- **Theme Persistence**: Settings saved per user in database
- **Local Storage Backup**: Client-side theme caching for performance

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd EricWriter
```

2. **Create a virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up the database:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run the development server:**
```bash
flask run
```

6. **Open your browser:**
Visit `http://localhost:5000` to start writing!

## 📖 Usage Guide

### Getting Started
1. **Register an Account**: Create your personal writing space
2. **Choose a Theme**: Select from built-in themes or create a custom one
3. **Start Writing**: Click "New" to create your first document
4. **Auto-Save**: Your work saves automatically as you type

### Theme Customization
1. Go to **Settings** from the navigation bar
2. Select **Custom** theme tile
3. Adjust font size with the slider
4. Pick your preferred colors using color pickers:
   - **Primary Background**: Creates a gradient effect (your color → white)
   - **Secondary Background**: Used for panels and modals
   - **Primary/Secondary Text**: Main and secondary text colors
   - **Accent Color**: Highlights and interactive elements
5. Click **Apply Custom Theme** to save

### Document Management
- **Create**: Click "New" button in sidebar
- **Open**: Click any document tile in sidebar
- **Delete**: Hover over document tile and click the "×" button
- **Auto-Save**: Documents save automatically every second after changes

## 🏗 Architecture

### Backend (Flask)
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User session management
- **Flask-Migrate**: Database migrations
- **Flask-WTF**: CSRF protection

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **CSS Variables**: Dynamic theming system
- **Responsive Design**: Mobile-first approach
- **Local Storage**: Client-side caching

### Database Schema
- **Users**: Authentication and theme preferences
- **Documents**: User-specific content storage
- **Migrations**: Version-controlled schema changes

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ericwriter.db  # or PostgreSQL URL for production
```

### Production Deployment
For production, consider:
- Using PostgreSQL instead of SQLite
- Setting a strong SECRET_KEY
- Enabling HTTPS
- Using a production WSGI server (Gunicorn, uWSGI)

## 🎯 Roadmap

- [ ] Export documents (PDF, Markdown, TXT)
- [ ] Document search functionality
- [ ] Collaborative editing
- [ ] Mobile app versions
- [ ] Cloud synchronization
- [ ] More theme options
- [ ] Keyboard shortcuts
- [ ] Word count statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
