package org.octoprint.printer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

/**
 * @author cemakpolat
 */

@Configuration
@PropertySource("classpath:application.properties")
public class ConfigProperties {

    @Value("${app.title}")
    private String appTitle;

    @Value("${printer.url}")
    private String printerUrl;

    @Value("${printer.apikey}")
    private String printerApiKey;

    @Value("${printer.models.path}")
    private String printerModelsPath;

    public String getAppTitle(){return appTitle;}
    public String getPrinterUrl(){return printerUrl;}
    public String getPrinterApiKey(){return printerApiKey;}
    public String getPrinterModelsPath(){return printerModelsPath;}

}
