# Technical Assessment: Real-Time Chat Application

## Project Overview
Create a simple real-time chat application that allows users to communicate in different chat rooms. This project will demonstrate your ability to work with Django and React, implement real-time features, and design efficient database schemas.

## Core Requirements

### Backend (Django)
1. Authentication:
   - Simple token-based authentication
   - Register and login endpoints

2. Chat Features:
   - Create and join chat rooms
   - Send and receive messages in real-time using WebSockets
   - Store chat history

3. Database Design:
   - Design an efficient schema for users, chat rooms, and messages
   - Include proper relationships and indexes
   - Document your database design decisions

### Frontend (React)
1. Core Features:
   - Login form
   - Chat room list
   - Chat interface with message history
   - Real-time message updates

2. Technical Requirements:
   - Use WebSocket connection for real-time updates
   - Implement proper state management

## Technical Specifications

### Backend Requirements
- Use Django REST Framework for API endpoints
- Implement Django Channels for WebSocket handling
- Include proper error handling
- Document API endpoints

### Frontend Requirements
- Use functional components with hooks
- Handle WebSocket connections properly
- Implement proper error handling
- Use Tailwind CSS for responsive design

## Deliverables

1. Source Code:
   - Well-organized repository
   - Clear commit history

2. Documentation:
   - README.md with:
     - Setup instructions
     - API documentation
     - Database schema diagram
     - Features list
   - Comments for complex logic

## Evaluation Criteria

1. Code Quality:
   - Clean, maintainable code
   - Proper error handling
   - Code organization

2. Technical Implementation:
   - Real-time functionality
   - Database design
   - Django-React integration

3. Documentation:
   - Clear setup & run instructions


## Setup Instructions Template
The candidate should provide:
1. Requirements list/file.
2. Environment setup steps
3. Running the application locally



## Testing Instructions

1. User Setup:
   - Create two test user accounts in the application
   - Log in with User A in one browser (e.g., Chrome)
   - Log in with User B in a different browser (e.g., Firefox)
   
2. Real-time Testing:
   - Open the same chat group/room in both browsers
   - Send messages from User A and verify they appear instantly in User B's browser
   - Send messages from User B and verify they appear instantly in User A's browser
   - Verify that message timestamps and sender information are correct

This will demonstrate the real-time WebSocket functionality of the group chat feature.



