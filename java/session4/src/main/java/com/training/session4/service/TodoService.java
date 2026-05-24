package com.training.session4.service;

import com.training.session4.dto.TodoDTO;
import com.training.session4.dto.TodoResponseDTO;
import java.util.List;

public interface TodoService {
    TodoResponseDTO createTodo(TodoDTO todoDTO);
    List<TodoResponseDTO> getAllTodos();
    TodoResponseDTO getTodoById(Long id);
    TodoResponseDTO updateTodo(Long id, TodoDTO todoDTO);
    void deleteTodo(Long id);
}
