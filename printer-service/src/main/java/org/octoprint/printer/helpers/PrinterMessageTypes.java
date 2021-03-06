package org.octoprint.printer.helpers;

/**
 * @author cemakpolat
 */
public
class PrinterMessageTypes {
    public static final String action_changePrinterState = "ChangePrinterState";
    public static final String action_setBedExtruderTemp = "BedExtruderTemperature";
    public static final String action_setAxes = "XYZAxes";
    public static final String action_changeModelToBePrinted = "change3DModel";

    public static final String status = "status";
    public static final String bedTemperature = "bedTemperature";
    public static final String extruderTemperature = "extruderTemperature";
    public static final String estimatedPrintTime = "estimatedPrintTime";
    public static final String estimatedFilamentUsage = "estimatedFilamentUsage";
    public static final String remainingPrintTime = "remainingPrintTime";
    public static final String progress = "progress";
}
