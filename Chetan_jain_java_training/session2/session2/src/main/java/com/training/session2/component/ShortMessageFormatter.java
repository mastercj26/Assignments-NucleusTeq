// component/ShortMessageFormatter.java
package com.training.session2.component;

import com.training.session2.formatter.MessageFormatter;
import org.springframework.stereotype.Component;



@Component
public class ShortMessageFormatter implements MessageFormatter {

    @Override
    public String format(String topic) {
       
        return String.format(" %s: Quick update - check app for details.", topic);
    }

    @Override
    public String getFormatterType() {
        return "SHORT";
    }
}