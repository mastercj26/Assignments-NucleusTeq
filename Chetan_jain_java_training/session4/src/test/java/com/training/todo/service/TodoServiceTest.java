package com.training.todo.service;

import com.training.todo.dto.TodoDTO;
import com.training.todo.model.Todo;
import com.training.todo.model.TodoStatus;
import com.training.todo.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class TodoServiceTest {

    @Mock
    private TodoRepository todoRepository;

    @Mock
    private NotificationServiceClient notificationServiceClient;

    @InjectMocks
    private TodoService todoService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCreateTodo() {
        TodoDTO dto = new TodoDTO("Test Title", "Test Desc", TodoStatus.PENDING);
        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test Title");

        when(todoRepository.save(any(Todo.class))).thenReturn(todo);

        Todo result = todoService.createTodo(dto);

        assertNotNull(result);
        assertEquals("Test Title", result.getTitle());
        verify(todoRepository, times(1)).save(any(Todo.class));
        verify(notificationServiceClient, times(1)).sendNotification(anyString());
    }

    @Test
    public void testGetAllTodos() {
        Todo t1 = new Todo();
        Todo t2 = new Todo();
        when(todoRepository.findAll()).thenReturn(Arrays.asList(t1, t2));

        List<Todo> result = todoService.getAllTodos();

        assertEquals(2, result.size());
        verify(todoRepository, times(1)).findAll();
    }

    @Test
    public void testGetTodoById() {
        Todo todo = new Todo();
        todo.setId(1L);
        when(todoRepository.findById(1L)).thenReturn(Optional.of(todo));

        Todo result = todoService.getTodoById(1L);

        assertNotNull(result);
        assertEquals(1L, result.getId());
    }

    @Test
    public void testGetTodoById_NotFound() {
        when(todoRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class, () -> todoService.getTodoById(1L));
    }

    @Test
    public void testUpdateTodo() {
        Todo existing = new Todo();
        existing.setId(1L);
        existing.setStatus(TodoStatus.PENDING);

        TodoDTO updateDto = new TodoDTO("Updated", "New Desc", TodoStatus.COMPLETED);

        when(todoRepository.findById(1L)).thenReturn(Optional.of(existing));
        when(todoRepository.save(any(Todo.class))).thenReturn(existing);

        Todo result = todoService.updateTodo(1L, updateDto);

        assertNotNull(result);
        assertEquals("Updated", result.getTitle());
        assertEquals(TodoStatus.COMPLETED, result.getStatus());
    }

    @Test
    public void testDeleteTodo() {
        when(todoRepository.existsById(1L)).thenReturn(true);
        doNothing().when(todoRepository).deleteById(1L);

        todoService.deleteTodo(1L);

        verify(todoRepository, times(1)).deleteById(1L);
    }

    @Test
    public void testDeleteTodo_NotFound() {
        when(todoRepository.existsById(1L)).thenReturn(false);

        assertThrows(RuntimeException.class, () -> todoService.deleteTodo(1L));
    }
}
