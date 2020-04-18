package com.acadiasoft.im.simmple.model.utils;

import com.acadiasoft.im.simmple.model.Crif;

import java.util.List;
import java.util.stream.Collectors;

public class CrifUtils {

    public static List<Crif> bumpCrif(List<Crif> crifs, String tradeId, double epsilon){
        List<Crif> cloned_crifs = crifs.stream().collect(Collectors.toList());
        for (Crif crif:crifs){
            if (crif.getTradeId().equals(tradeId)){
                String newAmount = Double.toString(new Double(crif.getAmount())*(1+epsilon));
                String newAmountUsd = Double.toString(new Double(crif.getAmountUSD())*(1+epsilon));
                cloned_crifs.remove(crif);
                Crif newCrif = new Crif(crif.getTradeId(), crif.getValuationDate(), crif.getEndDate(), crif.getImModel(), crif.getProductClass(), crif.getRiskType(), crif.getQualifier(), crif.getBucket(), crif.getLabel1(), crif.getLabel2(), newAmount, crif.getAmountCurrency(), newAmountUsd, crif.getPostRegulation(), crif.getCollectRegulation());
                cloned_crifs.add(newCrif);
            }
        }
        return cloned_crifs;
    }


}
