# Todo Application - Session 4

This is a Spring Boot application for managing TODO tasks. It demonstrates clean architecture, logging, and unit testing.

## Features
- CRUD operations for Todo tasks.
- Manual DTO mapping.
- SLF4J logging in Controller and Service layers.
- Unit testing with JUnit 5 and Mockito.
- Simulated NotificationServiceClient.
- Code coverage reporting with JaCoCo.

## Tech Stack
- Java 17
- Spring Boot 3.2.5
- Spring Data JPA
- H2 In-memory Database
- Maven

## How to Run
1. Clone the repository.
2. Navigate to `Chetan_jain_java_training/session4`.
3. Run `mvn spring-boot:run`.

## API Endpoints
- `POST /todos` - Create a new task.
- `GET /todos` - Get all tasks.
- `GET /todos/{id}` - Get a task by ID.
- `PUT /todos/{id}` - Update a task.
- `DELETE /todos/{id}` - Delete a task.

## Running Tests
Run `mvn test` to execute unit tests and generate the JaCoCo coverage report.
The report can be found at `target/site/jacoco/index.html`.
