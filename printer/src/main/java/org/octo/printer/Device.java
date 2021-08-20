package org.octo.printer;


public class Device {

    public String apiKey = "nicht nyll";
    public String octoprintURL ;
    private static OctoPrintInterface printer = null;

	public void Device() {
	    System.out.println();
        apiKey = "8CBD168330C34283AFDB22D61AB54D04";
        octoprintURL = "http://127.0.0.1:5000";
        printer = new OctoPrintInterface(octoprintURL,apiKey);

        // test codes
        printer.connectWithPortName("/dev/ttyUSB0");
        //printer.moveAxesRelativeToHome(50d , 50d, 0d);
        printer.printModel("cube_l.gcode");
        printer.getlatestJobStatus();
        printer.getLatestMeasurements();
        printer.moveToHome();
        printer.transferFileToPrinter("1leftgripper.gcode");
    }
    public void execute() {
        printer.getLatestMeasurements();
    }
    public void printFile(String fileName) {
        printer.printModel(fileName);
    }
    public Double getBedTemperature() {
        return printer.getBedTemperature();
    }
    public void setBedTemperature(Integer newBedTemp) {
        printer.setBedTemperature(newBedTemp);
    }
    public Double getExtruderTemperature() {
        return printer.getExtruderTemp();
    }
    public void setExtruderTemperature(Integer newExtruderTemp) {
        printer.setExtruderTemperature(newExtruderTemp);
    }
    public Long getEstimatedPrintTime() {
        return printer.getEstimatedPrintTime();
    }
    public Double getEstimatedFilamentUsage() {
        return printer.getEstimatedFilamentUsage();
    }
    public Long getRemainingPrintTime() {
        return printer.getRemainingPrintTime();
    }
    public Double getProgress() {
        return printer.getProgress();
    }
    public String getPrintingModel() {
        return printer.getPrintingModel();
    }
    public String getPrinterState() {
        return printer.getPrinterCurrentState();
    }
    public void setPrinterState(String newState) {
        printer.setPrinterState(newState);
    }
    public void moveToHome() {
        printer.moveToHome();
    }
    public void moveRelativeToHome(Double x, Double y, Double z) throws InterruptedException {
        printer.moveAxesRelativeToHome(x, y, z);
    }
    public void moveRelativeToCurrentPosition(Double x, Double y, Double z) throws InterruptedException {
        printer.moveAxesRelativeToCurrentPosition(x, y, z);
    }
    public void connectWithVirtualPort()
    {
        printer.connectWithVirtualPort();
    }
    public void connectWithPortName(String portName) {
        printer.connectWithPortName(portName);
    }
    public void disconnect() {
        printer.disconnect();
    }
    public void resumePrinting() {
        printer.resumePrinting();
    }
    public void restartPrinting() {
        printer.restartPrinting();
    }
    public void pausePrinting() {
        printer.pausePrinting();
    }
    public void cancelPrinting() {
        printer.cancelPrinting();
    }
    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }
    public void setOctoPrintURL(String baseUrl) {
        this.octoprintURL = baseUrl;
    }

}