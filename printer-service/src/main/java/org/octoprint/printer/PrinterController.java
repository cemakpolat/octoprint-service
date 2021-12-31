package org.octoprint.printer;

/**
 * @author cemakpolat
 */

import org.octoprint.printer.models.Status;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

@CrossOrigin
@RestController
public class PrinterController {


    public static String apiKey;
    public static String octoprintURL;
    private OctoPrintApiInterface printer; //new OctoPrintInterface(octoprintURL,apiKey);
    private final Boolean virtualModeEnabled = true;
    private final Logger logger = LoggerFactory.getLogger(PrinterController.class);

    private PrinterController() {
        printer = new OctoPrintApiInterface(octoprintURL, apiKey);
    }

    private OctoPrintApiInterface getPrinter(String port) {
        return new OctoPrintApiInterface(octoprintURL + ":" + port, apiKey);
    }

    private OctoPrintApiInterface getPrinter(String url, String port) {
        return new OctoPrintApiInterface(url + ":" + port, apiKey);
    }

    @GetMapping("/printer/connect")
    public Status enableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.UNKNOWN) && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/disconnect")
    public Status disableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.OPERATIONAL) ||
                printer.getPrinterCurrentState().equals(Constants.PrinterState.READY) ||
                printer.getPrinterCurrentState().equals(Constants.PrinterState.CONNECTED)) {
            printer.disconnect();
        } else if (printer.getPrinterCurrentState().equals(Constants.PrinterState.PRINTING)) {
            printer.cancelPrinting();
            printer.disconnect();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/status")
    public Status printerStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.UNKNOWN) && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/stop")
    public Status stopPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.PRINTING)) {
            printer.cancelPrinting();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/pause")
    public Status pausePrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.PRINTING)) {
            printer.pausePrinting();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/resume")
    public Status resumPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.PAUSED)) {
            printer.resumePrinting();
        }
        return new Status(printer.getPrinterCurrentState());
    }

    @GetMapping("/printer/print")
    public Status sendSelectedProduct(@RequestParam(value = "product", defaultValue = "") String selectedProduct,
                                      @RequestParam(value = "port", defaultValue = "") String port) {
        logger.debug("Selected product name:" + selectedProduct + ", given printer port" + port);
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.UNKNOWN) && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }

        String status = "";
        logger.info(printer.isPrinterConnected() + "");
        if (!selectedProduct.equals("")) {
            selectedProduct = selectedProduct + ".gcode";
            printer.transferFileToPrinter(selectedProduct);
            printer.printModel(selectedProduct);
            status = printer.getPrinterCurrentState();
        }
        return new Status(status);
    }

    @GetMapping("/product/status")
    public Status productStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState().equals(Constants.PrinterState.UNKNOWN) && this.virtualModeEnabled) {
            printer.connectWithVirtualPort();
        }
        return new Status(printer.getLatestMeasurements().toString());
    }

}