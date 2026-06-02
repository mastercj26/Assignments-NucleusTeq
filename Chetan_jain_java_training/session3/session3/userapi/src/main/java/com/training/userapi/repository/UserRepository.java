package com.training.userapi.repository;

import com.training.userapi.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class UserRepository {

    private List<User> userList = new ArrayList<>();

    public UserRepository() {
        userList.add(new User(1, "Priya", 25, "ADMIN"));
        userList.add(new User(2, "Rahul", 30, "USER"));
        userList.add(new User(3, "Sneha", 22, "USER"));
        userList.add(new User(4, "Arjun", 30, "MANAGER"));
        userList.add(new User(5, "Meera", 28, "USER"));
        userList.add(new User(6, "Karan", 35, "ADMIN"));
        userList.add(new User(7, "Divya", 25, "USER"));
    }

    public List<User> getAllUsers() {
        return userList;
    }

    public Optional<User> findById(int id) {
        for (User user : userList) {
            if (user.getId() == id) {
                return Optional.of(user);
            }
        }
        return Optional.empty();
    }

    public boolean deleteById(int id) {
        return userList.removeIf(user -> user.getId() == id);
    }

    public void addUser(User user) {
        userList.add(user);
    }

    public int getNextId() {
        if (userList.isEmpty()) {
            return 1;
        }

        int maxId = 0;
        for (User user : userList) {
            if (user.getId() > maxId) {
                maxId = user.getId();
            }
        }
        return maxId + 1;
    }
}