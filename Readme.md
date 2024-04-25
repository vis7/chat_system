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

# Run 
Create Virtual Environment and Install dependency
```commandline
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run Django App
```commandline
python manage.py runserver
```

Run Celery and Celery Beat
```commandline
celery -A chat_system worker --beat --scheduler django --loglevel=info
```

# Run Using Docker
```commandline
docker compose up -b
```
