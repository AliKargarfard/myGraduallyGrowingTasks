from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    # host = "http://todobackend:8080"

    @task
    def task_list(self):
        self.client.get("/todo/api/v1/task/")

    
