package com.dfine.ahoecherl.simmlibrestapi.fxConverter;

import com.acadiasoft.im.base.fx.ExchangeRate;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@RestController
public class FxConverterController {

    @Autowired
    private FxConverterService fxConverterService;

    @ApiOperation(value = "Upload a FX conversion engine for a given date")
    @RequestMapping(method = RequestMethod.POST, value="/fxConverter/")
    public String addFxConverter (@RequestBody List<ExchangeRate> fxConverter,
                                  @ApiParam(value = "yyyy-mm-dd", required = true) @RequestParam String date) {
        return fxConverterService.addFxConverter(fxConverter, date);
    }

    @ApiOperation(value = "Get all exchange rates of the specified date")
    @RequestMapping(method = RequestMethod.GET, value = "/fxConverter/{date}")
    public List<ExchangeRate> getFxConverter(@ApiParam(value = "Date for which the exchange rates are desired. Format: yyyy-mm-dd")
                                             @PathVariable(value = "date") String date){
        return fxConverterService.getFxConverter(date);
    };

}
