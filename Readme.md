This is Project contain API for Chat System like WhatsApp

# Features
1. User Authentication
    - Login method: Phone number and OTP verification.

2. Profile Management
    - Users should be able to edit their profile, including updating their name and profile picture.

3. Chat Functionality
    - Enable users to send, receive, forward, and reply to messages and media.
    - Suggest replies based on the last sent message.

4. Message Scheduling
    - Implement message scheduling capabilities.

5. Event-Based Auto-Sending Messages
   - Automatically send messages for specific events (e.g., Diwali greetings, birthday celebrations).
   - Pick events from the calendar for auto-sending messages.

6. Recurring Messages
   - Allow for the scheduling of recurring messages.

7. Settings
   - Provide a setting to turn the auto-sending and recurring messages feature off and on.
   - Enable sending messages to selected users.

# Setup
You need to place .env file inside 'chat_system/chat_system' along with settings.py containing below information
```
SECRET_KEY=<Your Secret Key>

TWILIO_ACCOUNT_SID=<YOUR TWILIO ACCOUNT SID> # Replace with your Twilio account SID
TWILIO_AUTH_TOKEN=<YOUR TWILIO AUTH TOKEN> # Replace with your Twilio auth token
TWILIO_PHONE_NUMBER='+15005550006' # Replace with your Twilio phone number you bought (this is test phone number provided by twilio)
```

Run below commands
```commandline
python manage.py makemigrations
python manage.py migrate
```
Create Your own superuser
```commandline
python manage.py createsuperuser
```

Provide below details

    - phone_number:+91<valid 10 digit phone number>
    - password: <whatever you want>
    - confirm_password: <same as password>


# Run 
Create Virtual Environment and Install dependency
```commandline
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run Django App
```commandline
python manage.py makemigrations
python manage.py migrate


python manage.py runserver
```

Run Celery and Celery Beat
```commandline
celery -A chat_system worker --beat --scheduler django --loglevel=info
```

# Run Using Docker
```commandline
docker compose up -build
```

# Usage
Now you can start using APIs in Postman.

Note that if you have not bought Number from twilio and set it into .env. You can find OTP using steps below 
    
   - Login admin - using credential you just created above using createsuperuser command
   - Go to "Users" -> "Respective Phone Number" whome you want to login -> find otp and use it in postman collection to verify and login

