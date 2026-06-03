package com.training.todo.service;

import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class NotificationServiceClientTest {

    @Test
    public void testSendNotification() {
        NotificationServiceClient client = new NotificationServiceClient();
        client.sendNotification("Test message");
    }
}
