# **Real-Time Chat Backend**

## **🚀 Features**

- **Auth**: Register/Login with JWT
- **Chat**: Create & join rooms, send messages via WebSockets
- **History**: Retrieve past messages via API

## **🛠️ Dependencies**
This project requires the following Python packages:

```txt
Django==5.1.6
djangorestframework==3.15.2
djangorestframework_simplejwt==5.4.0
channels==4.2.0
channels_redis==4.2.1
daphne==4.1.2
asgiref==3.8.1
redis==5.2.1
PyJWT==2.10.1
requests==2.32.3
sqlparse==0.5.3
```

To install dependencies, run:
```bash
pip install -r requirements.txt
```

## **🛠️ Setup**

```bash
git clone https://github.com/zainab-salah/chat_backend
cd chat_backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

## **🔹 API Endpoints**

### **Auth**

#### **1️⃣ Register User**

**Endpoint:** `POST /api/register/` **Request Body:**

```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
}
```

**Response:**

```json
{
    "user": {
        "id": 1,
        "username": "john",
        "email": "john@example.com"
    },
    "tokens": {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    }
}
```

#### **2️⃣ Login**

**Endpoint:** `POST /api/token/` **Request Body:**

```json
{
    "username": "john",
    "password": "password123"
}
```

**Response:**
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

### **Chat**
#### **3️⃣ List Chat Rooms**
**Endpoint:** `GET /api/chatrooms/`
**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```
**Response:**
```json
[
    {"id": 1, "name": "room1", "created_at": "2024-02-15T12:00:00Z"},
    {"id": 2, "name": "room2", "created_at": "2024-02-15T12:05:00Z"}
]
```

#### **4️⃣ Create Chat Room**
**Endpoint:** `POST /api/chatrooms/` **Headers:**

```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Request Body:**

```json
{
    "name": "room1"
}
```

**Response:**
```json
{
    "id": 1, "name": "room1", "created_at": "2024-02-15T12:00:00Z"
}
```

#### **5️⃣ Fetch Chat History**

**Endpoint:** `GET /api/messages/<room_name>/` **Headers:**

```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Response:**
```json
[
    {
        "id": 1,
        "user": "john",
        "chatroom": "room1",
        "content": "Hello, world!",
        "timestamp": "2024-02-15T12:00:00Z"
    }
]
```

## **🔹 WebSocket**

```bash
ws://127.0.0.1:8000/ws/chat/<room_name>/?token=<JWT>
```

**Example WebSocket Connection:**

```javascript
let socket = new WebSocket("ws://127.0.0.1:8000/ws/chat/room1/?token=YOUR_JWT_TOKEN");

socket.onopen = function() {
    console.log("Connected to WebSocket");
    socket.send(JSON.stringify({
        "message": "Hello from User!"
    }));
};

socket.onmessage = function(event) {
    console.log("Received:", event.data);
};
```

## **🔹 Testing**

1. Register & Login (`/api/register/`, `/api/token/`)
2. Create & Join Room (`/api/chatrooms/`)
3. Connect WebSocket (`ws://...`), send messages
4. Fetch chat history (`/api/messages/room1/`)

## **🛠️ Deployment**

```bash
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```


