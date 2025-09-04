
IP Tracking: Security and Analytics in Django
This project is a Django application designed to enhance web security and provide user analytics by logging, analyzing, and acting on client IP addresses. It includes features for basic request logging, IP blacklisting, geolocation, rate limiting, and automated anomaly detection using Celery.

Features
Request Logging: A custom middleware logs the IP address, timestamp, and requested path for every incoming request.

IP Blacklisting: A middleware checks incoming IPs against a database blacklist and returns a 403 Forbidden response to blocked addresses. Includes a management command to easily add IPs to the blacklist.

Geolocation Analytics: Request logs are enriched with country and city data by querying an external geolocation API. Results are cached for 24 hours to improve performance.

Rate Limiting: Protects sensitive views from abuse by applying rate limits. It distinguishes between anonymous users (5 requests/minute) and authenticated users (10 requests/minute).

Anomaly Detection: A background task running on Celery runs hourly to scan logs and flag suspicious IPs based on high request volume or access to sensitive paths.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+

pip and venv

Git

Redis Server (for Celery)

Setup and Installation
Clone the Repository

Bash

git clone <your-repository-url>
cd alx-backend-security
Create and Activate a Virtual Environment

Bash

python3 -m venv venv
source venv/bin/activate
On Windows, use venv\Scripts\activate

Install Python Dependencies
Install all required packages from the requirements.txt file.

Bash

pip install -r requirements.txt
Install and Configure Redis
This project uses Redis as a message broker for Celery.

Bash

# For Debian/Ubuntu-based systems like Zorin OS
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
Apply Database Migrations
Run the migrations to create the necessary database tables for the ip_tracking app.

Bash

python manage.py migrate
Running the Application
To run the full application, you need to start the Django development server and the Celery services in separate terminal windows.

Start the Celery Worker
The worker executes background tasks like anomaly detection.

Bash

# Make sure your virtual environment is activated
celery -A security_project worker -l info
Start the Celery Beat Scheduler
The beat service schedules periodic tasks.

Bash

# In a new terminal, activate the venv
celery -A security_project beat -l info
Start the Django Development Server
This will run the main web application.

Bash

# In a third terminal, activate the venv
python manage.py runserver
The application will be available at http://127.0.0.1:8000/.

Usage
IP Blacklisting
You can block an IP address using the custom management command.

Bash

python manage.py block_ip <ip_address_to_block>
Example:

Bash

python manage.py block_ip 198.51.10