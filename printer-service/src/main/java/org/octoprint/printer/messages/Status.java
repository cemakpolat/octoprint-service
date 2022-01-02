package org.octoprint.printer.messages;

/**
 * @author cemakpolat
 */
public class Status {

    private final String status;

    public Status(String status) {
        this.status = status;
    }

    public String getStatus() {
        return status;
    }

}
