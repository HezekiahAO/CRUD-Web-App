import requests
import uuid

end = "https://todo.pixegami.io"

response = requests.get(end)
print(response)

status_code = response.status_code
print(status_code)

data = response.json()
print(data)

def test_can_call_endpoint():
    response = requests.get(end)
    assert response.status_code == 200

def test_can_create_task():
    payload = {
        "content": "A Story to tell",
        "user_id": "test_user",
        "task_id": "task_id_user",
        "is_done": False,
    }
    create_task_response = requests.put(end + "/create-task", json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(end + f'/get-task/{task_id}')
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload["user_id"]

def test_can_update_task():
    # create a task first
    payload = {
        "content": "A Story to tell",
        "user_id": "test_user",
        "task_id": "task_id_user",
        "is_done": False,
    }
    create_task_response = requests.put(end + "/create-task", json=payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # then update the task
    new_payload = {
        "content": "My Task Updated",
        "user_id": payload["user_id"],
        "task_id": task_id,
        "is_done": True,
    }
    update_task_response = requests.put(end + "/update-task", json=new_payload)
    assert update_task_response.status_code == 200

    # get the task and validate the changes
    get_task_response = requests.get(end + f'/get-task/{task_id}')
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']


def test_can_list_task():
    #Create a task first
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
# List task
    user_id = payload['user_id']    
    list_task_response = list_task("user_id")
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data['tasks']
    assert len(tasks) == n


def test_can_delete_task():
    #Create a task first
    playload = new_task_payload()
    create_task_response = create_task(playload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # Delete task
    delect_task_response = requests.delete(task_id)
    assert delect_task_response.status_code == 200

    # Validate task is deleted    
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    print(get_task_response.status_code)    
    pass


def create_task(payload):
    return requests.put(end + "/create-task", json=payload  )

def update_task(payload):
    return requests.put(end + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(end + f'/get-task/{task_id}')

def list_task(user_id):
    return requests.get(end + f'/list-tasks/{user_id}')

def new_task_payload():
    user_id = f'test_user_{uuid.uuid4().hex}'
    content = "A Story to tell"
    task_id = f'task_{uuid.uuid4().hex}'
    print(f"Creating task for user {user_id} with content {content}")
    return {
        "content": content,
        "user_id": user_id,
        "task_id": task_id,
        "is_done": False,
    }