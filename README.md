# Product Catalog Application

A full-stack application with Flask backend and React frontend for managing product catalogs.

## Project Structure

```
amalitech_gtp_phase_two_lab_two/
├── backend/
│   ├── app.py
│   ├── .env.example
│   ├── setup_db.sql
│   └── venv/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js
│   │   │   └── ProductCard.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── MyProducts.js
│   │   │   ├── ProductForm.js
│   │   │   ├── ProductList.js
│   │   │   └── Register.js
│   │   ├── api.js
│   │   ├── App.css
│   │   ├── App.js
│   │   └── index.js
│   ├── .env.development
│   ├── .env.production
│   └── package.json
├── nginx.conf.example
└── .gitignore
```

## Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
python3 -m venv venv
. venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install flask flask-sqlalchemy psycopg2-binary flask-jwt-extended flask-bcrypt flask-cors python-dotenv
```

3. Create a .env file based on .env.example:
```bash
cp .env.example .env
# Edit .env with your specific configuration
```

4. Set up PostgreSQL database:

   If using Docker:
   ```bash
   # Access PostgreSQL container
   docker exec -it postgres-db psql -U postgres
   
   # Create database, user, and schema
   CREATE DATABASE catalog;
   CREATE USER catalog_user WITH PASSWORD 'catalog_pass';
   GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog_user;
   
   # Connect to the catalog database
   \c catalog
   
   # Create schema and grant privileges
   CREATE SCHEMA catalog;
   GRANT ALL ON SCHEMA catalog TO catalog_user;
   GRANT ALL ON ALL TABLES IN SCHEMA catalog TO catalog_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA catalog GRANT ALL ON TABLES TO catalog_user;
   ```

   If using local PostgreSQL:
   ```bash
   # Access PostgreSQL
   psql -U postgres
   
   # Create database, user, and schema
   CREATE DATABASE catalog;
   CREATE USER catalog_user WITH PASSWORD 'catalog_pass';
   GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog_user;
   
   # Connect to the catalog database
   \c catalog
   
   # Create schema and grant privileges
   CREATE SCHEMA catalog;
   GRANT ALL ON SCHEMA catalog TO catalog_user;
   GRANT ALL ON ALL TABLES IN SCHEMA catalog TO catalog_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA catalog GRANT ALL ON TABLES TO catalog_user;
   ```

5. Run the Flask application:
```bash
python app.py
```

## Frontend Setup

1. Install Node.js and npm if not already installed

2. Install dependencies:
```bash
cd frontend
npm install
```

3. If you encounter "react-scripts not found" error, try these solutions:
```bash
# Solution 1: Install react-scripts globally
npm install -g react-scripts

# Solution 2: Install react-scripts locally
npm install react-scripts --save

# Solution 3: Use npx to run the build
npx react-scripts build

# Solution 4: Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

4. Configure the API URL:
   - For development: Use the default `.env.development` file
   - For production: Create a `.env.production` file with your API URL
   ```
   REACT_APP_API_URL=/api
   ```

5. Start the React development server:
```bash
npm start
```

6. For production build:
```bash
# If react-scripts is installed globally or locally
npm run build

# Or use npx directly
npx react-scripts build
```

## Nginx Setup for Production

1. Build the React frontend:
```bash
cd frontend
# Use the provided build script
./build-script.sh

# Or build manually
npx react-scripts build
```

2. Configure Nginx:
   - Copy the example configuration file:
   ```bash
   cp nginx.conf.example /etc/nginx/sites-available/product-catalog
   ```
   - Edit the configuration file to match your server setup
   - Create a symbolic link to enable the site:
   ```bash
   ln -s /etc/nginx/sites-available/product-catalog /etc/nginx/sites-enabled/
   ```
   - Test and restart Nginx:
   ```bash
   nginx -t
   systemctl restart nginx
   ```

## Features

- User authentication (register, login, logout)
- JWT-based authentication
- Product management (create, read, update, delete)
- User-specific product views
- Responsive design
- Configurable API endpoint via environment variables
- Nginx-ready for production deployment

## API Endpoints

### Authentication
- POST /register - Register a new user
- POST /login - Login and get access token
- POST /logout - Logout and invalidate token

### Products
- GET /products - Get all products
- GET /products/:id - Get a specific product
- GET /products/user - Get current user's products
- POST /products - Create a new product
- PUT /products/:id - Update a product
- DELETE /products/:id - Delete a product

## Usage

1. Register a new account or login with the test account:
   - Username: testuser
   - Password: password123

2. Browse all products on the Products page
3. View your products on the My Products page
4. Add new products using the Add Product page
5. Edit or delete your products from the My Products page

## Deployment Screenshots

Here are screenshots showing the deployment process and application in action:

1. **1 updated the linux system.png**  
   Screenshot showing the process of updating the Linux system before deployment.

2. **2 installed nginx service.png**  
   Screenshot showing the installation of Nginx web server.

3. **3 install python3 and necessary modules.png**  
   Screenshot showing the installation of Python 3 and required modules.

4. **4 installed postgres.png**  
   Screenshot showing the installation of PostgreSQL database.

5. **5 created postgres database.png**  
   Screenshot showing the creation of the PostgreSQL database for the application.

6. **6 create products table.png**  
   Screenshot showing the creation of the products table in the database.

7. **7 running app.png**  
   Screenshot showing the application running in development mode.

8. **8 tested nginx.png**  
   Screenshot showing the testing of Nginx configuration.

9. **9 view of records in browser.png**  
   Screenshot showing the application displaying product records in the browser.

10. **10 running application using the background service.png**  
    Screenshot showing the application running as a background service.

11. **11 browser after implementing https.png**  
    Screenshot showing the application in the browser after implementing HTTPS.

12. **12 shell after implementing https.png**  
    Screenshot showing the shell commands after implementing HTTPS security.