package org.octo.printer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PrinterApplication {

	public static void main(String[] args) {

		Device device = new Device();
		System.out.println(device);
		SpringApplication.run(PrinterApplication.class, args);


	}

}
