package org.octo.printer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

/**
 * @author cemakpolat
 */
@Configuration
@PropertySource("classpath:application.properties")
public class ConfigProperties {

    // passing the key which you set in application.properties
    @Value("${userBucket.path}")
    private String userBucket;

    // getting the value from that key which you set in application.properties

    public String getUserBucketPath() {
        return userBucket;
    }
}
