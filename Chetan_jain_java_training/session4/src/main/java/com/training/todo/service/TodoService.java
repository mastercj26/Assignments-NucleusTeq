package com.training.todo.service;

import com.training.todo.dto.TodoDTO;
import com.training.todo.model.Todo;
import com.training.todo.model.TodoStatus;
import com.training.todo.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class TodoService {

    private final TodoRepository todoRepository;

    public TodoService(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    public Todo createTodo(TodoDTO todoDTO) {
        Todo todo = new Todo();
        todo.setTitle(todoDTO.getTitle());
        todo.setDescription(todoDTO.getDescription());
        
        if (todoDTO.getStatus() == null) {
            todo.setStatus(TodoStatus.PENDING);
        } else {
            todo.setStatus(todoDTO.getStatus());
        }
        
        todo.setCreatedAt(LocalDateTime.now());
        return todoRepository.save(todo);
    }

    public List<Todo> getAllTodos() {
        return todoRepository.findAll();
    }

    public Todo getTodoById(Long id) {
        return todoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Todo not found with id: " + id));
    }

    public Todo updateTodo(Long id, TodoDTO todoDTO) {
        Todo existingTodo = todoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Todo not found with id: " + id));

        // Status transition logic
        if (todoDTO.getStatus() != null && !existingTodo.getStatus().equals(todoDTO.getStatus())) {
            // PENDING -> COMPLETED or COMPLETED -> PENDING are the only transitions
            // Since there are only two, any change is a valid transition according to requirements
            // (Wait, the requirements say "Allowed transitions: PENDING -> COMPLETED, COMPLETED -> PENDING")
            // This means any change between these two is allowed.
            existingTodo.setStatus(todoDTO.getStatus());
        }

        existingTodo.setTitle(todoDTO.getTitle());
        existingTodo.setDescription(todoDTO.getDescription());

        return todoRepository.save(existingTodo);
    }

    public void deleteTodo(Long id) {
        if (!todoRepository.existsById(id)) {
            throw new RuntimeException("Todo not found with id: " + id);
        }
        todoRepository.deleteById(id);
    }
}
