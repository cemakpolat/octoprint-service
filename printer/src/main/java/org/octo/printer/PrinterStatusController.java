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

    @GetMapping("/printerStatus")
    public PrinterStatus printerStatus(@RequestParam(value = "name", defaultValue = "Levin! Wie geht es dir?") String name) {
        return new PrinterStatus(counter.incrementAndGet(), String.format(template, name));
    }

    @PostMapping("/selectProduct")
    public Status sendSelectedProduct(@RequestParam(value = "product", defaultValue = "Levin! Wie geht es dir?") String selectedProduct) {
        SelectedProduct prod = new SelectedProduct(counter.incrementAndGet(), String.format(template, selectedProduct));

        return new Status("Message is sent!");
    }
}