package com.training.session2.service;

import com.training.session2.formatter.MessageFormatter;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MessageService {

    private final List<MessageFormatter> messageFormatters;

    public MessageService(List<MessageFormatter> messageFormatters) {
        this.messageFormatters = messageFormatters;
    }

    public String getFormattedMessage(String type, String topic) {

        return messageFormatters.stream()
                .filter(formatter -> formatter.getFormatterType().equalsIgnoreCase(type))
                .findFirst()
                .map(formatter -> formatter.format(topic))
                .orElse(getDefaultMessage(type, topic));
    }

    private String getDefaultMessage(String type, String topic) {
        return String.format(
            "Unknown message type '%s'. Available types: SHORT, LONG. Topic: %s",
            type, topic
        );
    }

    public List<String> getAvailableFormatterTypes() {
        return messageFormatters.stream()
                .map(MessageFormatter::getFormatterType)
                .toList();
    }
}