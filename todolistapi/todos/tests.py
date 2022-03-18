from todos.models import Todo
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class TodoAPITestCase(APITestCase):

    def create_todo(self):
        
        post_data = {
            "title" : "Title For Testing",
            "desc" : "Description For Testing",
        }
        response = self.client.post(reverse("todos"), post_data)

        return response


    def authenticate(self):
        test_user_register_data = {
            "email" : "testinguser@tester123.com",
            "username" : "testuser1",
            "password" : "A really long password that only a test user may have",
        }
        self.client.post(reverse("register"), test_user_register_data)

        test_user_login_data = {
            "email" : "testinguser@tester123.com",
            "password" : "A really long password that only a test user may have",
        }
        response = self.client.post(reverse("login"), test_user_login_data)

        self.client.credentials(HTTP_AUTHORIZATION= "Bearer " + str(response.json().get("token")))

class TestListCreateTodos(TodoAPITestCase):


    def test_should_not_creates_todos_with_no_authentication(self):
        post_data = {
            "title" : "Title For Testing",
            "desc" : "Description For Testing",
        }
        response = self.client.post(reverse("todos"), post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_should_create_todo(self):
        self.authenticate()

        previous_todo_count = Todo.objects.all().count()

        response = self.create_todo()

        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), "Title For Testing")
        self.assertEqual(response.data.get("desc"), "Description For Testing")

    def test_retrieve_all_todos(self):
        self.authenticate()

        response = self.client.get(reverse("todos"))

        self.assertEqual(response.data.get("count"), Todo.objects.all().count())
        self.assertIsInstance(response.data.get("count"), int)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data.get("results"), list)

class TestTodoDetailAPIView(TodoAPITestCase):

    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.get(reverse("todo", kwargs= {"id" : response.data.get("id")}))
        # reverse("todo", kwargs= {"id" : response.data.get("id")})     For giving urls such as, .../todos/1, .../todos/4, etc
        # Here  response contains the data received after a post request
        # Here  res contains the data received after a get request

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get("title"), res.data.get("title"))
        self.assertEqual(response.data.get("desc"), res.data.get("desc"))

        todo = Todo.objects.get(id = response.data.get("id"))
        self.assertEqual(todo.title, res.data.get("title"))
        self.assertEqual(todo.desc, res.data.get("desc"))



    def test_update_one_item(self):
        self.authenticate()
        response = self.create_todo()

        updated_data = {
            "title" : "Another One",
            "is_complete" : True,
        }
        res = self.client.patch(
            reverse("todo", kwargs= {"id" : response.data.get("id")}),
            data= updated_data,
        )

        todo = Todo.objects.get(id = response.data.get("id"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(todo.is_complete, res.data.get("is_complete"))
        self.assertEqual(res.data.get("is_complete"), True)
        self.assertEqual(todo.title, "Another One")
    
    def test_delete_one_item(self):
        self.authenticate()
        response = self.create_todo()

        prev_db_count = Todo.objects.all().count()

        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        res = self.client.delete(reverse("todo", kwargs= {"id" : response.data.get("id")}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)



## Basically when an app has been made, and is ready to be fully operated, through django testing, each functionality can be checked thoroughly