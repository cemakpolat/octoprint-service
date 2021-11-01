package org.octo.printer;

/**
 * @author cemakpolat
 */

import java.util.concurrent.atomic.AtomicLong;

import org.octo.printer.models.PrinterStatus;
import org.octo.printer.models.SelectedProduct;
import org.octo.printer.models.Status;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PrinterStatusController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();
    String apiKey = "1D8DF67AD9594E81A44830CF33936F55";
    String octoprintURL = "http://127.0.0.1:5000";
    OctoPrintInterface printer = new OctoPrintInterface(octoprintURL,apiKey);


    @GetMapping("/gretings")
    public PrinterStatus greetings(@RequestParam(value = "name", defaultValue = "Levin! Wie geht es dir?") String name) {
        return new PrinterStatus(counter.incrementAndGet(), String.format(template, name));
    }
    @GetMapping("/printerStatus")
    public PrinterStatus printerStatus(@RequestParam(value = "name", defaultValue = "Levin! Wie geht es dir?") String name) {
        return new PrinterStatus(1,printer.getPrinterCurrentState());
    }

    @GetMapping("/selectProduct")
    public Status sendSelectedProduct(@RequestParam(value = "product", defaultValue = "Levin! Wie geht es dir?") String selectedProduct) {
        SelectedProduct prod = new SelectedProduct(counter.incrementAndGet(), String.format(template, selectedProduct));
        // select the printer, printer id and the development id
        String status = "";
        System.out.println("model:"+selectedProduct);
        System.out.println(printer.isPrinterConnected());
        printer.transferFileToPrinter(selectedProduct);
        printer.printModel(selectedProduct);
        //printer.printModel("palm-coin_02mm_pla_mk3s_36m.gcode");
        if (selectedProduct != null){

            printer.printModel(selectedProduct);

            status = printer.getPrinterCurrentState();
        }
        return new Status(status);
    }
}