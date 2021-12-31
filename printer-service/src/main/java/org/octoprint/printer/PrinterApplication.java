package org.octoprint.printer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class PrinterApplication {

	public static void main(String[] args) {

		ApplicationContext c = SpringApplication.run(PrinterApplication.class, args);
		Logger logger = LoggerFactory.getLogger(PrinterApplication.class);
		ConfigProperties  con = c.getBean(ConfigProperties.class);
		logger.info(con.getAppTitle()+" starts...");

		OctoPrintApiInterface.printableFiles = con.getPrinterModelsPath();
		PrinterController.octoprintURL = con.getPrinterUrl();
		PrinterController.apiKey = con.getPrinterApiKey();
	}
}
