package org.octo.printer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class PrinterApplication {

	public static void main(String[] args) {

		ApplicationContext c = SpringApplication.run(PrinterApplication.class, args);
//		System.out.println("Working Directory = " + System.getProperty("user.dir"));
		ConfigProperties  con = c.getBean(ConfigProperties.class);


		OctoPrintInterface.printableFiles = con.getPrinterModelsPath();
		PrinterController.octoprintURL = con.getPrinterUrl();
		PrinterController.apiKey = con.getPrinterApiKey();
	}
}
