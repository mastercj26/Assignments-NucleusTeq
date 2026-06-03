package com.training.todo.service;

import com.training.todo.dto.TodoDTO;
import com.training.todo.model.Todo;
import com.training.todo.model.TodoStatus;
import com.training.todo.repository.TodoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class TodoService {

    private static final Logger logger = LoggerFactory.getLogger(TodoService.class);
    private final TodoRepository todoRepository;
    private final NotificationServiceClient notificationServiceClient;

    public TodoService(TodoRepository todoRepository, NotificationServiceClient notificationServiceClient) {
        this.todoRepository = todoRepository;
        this.notificationServiceClient = notificationServiceClient;
    }

    public Todo createTodo(TodoDTO todoDTO) {
        logger.info("Creating new todo with title: " + todoDTO.getTitle());
        Todo todo = new Todo();
        todo.setTitle(todoDTO.getTitle());
        todo.setDescription(todoDTO.getDescription());
        
        if (todoDTO.getStatus() == null) {
            todo.setStatus(TodoStatus.PENDING);
        } else {
            todo.setStatus(todoDTO.getStatus());
        }
        
        todo.setCreatedAt(LocalDateTime.now());
        Todo savedTodo = todoRepository.save(todo);
        
        notificationServiceClient.sendNotification("Notification sent for new TODO: " + savedTodo.getTitle());
        
        return savedTodo;
    }

    public List<Todo> getAllTodos() {
        logger.info("Fetching all todos");
        return todoRepository.findAll();
    }

    public Todo getTodoById(Long id) {
        logger.info("Fetching todo with id: " + id);
        return todoRepository.findById(id)
                .orElseThrow(() -> {
                    logger.error("Todo not found with id: " + id);
                    return new RuntimeException("Todo not found with id: " + id);
                });
    }

    public Todo updateTodo(Long id, TodoDTO todoDTO) {
        logger.info("Updating todo with id: " + id);
        Todo existingTodo = todoRepository.findById(id)
                .orElseThrow(() -> {
                    logger.error("Todo not found with id: " + id);
                    return new RuntimeException("Todo not found with id: " + id);
                });

        if (todoDTO.getStatus() != null && !existingTodo.getStatus().equals(todoDTO.getStatus())) {
            existingTodo.setStatus(todoDTO.getStatus());
        }

        existingTodo.setTitle(todoDTO.getTitle());
        existingTodo.setDescription(todoDTO.getDescription());

        return todoRepository.save(existingTodo);
    }

    public void deleteTodo(Long id) {
        logger.info("Deleting todo with id: " + id);
        if (!todoRepository.existsById(id)) {
            logger.error("Todo not found with id: " + id);
            throw new RuntimeException("Todo not found with id: " + id);
        }
        todoRepository.deleteById(id);
    }
}
