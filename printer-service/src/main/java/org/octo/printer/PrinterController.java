package org.octo.printer;

/**
 * @author cemakpolat
 */

import java.util.concurrent.atomic.AtomicLong;
import org.octo.printer.models.PrinterStatus;
import org.octo.printer.models.Status;
import org.springframework.web.bind.annotation.*;

@CrossOrigin
@RestController
public class PrinterController {

    private final AtomicLong counter = new AtomicLong();
    public static String apiKey;
    public static String octoprintURL;
    private OctoPrintInterface printer; //new OctoPrintInterface(octoprintURL,apiKey);
    private final Boolean virtualModeEnabled = true;

    private PrinterController() {
        printer = new OctoPrintInterface(octoprintURL, apiKey);
    }

    private OctoPrintInterface getPrinter(String port) {
        return new OctoPrintInterface(this.octoprintURL + ":" + port, apiKey);
    }

    private OctoPrintInterface getPrinter(String url, String port) {
        return new OctoPrintInterface(url + ":" + port, apiKey);
    }

    @GetMapping("/printer/connect")
    public Status enableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN" && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/disconnect")
    public Status disableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "OPERATIONAL" || printer.getPrinterCurrentState() == "READY" || printer.getPrinterCurrentState() == "CONNECTED") {
            printer.disconnect();
        } else if (printer.getPrinterCurrentState() == "PRINTING") {
            printer.cancelPrinting();
            printer.disconnect();
        }
        return new Status(String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/status")
    public Status printerStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN" && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/stop")
    public Status stopPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PRINTING") {
            printer.cancelPrinting();
        }
        return new Status(String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/pause")
    public Status pausePrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PRINTING") {
            printer.pausePrinting();
        }
        return new Status(String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/resume")
    public Status resumPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PAUSED") {
            printer.resumePrinting();
        }
        return new Status(String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/print")
    public Status sendSelectedProduct(@RequestParam(value = "product", defaultValue = "") String selectedProduct,
                                      @RequestParam(value = "port", defaultValue = "") String port) {
        System.out.println("called:" + selectedProduct + " " + port);
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN" && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }

        String status = "";
        System.out.println("model:" + selectedProduct);
        System.out.println(printer.isPrinterConnected());
        selectedProduct = selectedProduct + ".gcode";
        if (selectedProduct != null) {
            printer.transferFileToPrinter(selectedProduct);
            printer.printModel(selectedProduct);
            status = printer.getPrinterCurrentState();
        }
        return new Status(status);
    }

    @GetMapping("/product/status")
    public Status productStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN" && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(printer.getLatestMeasurements().toString());
    }

}