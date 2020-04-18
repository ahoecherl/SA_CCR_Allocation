package com.acadiasoft.im.base.fx;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;

public class FXconverter implements FxRate {

    private List<ExchangeRate> exchangeRates;

    public FXconverter(List<ExchangeRate> exchangeRates){
        this.exchangeRates = exchangeRates;
    }

    @Override
    public BigDecimal convert(BigDecimal amount, String from, String to) {
        if (from.equals(to)){
            return amount;
        }
        for (ExchangeRate exchangeRate : this.exchangeRates){
            if (exchangeRate.getPrimaryCurrency().equals(from) && exchangeRate.getQuotingCurrency().equals(to)){
                return new BigDecimal(exchangeRate.getExchangeRate()).multiply(amount);
            }
        }
        throw new NoSuchElementException(String.format("Required exchange rate not found in FXconverter. Primary Currency %s Quotation Currency %s",from, to));
    }

    public List<ExchangeRate> getExchangeRates() {
        return exchangeRates;
    }

}
