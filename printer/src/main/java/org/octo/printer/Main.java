package org.octo.printer;


public class Main {

    public String apiKey;
    public String printerURL;
    private static OctoPrintInterface printer = null;

    public static void main(String[] args){

        String apiKey;
        String octoprintURL;
        apiKey = "8CBD168330C34283AFDB22D61AB54D04";
        octoprintURL = "http://localhost:5000";
        Device device = new Device();
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
    }

}
