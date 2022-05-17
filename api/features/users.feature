Feature: microservice users management

    Background: requirements of the feature
        Given we have the client configured
        Given we have the admin user created

    Scenario: create a user in the microservice
        Given we have no users in the system
        And we know the name, lastname, email, username and password
            When we post the user data to the users endpoint
            Then a json response is received
            And a new user is created
            And the id of the user is returned
            And the id is an uuid version 4
            

