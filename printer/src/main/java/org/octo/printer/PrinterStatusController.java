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
    String octoprintURL = "http://127.0.0.1";
    OctoPrintInterface printer = new OctoPrintInterface(octoprintURL,apiKey);

    /**
     *
     // use case 1
     // assuming that the product is ordered
     // get initial status of the printer
     // send it to the printer from the location
     // print it
     // observe printer and print the status
     // receive the results

     // what are the rules that we have to define here? What kind of use cases
     // 1. Generate the access key and assign the URL
     //Get information from the virtual printer about its actual status
     //Get the existing files on the OctoPrint to print one of them
     //Initiate the printing process of the selected file
     //Monitor the printing process.
     //End of the p rinting process
     //Upload a gcode file through the API to the OctoPrint (where can I find a gcode file, download from open source projects)
     //Initiate and monitor the process
     //End the printing process.
     // A single program that returns all request to the other parts
     // 1. how to handle muliple request
     //
     */

    private OctoPrintInterface getPrinter(String port){
        String octoprintURL = "http://127.0.0.1"+":"+port;
        return new OctoPrintInterface(octoprintURL,apiKey);
    }

    @GetMapping("/printer/virtual/connect")
    public PrinterStatus enableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN"){
            printer.connectWithVirtualPort();
        }
        return new PrinterStatus(counter.incrementAndGet(), String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/virtual/disconnect")
    public PrinterStatus disableVirtualPrinter(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "OPERATIONAL" || printer.getPrinterCurrentState() == "READY" || printer.getPrinterCurrentState() == "CONNECTED"){
            printer.disconnect();
        }else if (printer.getPrinterCurrentState() == "PRINTING"){
            printer.cancelPrinting();
            printer.disconnect();
        }
        return new PrinterStatus(counter.incrementAndGet(), String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/status")
    public PrinterStatus printerStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN"){
            printer.connectWithVirtualPort();
        }
        return new PrinterStatus(1,printer.getPrinterCurrentState());
    }
    @GetMapping("/printer/product/status")
    public PrinterStatus productStatus(@RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN"){
            printer.connectWithVirtualPort();
        }
        return new PrinterStatus(1,printer.getLatestMeasurements().toString());
    }

    @GetMapping("/printer/stop")
    public PrinterStatus stopPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PRINTING"){
            printer.cancelPrinting();
        }
        return new PrinterStatus(counter.incrementAndGet(), String.format(printer.getPrinterCurrentState()));
    }
    @GetMapping("/printer/pause")
    public PrinterStatus pausePrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PRINTING"){
            printer.pausePrinting();
        }
        return new PrinterStatus(counter.incrementAndGet(), String.format(printer.getPrinterCurrentState()));
    }
    @GetMapping("/printer/resume")
    public PrinterStatus resumPrinting(@RequestParam(value = "port", defaultValue = "") String port) {

        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "PAUSED"){
            printer.resumePrinting();
        }
        return new PrinterStatus(counter.incrementAndGet(), String.format(printer.getPrinterCurrentState()));
    }

    @GetMapping("/printer/print")
    public Status sendSelectedProduct(@RequestParam(value = "product", defaultValue = "") String selectedProduct,
                                      @RequestParam(value = "port", defaultValue = "") String port) {
        printer = getPrinter(port);
        if (printer.getPrinterCurrentState() == "UNKNOWN"){
            printer.connectWithVirtualPort();
        }

        // select the printer, printer id and the development id
        String status = "";
        System.out.println("model:"+selectedProduct);
        System.out.println(printer.isPrinterConnected());
        if (selectedProduct != null){
            printer.transferFileToPrinter(selectedProduct);
            printer.printModel(selectedProduct);
        //printer.printModel("palm-coin_02mm_pla_mk3s_36m.gcode");
            status = printer.getPrinterCurrentState();
        }
        return new Status(status);
    }
}