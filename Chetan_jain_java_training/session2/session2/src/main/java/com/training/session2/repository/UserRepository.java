package com.training.session2.repository;

import com.training.session2.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Repository
public class UserRepository {

    private final List<User> userDatabase = new ArrayList<>();

    public UserRepository() {
        userDatabase.add(new User(1, "Alice Johnson", "alice@example.com", "ADMIN"));
        userDatabase.add(new User(2, "Bob Smith", "bob@example.com", "USER"));
        userDatabase.add(new User(3, "Charlie Brown", "charlie@example.com", "USER"));
        userDatabase.add(new User(4, "Diana Prince", "diana@example.com", "MANAGER"));
    }

    public List<User> findAllUsers() {
        return userDatabase;
    }

    public Optional<User> findUserById(int id) {
        return userDatabase.stream()
                .filter(user -> user.getId() == id)
                .findFirst();
    }

    public User saveUser(User user) {
        int newId = userDatabase.size() + 1;
        user.setId(newId);
        userDatabase.add(user);
        return user;
    }
}