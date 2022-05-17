import uuid
import logging
from behave import given, when, then
from fastapi.testclient import TestClient

from indexer.api.app import app


@given('we have the client configured')
def step_impl(context):
    context.client = TestClient(app)


@given('we have the admin user created')
def step_impl(context):
    context.client.post('/admin')


@given('we have no users in the system')
def step_impl(context):
    response = context.client.get('/users')
    logging.info(response)
    assert response.status_code == 200
    data = response.json()
    assert data['size'] == 0
    users = data['users']
    assert len(users) == 0


@given('we know the name, lastname, email, username and password')
def step_impl(context):
    context.create_user_data = {
        'name': 'One Name',
        'lastname': 'One Lastname',
        'email': 'something@gmail.com',
        'username': 'myusername',
        'password': 'mypassword'
    }


@when('we post the user data to the users endpoint')
def step_impl(context):
    client: TestClient = context.client
    payload = context.create_user_data
    context.response = client.post('/users', json=payload)


@then('a json response is received')
def step_impl(context):
    r = context.response
    rdata = r.json()
    assert rdata is not None
    context.rdata = rdata


@then('a new user is created')
def step_impl(context):
    assert context.response.status_code == 200


@then('the id of the user is returned')
def step_impl(context):
    assert 'id' in context.rdata
    assert context.rdata['id'] is not None


@then('the id is an uuid version 4')
def step_impl(context):
    uid = context.rdata['id']
    assert uuid.UUID(uid, version=4)
    