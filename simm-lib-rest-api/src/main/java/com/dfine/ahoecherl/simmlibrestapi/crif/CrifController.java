package com.dfine.ahoecherl.simmlibrestapi.crif;

import com.acadiasoft.im.simmple.model.Crif;
import com.acadiasoft.im.simmple.model.result.ImTreeResult;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.SortedMap;

@RestController
public class CrifController {

    @Autowired
    private CrifService crifService;

    @ApiOperation(value = "Get all CRIFs as JSON")
    @RequestMapping(method = RequestMethod.GET, value = "/crifs")
    public SortedMap<Integer, List<Crif>> getCrifs(){return crifService.getCrifs();}

    @ApiOperation(value = "Receive CRIF of given id as JSON")
    @RequestMapping(method = RequestMethod.GET, value ="/crifs/{id}")
    public List<Crif> getCrif(@PathVariable Integer id){return crifService.getCrif(id);}

    @ApiOperation(value = "Upload a new CRIF as JSON receive id under which it has been stored")
    @RequestMapping(method = RequestMethod.POST,value="/crifs")
    public Integer addCrif(@RequestBody List<Crif> crif) {return crifService.addCrif(crif);}

    @ApiOperation(value = "Calculate the initial margin using the Fx Converter of a given valuation date")
    @RequestMapping(method = RequestMethod.GET, value = "/crifs/{id}/calculate")
    public double calculateIM (@ApiParam(value = "id of the CRIF that should be used for calculation", required = true)
                               @PathVariable(value = "id") Integer id,
                               @ApiParam(value = "Should calculation be performed as Pledgor or Secured role. In Pledgor role, all amounts in CRIF are negated as a first step. ", allowableValues = "SECURED, PLEDGOR",required = true, defaultValue = "SECURED")
                               @RequestParam String imRole,
                               @ApiParam(value = "Calculation currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
                               @RequestParam String calculationCurrency,
                               @ApiParam(value = "Result Currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
                               @RequestParam String resultCurrency,
                               @ApiParam(value = "Valuation date used to load the matching FX Converter. If no valuation date is provided or no FX Converter has been uploaded for the given valuation date an empty FX Converter is created.", required = false)
                               @RequestParam Optional<String> fxConversionDate){
        ImTreeResult tree;
        if (fxConversionDate.isPresent()){
            tree = crifService.calculate(id, fxConversionDate.get(), imRole, calculationCurrency, resultCurrency);
        }
        else{
            tree = crifService.calculate(id,imRole,calculationCurrency, resultCurrency);
        }
        return tree.getImTree().getMargin().doubleValue();
    }

    @ApiOperation(value = "Calculate and return the initial margin tree using the Fx Converter of a given valuation date")
    @RequestMapping(method = RequestMethod.GET, value = "/crifs/{id}/calculateTree")
    public String calculateIMtree (@ApiParam(value = "id of the CRIF that should be used for calculation", required = true)
                               @PathVariable(value = "id") Integer id,
                               @ApiParam(value = "Should calculation be performed as Pledgor or Secured role. In Pledgor role, all amounts in CRIF are negated as a first step. ", allowableValues = "SECURED, PLEDGOR",required = true, defaultValue = "SECURED")
                               @RequestParam String imRole,
                               @ApiParam(value = "Calculation currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
                               @RequestParam String calculationCurrency,
                               @ApiParam(value = "Result Currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
                               @RequestParam String resultCurrency,
                               @ApiParam(value = "Valuation date used to load the matching FX Converter. If no valuation date is provided or no FX Converter has been uploaded for the given valuation date an empty FX Converter is created.", required = false)
                               @RequestParam Optional<String> fxConversionDate){
        ImTreeResult tree;
        if (fxConversionDate.isPresent()){
            tree = crifService.calculate(id, fxConversionDate.get(), imRole, calculationCurrency, resultCurrency);
        }
        else{
            tree = crifService.calculate(id,imRole,calculationCurrency, resultCurrency);
        }

        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        String json = gson.toJson(tree);
        return json;

    }

    @ApiOperation(value = "Upload CRIF as a csv. Not working yet.")
    @RequestMapping(value="/csvcrif", method=RequestMethod.POST)
    public Integer addCrif_as_csv(
            @ApiParam(value = "CRIF csv file. Format reference found in ISDA-SIMM risk data standard.")
            @RequestParam MultipartFile file,
            @ApiParam(allowableValues = "tab, comma, semicolon")
            @RequestParam String delimiter) throws IOException {
        // process your
        return 0;
    }

    //@RequestMapping(method = RequestMethod.POST,value="/crifs")
    //public Integer addCrifLine(@RequestBody Crif crif) {return crifService.addCrifLine(crif);}

    @ApiOperation(value = "Delete the CRIF saved under a given id")
    @RequestMapping(method = RequestMethod.DELETE, value="/crifs/{id}")
    public void deleteCrif(
            @ApiParam(value = "CRIF Id from which Crif object will be deleted from storage", required = true)
            @PathVariable(value = "id") Integer id) {
        crifService.deleteCrif(id);
    }

    @ApiOperation(value = "Bump all crif entries related to a specific trade by multiplying them with (1+epsilon)")
    @RequestMapping(method = RequestMethod.GET, value="/crifs/{id}/bump/{tradeId}")
    public List<Crif> bumpCrif(
            @ApiParam(value = "CRIF id", required = true)
            @PathVariable(value = "id") Integer id,
            @ApiParam(value = "trade Id of the trade that should be bumped", required = true)
            @PathVariable(value = "tradeId") String tradeId,
            @ApiParam(value = "Epsilon used for a relative bump of sensitivities, notional etc by 1+epsilon", defaultValue = "0.0001")
            @RequestParam double epsilon) {
        return crifService.getBumpedCrif(id, tradeId, epsilon);
    }

    @ApiOperation(value = "Calculate and return Initial margin of bumped Crif")
    @RequestMapping(method = RequestMethod.GET, value ="/crifs/{id}/bump/{tradeId}/calculate")
    public double calculateBumpedCrif(
            @ApiParam(value = "CRIF id", required = true)
            @PathVariable(value = "id") Integer id,
            @ApiParam(value = "trade Id of the trade that should be bumped", required = true)
            @PathVariable(value = "tradeId") String tradeId,
            @ApiParam(value = "Epsilon used for a relative bump of sensitivities, notional etc by 1+epsilon", defaultValue = "0.0001")
            @RequestParam double epsilon,
            @ApiParam(value = "Should calculation be performed as Pledgor or Secured role. In Pledgor role, all amounts in CRIF are negated as a first step. ", allowableValues = "SECURED, PLEDGOR",required = true, defaultValue = "SECURED")
            @RequestParam String imRole,
            @ApiParam(value = "Calculation currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
            @RequestParam String calculationCurrency,
            @ApiParam(value = "Result Currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
            @RequestParam String resultCurrency,
            @ApiParam(value = "Valuation date used to load the matching FX Converter. If no valuation date is provided or no FX Converter has been uploaded for the given valuation date an empty FX Converter is created.", required = false)
            @RequestParam Optional<String> fxConversionDate){
        ImTreeResult tree;
        if (fxConversionDate.isPresent()){
            tree = crifService.bumpedCalculate(id, fxConversionDate.get(), imRole, calculationCurrency, resultCurrency, tradeId, epsilon);
        }
        else{
            tree = crifService.bumpedCalculate(id,imRole,calculationCurrency, resultCurrency, tradeId, epsilon);
        }
        return tree.getImTree().getMargin().doubleValue();
    }

    @ApiOperation(value = "Calculate and return Initial margin of bumped Crif")
    @RequestMapping(method = RequestMethod.GET, value ="/crifs/{id}/bump/{tradeId}/calculateTree")
    public String calculateTreeBumpedCrif(
            @ApiParam(value = "CRIF id", required = true)
            @PathVariable(value = "id") Integer id,
            @ApiParam(value = "trade Id of the trade that should be bumped", required = true)
            @PathVariable(value = "tradeId") String tradeId,
            @ApiParam(value = "Epsilon used for a relative bump of sensitivities, notional etc by 1+epsilon", defaultValue = "0.0001")
            @RequestParam double epsilon,
            @ApiParam(value = "Should calculation be performed as Pledgor or Secured role. In Pledgor role, all amounts in CRIF are negated as a first step. ", allowableValues = "SECURED, PLEDGOR",required = true, defaultValue = "SECURED")
            @RequestParam String imRole,
            @ApiParam(value = "Calculation currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
            @RequestParam String calculationCurrency,
            @ApiParam(value = "Result Currency used - refer to Risk Data Standard for significance. Has to be three letter ISO code for currency", required = true, defaultValue = "USD")
            @RequestParam String resultCurrency,
            @ApiParam(value = "Valuation date used to load the matching FX Converter. If no valuation date is provided or no FX Converter has been uploaded for the given valuation date an empty FX Converter is created.", required = false)
            @RequestParam Optional<String> fxConversionDate){
        ImTreeResult tree;
        if (fxConversionDate.isPresent()){
            tree = crifService.bumpedCalculate(id, fxConversionDate.get(), imRole, calculationCurrency, resultCurrency, tradeId, epsilon);
        }
        else{
            tree = crifService.bumpedCalculate(id,imRole,calculationCurrency, resultCurrency, tradeId, epsilon);
        }
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        String json = gson.toJson(tree);
        return json;
    }

}
