from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):

    def test_creates_user(self):
        user = User.objects.create_user("aman", "aman@gmail.com", "password123!@")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, "aman@gmail.com")
    
    
    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username= "", email= "aman@gmail.com", password= "password123!@")
        # self.assertRaisesMessage(ValueError, "The given username must be set")
    
    
    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user(username= "", email= "aman@gmail.com", password= "password123!@")
    
    
    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username= "aman", email= "", password= "password123!@")
        self.assertRaisesMessage(ValueError, "The given username must be set")
    

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(username= "aman", email= "", password= "password123!@")
    
    
    def test_creates_super_user(self):
        user = User.objects.create_superuser("aman", "aman@gmail.com", "password123!@")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, "aman@gmail.com")
    

    def test_no_super_user_without_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(username= "aman", email= "aman@gmail.com", password= "password123!@", is_staff= False)
    

    def test_no_super_user_without_is_super_user_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(username= "aman", email= "aman@gmail.com", password= "password123!@", is_superuser= False)
    
    
