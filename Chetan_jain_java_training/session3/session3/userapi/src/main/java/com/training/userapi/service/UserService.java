package com.training.userapi.service;

import com.training.userapi.model.User;
import com.training.userapi.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> searchUsers(String name, Integer age, String role) {
        return userRepository.getAllUsers().stream()
                .filter(user -> (name == null || user.getName().equalsIgnoreCase(name)))
                .filter(user -> (age == null || user.getAge() == age))
                .filter(user -> (role == null || user.getRole().equalsIgnoreCase(role)))
                .collect(Collectors.toList());
    }

    public String addUser(User user) {
        if (user.getName() == null || user.getName().isEmpty()) {
            return "Name cannot be empty";
        }
        if (user.getAge() <= 0) {
            return "Age must be greater than 0";
        }
        if (user.getRole() == null || user.getRole().isEmpty()) {
            return "Role cannot be empty";
        }

        user.setId(userRepository.getNextId());
        userRepository.addUser(user);
        return "SUCCESS";
    }

    public String deleteUser(int id, boolean confirm) {
        Optional<User> user = userRepository.findById(id);

        if (user.isEmpty()) {
            return "NOT_FOUND";
        }

        if (!confirm) {
            return "CONFIRMATION_REQUIRED";
        }

        userRepository.deleteById(id);
        return "SUCCESS";
    }
}
