# FTSE-Pricing-Engines

## Folders needed to run engine 2.4.x
* clock_log
* Data
* DataStat
* Error_Logs
* Stat_Filtered_Data_Holding
* Credentials
* DataBaseCurrency
* Error_Files
* Raw_Data_Holding
* test
* DAR_S3_Upload_Holding
* DataPersist
* Error_logs
* Stable_Data
* Vwap



## Functionality Description
### Slack_FTSE_Alert_message
* Send an alert message to Slack (ftse-alert channel)

### get_sql_data
* Reads sql data using necessary credentials from DAX (where trades from kubes system is being collected)

### get_all_data(start_stamp, end_stamp, save_directory)
* Gets trade data from SpotTrade (from start_stamp to end_stamp)
* Gets exchange name and token name
* Saves the trades in save_directory with the name Trade_<start_stamp>
* Execution time is clocked.

### base_currency(start_stamp, end_stamp)
* Gets trade data from the file stored in <i>DataBaseCurrency/df_base_data.csv </i>
* This trade data has 1hr 15 secs worth of data. (Recently(Oct 29, 2020) changed it to less than an hour to reduce processing time)
* Processing for stable coins
  * Gets volume weighted average price for each exchange pair. This gives the Tether price 
  * Saves this output to <i>DataBaseCurrency/df_stable_persist.csv </i>
  * Filters out row based on the acceptable pairs and exchange (drops Bitfinex specifically)
  * Vwap it to get the tether price for all exchange with Source = 'ALL'
* Processing for base coins
  * Gets the vwap for pairs with usd/usdt as currency and with base coin of all exchanges
  * The weighted price for usdt pairs is replaced with the previously calculated one
  * A global average is also calculated using the data from above which is independent of source (Source = 'ALL').
* Finally stable coin and base coin are merged into df_master.
* Processing for other currencies
  * The exchange rates for fiat currencies ['KRW', 'JPY', 'CNY', 'EUR', 'GBP'] from 20 mins from the start_stamp is collected from Exchange_Rates db.
  * The exchange rate data is aggregated wrt currency and source and stored in <i>DataBaseCurrency/df_fiat_persist.csv </i>
* Finally, exchange rates data is also merged with the df_master.
* Execution time is clocked.

### stamp_to_directory(tstamp)
* Converts tstamp to year/month/day format

### DAR_asset_conversion(df)
* Converts the asset names to corresponding tickers.

### DAR_name_filter(df)
* Corrects the bad names of some of the assets

### get_rates(df_stat)
* Gets exchange rates for each token.
* First it gets the base currency (conversion_df) from base_currency function.
* Also acquires prev conversion rates (conversion_df_prev).
* Now the conversion_df is checked to see if anything is missing. If it is, then the value will be adapted from the conversion_df_prev.
* Final data will be saved in <i> conversion_df.csv </i>
* standardize(df_standard) is then called on data. It calls yet another function Vector_pandas_currency_apply(df_vector) to parse and get the currency of each pair. Finally standardize function removes all pairs which do not have a valid currency and prints them on console
* For all the sources which have conversion rate for eth/btc is present in conversion_df, they are set as Rate to corresponding df_stat (df) data. For sources which do not have eth/btc conversion rate in conversion_df, the global conversion is set.
* For rest of the currencies, the conversion rate is set for df.
* The output is saved to <i> test.csv </i>

### find_currency(Pair, Token_ID) (Flawed and should not be used)
* Parses the pair and return the currency

### pandas_currency_apply(x) 
* Function which helps apply with pandas to get the corresponding currency.

### filter_stdv_ticker_agnostic_exchange_filter(df_raw, filter_sigma, start_stamp)
* Gets the previous file with filtered std deviation (df_stat)
* Gets the conversion rate for df_raw (The data that is to be processed).
* Filtering out rows with converted_price > 1.5 stddev
  * Data is grouped wrt Excange and token to calculate mean converted price(df_raw_by_exchange).
  * Then again grouped based on only TokenID to get converted price std and converted price mean (df_raw_by_exchange_stdv)
  * df_raw_by_exchange is joined with df_raw_by_exchange_std. Now df_raw_by_exchange will have Exchange token pairs with currency std dev based on Token_Id.
  * Sigma of converted price std dev is calculated and all the rows with sigma greater than 1.5 is considered as the filter_out_list.
  * Using the filtered_out_list (which has the exchange token pair whose std dev is greater than 1.5 sigma) all the data that has to be filtered out from df_raw is collected into df_filtered_out.
  * df_raw is updated with rest of the data.
* Calculation of weighted avg and std calculation
  * df_stat is used for this.
  * Vwap of converted price is calculated (wavg_calc).
  * For std dev, df_stat is grouped by TokenId and converted_price and aggregated total_size (stdev_calc).
  * wavg_calc is joined to stdev_calc.
  * Stddev is calculated using ((converted_price - vwap_price)^2) * Trade_Size. Converted Price in stddev_calc, vwap_price is the weighted_price from wavg_calc and Trade_size is the aggregated trade size from stdev_calc.
  * stddev_calc is grouped by token_id aggregating stdev(sum), trade_size(sum), weighted_price(mean) and non_weighted_price(mean)
  * Weighted stdev is calculated by formula sqrt(stdev/trade_size)
* The weighted stdev and weighted price is merged with df_raw and filtered with rows having std dev less than filter_sigma.
* df_stat is appended with the df_raw and the data within that from 10 mins before is saved to <i>DataStat/Price_Stat.csv</i>
* Finally all the data which was filtered by weighted stdev is returned
  
### Misc
* The SQL connection is being pooled to reduce disruption by connection failure.

## Workflow
* Starts from main
* The data this engine reports will have a lag of start_look_back_time (120s). So the start time stamp will be 135s behind and end time stamp be 120s behind for each cycle.
* Engine starts exactly at 0s of a minute
* It needs <i>DataPersist/Price_Persist</i> to start. If not present it will create all necessary files before it starts.
* Calls get_all_data function and gets 15 seconds data (df_list).
* df_list is filtered to only ftse exchanges and tokens.
* Base data (df_base_data) 1800s of data in <i>DataBaseCurrency/df_base_data.csv</i> is appended with current data (df_list). It is then again filtered to prev 1800s and stored back to same place.
* filter_stdv_ticker_agnostic_exchange_filter funtion is used on df_list and its output(df_final) is stored in Stat_Filtered_Data_Holding/<end_timestamp>.
* Vwap is calculated using df_final and the Dar_asset_conversion is used to get the tickers.
* df_final is checked for 0 prices and replaces them with the price in df_persist.
* df_persist is then updated with new vwap prices in df_final. If there are new tokens in current scraping, they are updated as well.
* df_final is marked with vetted and non vetted exchanges and tokens (df_prod). 
* df_prod is then saved to Vwap/DAR_PRICE_FILE_PROD_<end_timestamp>
* Then, these price files are uploaded to FTSE buckets. df_persist is uploaded to bucket ftse-da-dev-indexdata-ew1 and df_prod is uploaded to ftse-da-prod-indexdata-ew1.
* All data in df_persist is flagged to 1 (sign to say the prices are old) and uploaded back again to <i>DataPersist/<end_Timestamp>_Price_Persist.csv</i>.
* Clock log is uploaded to <i>clock_log/</i>.
* Sleeps until next time snap and starts the cycle again.
