# Luna6Algotrader

One of the lambda functions written for the Luna6/Mila3 algotrader project. Luna6 was created with AWS Chalice and hosted on AWS lambda as a self-calling API. 

I created SQL queries to access AWS-RDB-mySQL via a VCN in order to access data on client created algotraders. 
Makes daily http requests to the [alpaca brokerage api](https://alpaca.markets/) and a few other financial data suppliers. 
