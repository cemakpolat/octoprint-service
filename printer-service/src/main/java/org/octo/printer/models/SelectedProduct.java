package org.octo.printer.models;

/**
 * @author cemakpolat
 */

public class SelectedProduct {

    private final long productId;
    private final String productName;

    public SelectedProduct(long productId, String productName) {
        this.productId = productId;
        this.productName= productName;
    }

    public long getProductId() {
        return productId;
    }

    public String getProductName() {
        return productName;
    }
}