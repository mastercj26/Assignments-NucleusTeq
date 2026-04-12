package com.training.session2.formatter;

public interface MessageFormatter {

    String format(String topic);

    String getFormatterType();
}