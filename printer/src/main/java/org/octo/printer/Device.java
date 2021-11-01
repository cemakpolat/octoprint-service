package org.octo.printer;


public class Device {

    public String apiKey = "nicht nyll";
    public String octoprintURL ;
    private static OctoPrintInterface printer = null;

	public void Device() {

	    System.out.println();
        apiKey = "083C5A02B2A948F1A6D42D1366591CEF";
        octoprintURL = "http://127.0.0.1:5000";
        printer = new OctoPrintInterface(octoprintURL,apiKey);

        // test codes

        //printer.moveAxesRelativeToHome(50d , 50d, 0d);

        printer.printModel("palm-coin_02mm_pla_mk3s_36m.gcode");
        printer.getlatestJobStatus();
        printer.getLatestMeasurements();

        printer.getlatestJobStatus();
        printer.getLatestMeasurements();
        printer.transferFileToPrinter("1leftgripper.gcode");

        System.out.println(printer.getPrinterCurrentState());
        printer.transferFileToPrinter("whistle_02mm_pla_mk3_34m.gcode");
        printer.printModel("palm-coin_02mm_pla_mk3s_36m.gcode");
    }

    public static void main(String[] args) {
        System.out.println();
        String apiKey = "0792B665FF2D44D9A709FE414FBAD68B";
        String octoprintURL = "http://127.0.0.1:5000";
        OctoPrintInterface printer = new OctoPrintInterface(octoprintURL, apiKey);
        printer.connectWithVirtualPort();
        // test codes
        try {
            printer.moveAxesRelativeToHome(50d, 50d, 0d);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        //printer.printModel("palm-coin_02mm_pla_mk3s_36m.gcode");
        printer.getlatestJobStatus();
        printer.getLatestMeasurements();
        //printer.moveToHome();
        //printer.initiate();
        System.out.println(printer.getPrinterCurrentState());
        printer.transferFileToPrinter("whistle_02mm_pla_mk3_34m.gcode");
        printer.printModel("whistle_02mm_pla_mk3_34m.gcode");
    }

}