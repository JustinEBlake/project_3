-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/ixr1TV
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "company" (
    "company_symbol" Varchar(255)   NOT NULL,
    "company_name" Varchar(255)   NOT NULL,
    CONSTRAINT "pk_company" PRIMARY KEY (
        "company_symbol"
     )
);

CREATE TABLE "stocks" (
    "company_symbol" Varchar(255)   NOT NULL,
    "date" Date   NOT NULL,
    "open" Numeric   NOT NULL,
    "high" Numeric   NOT NULL,
    "low" Numeric   NOT NULL,
    "close" Numeric   NOT NULL,
    "adj_Close" Numeric   NOT NULL,
    "volume" Numeric   NOT NULL
);

CREATE TABLE "balance_sheet" (
    "company_symbol" Varchar(255)   NOT NULL,
    "date" Date   NOT NULL,
    "total_debt" Numeric   NOT NULL,
    "shares_issued" Numeric   NOT NULL
);

CREATE TABLE "financial_statement" (
    "company_symbol" Varchar(255)   NOT NULL,
    "date" Date   NOT NULL,
    "total_revenue" Numeric   NOT NULL,
    "gross_profit" Numeric   NOT NULL,
    "total_expenses" Numeric   NOT NULL,
    "net_income" Numeric   NOT NULL
);

ALTER TABLE "stocks" ADD CONSTRAINT "fk_stocks_company_symbol" FOREIGN KEY("company_symbol")
REFERENCES "company" ("company_symbol");

ALTER TABLE "balance_sheet" ADD CONSTRAINT "fk_balance_sheet_company_symbol" FOREIGN KEY("company_symbol")
REFERENCES "company" ("company_symbol");

ALTER TABLE "financial_statement" ADD CONSTRAINT "fk_financial_statement_company_symbol" FOREIGN KEY("company_symbol")
REFERENCES "company" ("company_symbol");

