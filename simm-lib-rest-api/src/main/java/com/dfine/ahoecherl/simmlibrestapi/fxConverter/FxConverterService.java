package com.dfine.ahoecherl.simmlibrestapi.fxConverter;

import com.acadiasoft.im.base.fx.ExchangeRate;
import com.acadiasoft.im.base.fx.FXconverter;
import com.acadiasoft.im.base.fx.FxRate;
import io.swagger.annotations.Api;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;

@Service
public class FxConverterService {

    private SortedMap<String, FXconverter> fxConverters = new TreeMap<>();

    public String addFxConverter (List<ExchangeRate> fxConverter, String date){
        fxConverters.put(date, new FXconverter(fxConverter));
        return date.toString();
    }

    public List<ExchangeRate> getFxConverter (String date) {
        return fxConverters.get(date).getExchangeRates();
    }

    public void deleteFxConverter (String date){
        fxConverters.remove(date);
    }

}
