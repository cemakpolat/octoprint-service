package org.octoprint.printer.models;

/**
 * @author cemakpolat
 */

public class PrinterStatus {

    private final long id;
    private final String content;

    public PrinterStatus(long id, String content) {
        this.id = id;
        this.content = content;
    }

    public long getId() {
        return id;
    }

    public String getContent() {
        return content;
    }
}