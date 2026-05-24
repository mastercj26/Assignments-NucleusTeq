package com.training.session4.dto;

import com.training.session4.model.TodoStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class TodoDTO {

    @NotNull(message = "Title cannot be null")
    @Size(min = 3, message = "Title must be at least 3 characters long")
    private String title;

    private String description;

    private TodoStatus status;

    public TodoDTO() {
    }

    public TodoDTO(String title, String description, TodoStatus status) {
        this.title = title;
        this.description = description;
        this.status = status;
    }

    // Getters and Setters
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public TodoStatus getStatus() {
        return status;
    }

    public void setStatus(TodoStatus status) {
        this.status = status;
    }
}
