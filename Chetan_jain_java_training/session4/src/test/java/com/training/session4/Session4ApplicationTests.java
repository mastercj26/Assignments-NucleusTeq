package com.training.session4;

import com.training.session4.dto.TodoDTO;
import com.training.session4.dto.TodoResponseDTO;
import com.training.session4.model.TodoStatus;
import com.training.session4.service.TodoService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class Session4ApplicationTests {

    @Autowired
    private TodoService todoService;

    @Test
    void contextLoads() {
    }

    @Test
    void testCreateTodo() {
        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Task");
        dto.setDescription("Test Description");
        dto.setStatus(TodoStatus.PENDING);

        TodoResponseDTO created = todoService.createTodo(dto);

        assertNotNull(created.getId());
        assertEquals("Test Task", created.getTitle());
        assertEquals(TodoStatus.PENDING, created.getStatus());
        assertNotNull(created.getCreatedAt());
    }
}
