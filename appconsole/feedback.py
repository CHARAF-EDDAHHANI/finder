#!/usr/bin/env python3

# FeedbackModel class representing a model for user feedback
class feedbackmodel:
    # Constructor method to initialize the FeedbackModel instance
    # Parameters:
    #   - user_name: User's name providing feedback
    #   - email: User's email address
    #   - subject: Subject of the feedback
    #   - message: Detailed feedback message
    
    # Instance attributes set based on provided parameters
    def __init__(self, user_name, email, subject, message):
        self.user_name = user_name
        self.email = email
        self.subject = subject
        self.message = message
