/*
 * Copyright (c) 2019 AcadiaSoft, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package com.acadiasoft.im.simmple.model;

import java.io.Serializable;
import java.math.BigDecimal;

/**
 *
 * @author alec.stewart
 */
public class Crif implements Serializable {

  private String tradeId;
  private String imModel;
  private String productClass;
  private String riskType;
  private String qualifier;
  private String bucket;
  private String label1;
  private String label2;
  private String amount;
  private String amountCurrency;
  private String amountUSD;
  private String postRegulation;
  private String collectRegulation;
  private String valuationDate;
  private String endDate;
  private String notional;
  private String notionalCurrency;

  /**
   * Builds a line of CRIF data with all fields
   *
   * @param tradeId           the id of the trade that the CRIF line belongs to
   * @param valuationDate     the valuation date of the trade
   * @param endDate           the end date of the trade
   * @param notional          the notional amount of the trade
   * @param notionalCurrency  the currency of the trade notional
   * @param imModel           the model that im will be calculated with for the
   *                          trade
   * @param productClass      the product class of the trade (either SIMM:
   *                          [RatesFX, Credit, Commdity, Equity] or Schedule:
   *                          [Rates, FX, Credit, Commodity, Equity]
   * @param riskType          the risk type of the CRIF line as defined by the
   *                          Common Risk Interchange Format
   * @param qualifier         the qualifier " . . . "
   * @param bucket            the bucket " . . . "
   * @param label1            the label1 " . . . "
   * @param label2            the label2 " . . . "
   * @param amount            the amount " . . . "
   * @param amountCurrency    the currency of the amount
   * @param amountUSD         the amount in USD
   * @param postRegulation    the regulator of the posting party (usually this is
   *                          yourself)
   * @param collectRegulation the regulator of the collecting party (usually this
   *                          is a counter-party)
   */

  public Crif(String tradeId, String valuationDate, String endDate, String notional, String notionalCurrency,
      String imModel, String productClass, String riskType, String qualifier, String bucket, String label1,
      String label2, String amount, String amountCurrency, String amountUSD, String postRegulation,
      String collectRegulation) {
    this.valuationDate = valuationDate;
    this.endDate = endDate;
    this.tradeId = tradeId;
    this.imModel = imModel;
    this.productClass = productClass;
    this.riskType = riskType;
    this.qualifier = qualifier;
    this.bucket = bucket;
    this.label1 = label1;
    this.label2 = label2;
    this.amount = amount;
    this.amountCurrency = amountCurrency;
    this.amountUSD = amountUSD;
    this.postRegulation = postRegulation;
    this.collectRegulation = collectRegulation;
    this.notional = notional;
    this.notionalCurrency = notionalCurrency;
  }

  public Crif(String tradeId, String valuationDate, String endDate, String imModel, String productClass,
      String riskType, String qualifier, String bucket, String label1, String label2, String amount,
      String amountCurrency, String amountUSD, String postRegulation, String collectRegulation) {
    this(tradeId, valuationDate, endDate, "", "", imModel, productClass, riskType, qualifier, bucket, label1, label2,
        amount, amountCurrency, amountUSD, postRegulation, collectRegulation);
  }


  public Crif(){

  }

  public String getValuationDate() {
    return valuationDate;
  }

  public String getEndDate() {
    return endDate;
  }

  public String getTradeId() {
    return tradeId;
  }

  public String getImModel() {
    return imModel;
  }

  public String getProductClass() {
    return productClass;
  }

  public String getRiskType() {
    return riskType;
  }

  public String getQualifier() {
    return qualifier;
  }

  public String getBucket() {
    return bucket;
  }

  public String getLabel1() {
    return label1;
  }

  public String getLabel2() {
    return label2;
  }

  public String getAmount() {
    return amount;
  }

  public String getAmountCurrency() {
    return amountCurrency;
  }

  public String getAmountUSD() {
    return amountUSD;
  }

  public String getPostRegulation() {
    return postRegulation;
  }

  public String getCollectRegulation() {
    return collectRegulation;
  }

  public String getNotionalString() {
    return notional;
  }

  public String getNotional() {
    return notional;
  }

  public String getNotionalCurrency() {
    return notionalCurrency;
  }

  public String toTestString() {
    return "\"" + valuationDate + "\", \"" + endDate + "\", \"" + tradeId + "\", \"" + imModel + "\", \"" + productClass
        + "\", \"" + riskType + "\", \"" + qualifier + "\", \"" + bucket + "\", \"" + label1 + "\", \"" + label2
        + "\", \"" + amount + "\", \"" + amountCurrency + "\", \"" + amountUSD + "\", \"" + postRegulation + "\", \""
        + collectRegulation + "\", \"" + notional + "\", \"" + notionalCurrency + "\"";
  }

}
