package com.dfine.ahoecherl.simmlibrestapi.crif;

import com.acadiasoft.im.base.fx.FXconverter;
import com.acadiasoft.im.base.fx.FxRate;
import com.acadiasoft.im.base.fx.NoConversionFxRate;
import com.acadiasoft.im.base.imtree.ImTree;
import com.acadiasoft.im.simm.engine.Simm;
import com.acadiasoft.im.simm.model.utils.SimmCalculationType;
import com.acadiasoft.im.simmple.engine.Simmple;
import com.acadiasoft.im.simmple.model.Crif;
import com.acadiasoft.im.simmple.model.ImRole;
import com.acadiasoft.im.simmple.model.result.ImTreeResult;
import com.dfine.ahoecherl.simmlibrestapi.fxConverter.FxConverterService;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import javafx.util.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.acadiasoft.im.simmple.model.utils.CrifUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;

@Service
public class CrifService {

    @Autowired
    private FxConverterService fxConverterService;

    public SortedMap<Integer, List<Crif>> getCrifs() {
        return crifs;
    }

    private SortedMap<Integer, List<Crif>> crifs = new TreeMap<>();

    public List<Crif> getCrif (Integer i){return crifs.get(i);}

    public Integer addCrif(List<Crif> crif){
        Integer newKey;
        if (crifs.isEmpty()){
            newKey = 0;
        }
        else {
            newKey = crifs.lastKey()+1;
        }
        crifs.put(newKey, crif);
        return newKey;
    }

    public void deleteCrif(Integer key){crifs.remove(key);}

    public Integer addCrifLine(Crif crif){
        List<Crif> crifList = new ArrayList<>();
        crifList.add(crif);
        crifs.put(1, crifList);
        return 1;
    }

    public ImTreeResult calculate(Integer key, String imRoleString, String calculationCurrency, String resultCurrency){
        return calculate(key, new NoConversionFxRate(), imRoleString, calculationCurrency, resultCurrency);
    }

    public ImTreeResult calculate(Integer key, String fxConversionDate, String imRoleString, String calculationCurrency, String resultCurrency) {

        FxRate fxConverter = new FXconverter(fxConverterService.getFxConverter(fxConversionDate));
        return calculate(key, fxConverter, imRoleString, calculationCurrency, resultCurrency);
    }

    public ImTreeResult calculate(Integer key, FxRate fxConverter, String imRoleString, String calculationCurrency, String resultCurrency){
        ImRole imRole;

        switch(imRoleString){
            case "SECURED":
                imRole = ImRole.SECURED;
                break;
            case "PLEDGOR":
                imRole = ImRole.PLEDGOR;
                break;
            default:
                imRole = ImRole.SECURED;
        }

        ImTreeResult tree = Simmple.calculateWorstOf(crifs.get(key), calculationCurrency, fxConverter, resultCurrency, imRole, SimmCalculationType.TOTAL);
        return tree;

    }

    public List<Crif> getBumpedCrif (Integer i, String tradeId, double epsilon){
        List<Crif> originalCrif = getCrif(i);
        List<Crif> newCrif = CrifUtils.bumpCrif(originalCrif, tradeId, epsilon);
        return newCrif;
    }

    public ImTreeResult bumpedCalculate(Integer key, String imRoleString, String calculationCurrency, String resultCurrency, String tradeId, double epsilon){
        return bumpedCalculate(key, new NoConversionFxRate(), imRoleString, calculationCurrency, resultCurrency, tradeId, epsilon);
    }

    public ImTreeResult bumpedCalculate(Integer key, String fxConversionDate, String imRoleString, String calculationCurrency, String resultCurrency, String tradeId, double epsilon) {
        FxRate fxConverter = new FXconverter(fxConverterService.getFxConverter(fxConversionDate));
        return bumpedCalculate(key, fxConverter, imRoleString, calculationCurrency, resultCurrency, tradeId, epsilon);
    }

    public ImTreeResult bumpedCalculate(Integer key, FxRate fxConverter, String imRoleString, String calculationCurrency, String resultCurrency, String tradeId, double epsilon){
        ImRole imRole;

        switch(imRoleString){
            case "SECURED":
                imRole = ImRole.SECURED;
                break;
            case "PLEDGOR":
                imRole = ImRole.PLEDGOR;
                break;
            default:
                imRole = ImRole.SECURED;
        }

        List<Crif> bumpedCrif = getBumpedCrif(key, tradeId, epsilon);

        return Simmple.calculateWorstOf(bumpedCrif, calculationCurrency, fxConverter, resultCurrency, imRole, SimmCalculationType.TOTAL);

    }



}
