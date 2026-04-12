package Chetan_jain_java_training.session2.session2.src.main.java.com.training.session2.exception;

public class UserNotFoundException extends RuntimeException {

    private final int userId;

    public UserNotFoundException(int userId) {
        super("User not found with ID: " + userId);
        this.userId = userId;
    }

    public int getUserId() {
        return userId;
    }
}