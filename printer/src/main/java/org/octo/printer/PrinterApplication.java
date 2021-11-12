package org.octo.printer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.core.env.Environment;


@SpringBootApplication
public class PrinterApplication {

	public static void main(String[] args) {
		ApplicationContext c = SpringApplication.run(PrinterApplication.class, args);PrinterApplication p = new PrinterApplication();
		ConfigProperties  con = c.getBean(ConfigProperties.class);
		System.out.println(con.getUserBucketPath());

		// set
		OctoPrintInterface.modelsFolder = con.getUserBucketPath();
	}
}
