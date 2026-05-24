package com.training.session4.controller;

import com.training.session4.dto.TodoDTO;
import com.training.session4.dto.TodoResponseDTO;
import com.training.session4.service.TodoService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoService todoService;

    // Constructor Injection
    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    @PostMapping
    public ResponseEntity<TodoResponseDTO> createTodo(@Valid @RequestBody TodoDTO todoDTO) {
        TodoResponseDTO createdTodo = todoService.createTodo(todoDTO);
        return new ResponseEntity<>(createdTodo, HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<TodoResponseDTO>> getAllTodos() {
        List<TodoResponseDTO> todos = todoService.getAllTodos();
        return new ResponseEntity<>(todos, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> getTodoById(@PathVariable Long id) {
        TodoResponseDTO todo = todoService.getTodoById(id);
        return new ResponseEntity<>(todo, HttpStatus.OK);
    }

    @PutMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> updateTodo(@PathVariable Long id, @Valid @RequestBody TodoDTO todoDTO) {
        TodoResponseDTO updatedTodo = todoService.updateTodo(id, todoDTO);
        return new ResponseEntity<>(updatedTodo, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        todoService.deleteTodo(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
