package com.training.todo.controller;

import com.training.todo.dto.TodoDTO;
import com.training.todo.model.Todo;
import com.training.todo.model.TodoStatus;
import com.training.todo.service.TodoService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TodoController.class)
public class TodoControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TodoService todoService;

    @Test
    public void testCreateTodo() throws Exception {
        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Test Title");

        when(todoService.createTodo(any(TodoDTO.class))).thenReturn(todo);

        mockMvc.perform(post("/todos")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Test Title\", \"description\": \"Test Desc\", \"status\": \"PENDING\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title").value("Test Title"));
    }

    @Test
    public void testGetAllTodos() throws Exception {
        Todo t1 = new Todo();
        t1.setTitle("T1");
        when(todoService.getAllTodos()).thenReturn(Arrays.asList(t1));

        mockMvc.perform(get("/todos"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("T1"));
    }

    @Test
    public void testGetTodoById() throws Exception {
        Todo todo = new Todo();
        todo.setId(1L);
        when(todoService.getTodoById(1L)).thenReturn(todo);

        mockMvc.perform(get("/todos/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1));
    }

    @Test
    public void testUpdateTodo() throws Exception {
        Todo todo = new Todo();
        todo.setId(1L);
        todo.setTitle("Updated");

        when(todoService.updateTodo(eq(1L), any(TodoDTO.class))).thenReturn(todo);

        mockMvc.perform(put("/todos/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Updated\", \"description\": \"Test Desc\", \"status\": \"COMPLETED\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated"));
    }

    @Test
    public void testDeleteTodo() throws Exception {
        mockMvc.perform(delete("/todos/1"))
                .andExpect(status().isOk())
                .andExpect(content().string("Todo deleted successfully"));
    }

    @Test
    public void testGetTodoById_NotFound() throws Exception {
        when(todoService.getTodoById(1L)).thenThrow(new RuntimeException("Todo not found with id: 1"));

        mockMvc.perform(get("/todos/1"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Todo not found with id: 1"));
    }

    @Test
    public void testGeneralException() throws Exception {
        when(todoService.getAllTodos()).thenThrow(new RuntimeException("Unexpected"));

        mockMvc.perform(get("/todos"))
                .andExpect(status().isNotFound());
    }
}
