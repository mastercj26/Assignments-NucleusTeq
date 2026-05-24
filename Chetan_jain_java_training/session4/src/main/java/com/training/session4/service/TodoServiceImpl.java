package com.training.session4.service;

import com.training.session4.dto.TodoDTO;
import com.training.session4.dto.TodoResponseDTO;
import com.training.session4.exception.ResourceNotFoundException;
import com.training.session4.model.Todo;
import com.training.session4.model.TodoStatus;
import com.training.session4.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class TodoServiceImpl implements TodoService {

    private final TodoRepository todoRepository;

    // Constructor Injection
    public TodoServiceImpl(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    @Override
    public TodoResponseDTO createTodo(TodoDTO todoDTO) {
        Todo todo = new Todo();
        todo.setTitle(todoDTO.getTitle());
        todo.setDescription(todoDTO.getDescription());
        
        // Default status = PENDING if not provided
        if (todoDTO.getStatus() == null) {
            todo.setStatus(TodoStatus.PENDING);
        } else {
            todo.setStatus(todoDTO.getStatus());
        }
        
        // Set createdAt automatically
        todo.setCreatedAt(LocalDateTime.now());
        
        Todo savedTodo = todoRepository.save(todo);
        return mapToResponseDTO(savedTodo);
    }

    @Override
    public List<TodoResponseDTO> getAllTodos() {
        return todoRepository.findAll().stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    @Override
    public TodoResponseDTO getTodoById(Long id) {
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));
        return mapToResponseDTO(todo);
    }

    @Override
    public TodoResponseDTO updateTodo(Long id, TodoDTO todoDTO) {
        Todo existingTodo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));
        
        // Manual mapping and update
        existingTodo.setTitle(todoDTO.getTitle());
        existingTodo.setDescription(todoDTO.getDescription());
        
        // Allowed transitions: PENDING <-> COMPLETED
        if (todoDTO.getStatus() != null) {
            existingTodo.setStatus(todoDTO.getStatus());
        }
        
        Todo updatedTodo = todoRepository.save(existingTodo);
        return mapToResponseDTO(updatedTodo);
    }

    @Override
    public void deleteTodo(Long id) {
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));
        todoRepository.delete(todo);
    }

    // Manual DTO Mapping
    private TodoResponseDTO mapToResponseDTO(Todo todo) {
        TodoResponseDTO responseDTO = new TodoResponseDTO();
        responseDTO.setId(todo.getId());
        responseDTO.setTitle(todo.getTitle());
        responseDTO.setDescription(todo.getDescription());
        responseDTO.setStatus(todo.getStatus());
        responseDTO.setCreatedAt(todo.getCreatedAt());
        return responseDTO;
    }
}
