package com.acadiasoft.im.base.fx;

public class ExchangeRate {

    private String primaryCurrency;
    private String quotingCurrency;
    private double exchangeRate;

    public ExchangeRate(){

    }

    public String getPrimaryCurrency() {
        return primaryCurrency;
    }

    public void setPrimaryCurrency(String primaryCurrency) {
        this.primaryCurrency = primaryCurrency;
    }

    public String getQuotingCurrency() {
        return quotingCurrency;
    }

    public void setQuotingCurrency(String quotingCurrency) {
        this.quotingCurrency = quotingCurrency;
    }

    public double getExchangeRate() {
        return exchangeRate;
    }

    public void setExchangeRate(double exchangeRate) {
        this.exchangeRate = exchangeRate;
    }
}
