package com.training.session2.component;

import com.training.session2.formatter.MessageFormatter;
import org.springframework.stereotype.Component;

@Component
public class LongMessageFormatter implements MessageFormatter {

    @Override
    public String format(String topic) {
        return String.format(
           
            
            "Thank you for your time and attention.",
            topic, topic
        );
    }

    @Override
    public String getFormatterType() {
        return "LONG";
    }
}