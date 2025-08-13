fields = {
    "titlemso": {
        "deal_number": "<Unique internal transaction number, often labeled as 'INVOICE NO.', 'DEAL #', or found near the invoice date at the top of the document.>",
        "stock_number": "<Internal dealership reference, may appear as 'STOCK NO.' or be embedded in dealer forms. Not always available in Lexus invoices.>",
        "vin": "<17-character Vehicle Identification Number, found under labels like 'VEHICLE IDENTIFICATION NO.', 'VIN', or 'SERIAL NO.'.>",
        "year": "<Model year of the vehicle. Typically appears above or beside the make/model and VIN, often as a 4-digit number.>",
        "make": "<Vehicle brand or manufacturer (e.g., Lexus, Toyota). Usually located near the model or VIN.>",
        "model": "<Model name (e.g., RX 350h). May appear beside 'SERIES OR MODEL' or 'DESCRIPTION'.>",
        "odometer_reading": "<Odometer reading at time of sale. Shown with terms like 'ODOMETER READING', 'ACTUAL MILEAGE', or simply 'MI'.>",
        "buyer_name": "<Full name of the purchaser. Often found below a label like 'REGISTERED OWNER(S)' or filled in signature areas.>",
        "co_buyer_name": "<Additional buyer if applicable. May be found near the buyer or as a second listed name (e.g., 'LSR', 'LSE', or 'AND').>",
        "buyer_address": "<Full address of the buyer. Usually found below the buyer’s name in blocks like 'REGISTERED OWNER(S)' or 'SOLD TO'.>",
        "sale_price": "<Total selling price before taxes or fees. Might appear near labels like 'SALE PRICE', 'SELLING PRICE', or within a breakdown table.>",
        "tavt_tax_amount": "<TAVT (Title Ad Valorem Tax) or sales tax. May appear as 'TAX', 'TAVT', or in a financial breakdown.>",
        "trade_in_value": "<Credit amount given for a trade-in vehicle. Look for 'TRADE IN VALUE' or similar terms in financing sections.>",
        "total_amount_due": "<Final amount payable. Found under labels such as 'TOTAL DUE', 'AMOUNT DUE', or at the end of fee breakdowns.>",
        "lien_holder_name": "<Bank or financial institution listed as lienholder. Frequently appears under 'LIENHOLDER(S)' or in finance sections.>",
        "dealer_fees": "<Additional dealership charges such as 'DOC FEE', 'PROCESSING FEE', 'ELECTRONIC FILING', or grouped under 'FEES'.>"
    },
    "bill_of_sale": {
        "deal_number": "<Unique internal transaction number, often labeled as 'INVOICE NO.', 'DEAL #', or found near the invoice date at the top of the document.>",
        "stock_number": "<Internal dealership reference, may appear as 'STOCK NO.' or be embedded in dealer forms.>",
        "vin": "<17-character Vehicle Identification Number, found under labels like 'VIN NO.', 'VIN', or 'VEHICLE ID'.>",
        "year": "<Model year of the vehicle. Usually appears near make/model/VIN.>",
        "make": "<Vehicle manufacturer, such as 'LEXUS', 'TOYOTA'.>",
        "model": "<Vehicle model, e.g., 'RX 350h PREMIUM'.>",
        "odometer_reading": "<Odometer reading at sale time, often shown with 'ODO', 'Miles', or 'MI'.>",
        "buyer_name": "<Name of the main purchaser.>",
        "co_buyer_name": "<Name of any co-buyer or cosigner.>",
        "buyer_address": "<Full address including street, city, state, and zip.>",
        "sale_price": "<Total base sale price before taxes or fees.>",
        "tavt_tax_amount": "<Title Ad Valorem Tax or applicable sales tax.>",
        "trade_in_value": "<Value of trade-in vehicle credited in the transaction.>",
        "total_amount_due": "<Final payable amount after deductions and additions.>",
        "lien_holder_name": "<Name of the lienholder or financing institution.>",
        "dealer_fees": "<Any dealer-specific fees such as doc or processing fees.>"
    },
    "driver_license": {
        "full_name": "<Full name of the license holder. Often labeled as 'Name' or 'Driver Name'.>",
        "date_of_birth": "<Date of birth of the individual. Look for labels like 'DOB' or 'Birth Date'.>",
        "address": "<Street address (not including city/state/zip). Found under 'Address', 'Street Address', or similar.>",
        "city": "<City portion of the license holder's address.>",
        "state": "<State abbreviation or full name. Often paired with city or ZIP.>",
        "zip": "<ZIP or postal code. Usually numeric and near the state.>",
        "driver_s_license_number": "<Unique driver license number. Labels may include 'DLN', 'License No.', or 'License #'.>",
        "expiration_date": "<Expiration date of the license. Labeled as 'EXP', 'Exp Date', or 'Expiration Date'.>"
    },
    "red_reassignment": {
        "vin": "<17-character Vehicle Identification Number. Labels include 'VIN', 'VIN #', or 'Vehicle ID'.>",
        "year": "<Model year of the vehicle, typically a 4-digit number.>",
        "make": "<Vehicle manufacturer (e.g., LEXUS, TOYOTA).>",
        "model": "<Vehicle model (e.g., RX 350h).>",
        "odometer_reading": "<Odometer mileage at reassignment. May be labeled as 'Miles' or 'Mileage'.>",
        "odometer_type": "<Odometer status such as 'ACTUAL', 'EXCEEDS', 'NOT ACTUAL', or 'Mileage Type'.>",
        "buyer_name": "<Name of the buyer or new owner.>",
        "buyer_address": "<Address of the buyer. Includes street-level details.>",
        "date_of_reassignment": "<Date when title was reassigned to a new owner.>",
        "signatures": "<List or string containing seller and buyer signatures.>"
    },
    "mv-1": {
        "buyer_full_name": "<Full name of the buyer. Often appears as 'Buyer', 'Purchaser', or 'Owner Name'.>",
        "co_buyer_name": "<Name of any co-buyer. Look for 'Co-Buyer' or 'Co-Purchaser'.>",
        "buyer_address": "<Residential address of the buyer. May appear under 'Address', 'Residence', or 'Street Address'.>",
        "city": "<City portion of the buyer’s address.>",
        "state": "<State code or name from buyer's address.>",
        "zip": "<Postal or ZIP code. May be labeled 'Zip Code' or 'Postal Code'.>",
        "county_of_residence": "<County where the buyer resides. May follow address or appear separately.>",
        "customer_id": "<Customer identifier such as 'DL#', 'Driver's License Number', or 'DLN'.>",
        "vin": "<Vehicle Identification Number. Look for 'VIN', 'VIN#', or 'Vehicle ID Number'.>",
        "year": "<Vehicle’s model year. Sometimes labeled as 'YR'.>",
        "make": "<Vehicle make. Appears as 'Vehicle Make'.>",
        "model": "<Vehicle model. Look for 'Vehicle Model'.>",
        "body_style": "<Vehicle’s body style or type. May appear as 'Body Type'.>",
        "odometer_reading": "<Vehicle mileage at sale. Look for 'ODO' or 'Mileage'.>",
        "lien_holder_name": "<Name of the lienholder or lender. Also seen as 'Lender Name'.>",
        "lien_holder_address": "<Address of the lienholder. May be called 'Lender Address' or 'Secured Party Address'.>",
        "dealer_name": "<Name of the dealership selling the vehicle.>",
        "dealer_number": "<Dealer identifier, license number. Look for 'Dealer ID' or 'License #'.>",
        "sale_price": "<Final sale amount before taxes/fees. Look for 'Purchase Price' or 'Selling Price'.>"
    },
    "mv-7d": {
        "vin": "<Vehicle Identification Number. Look for 'VIN', 'Vehicle ID', or 'VIN #'.>",
        "year": "<Vehicle model year. May be part of 'YM/M', 'YMM', or 'YR/MAKE/MODEL'.>",
        "make": "<Vehicle make. Often grouped with year and model under 'Vehicle Info'.>",
        "model": "<Vehicle model name. Look near 'Vehicle Info', 'YMM'.>",
        "odometer_reading": "<Mileage at the time of transfer. Look for 'Miles', 'ODO', or 'Mileage'.>",
        "odometer_disclosure_type": "<Disclosure of odometer accuracy. Look for 'Actual', 'Not Actual', 'Exceeds', or 'Odometer Type'.>",
        "seller_name": "<Name of the seller or transferor. Look for 'Seller', 'Current Owner', or 'Transferor'.>",
        "seller_address": "<Address of the seller. May be under 'Seller Address' or 'Address of Seller'.>",
        "buyer_name": "<Name of the buyer. Look for 'Buyer', 'Purchaser', or 'New Owner'.>",
        "buyer_address": "<Residential address of the buyer. May be labeled as 'Buyer Address', 'Residence', or 'Street Address'.>",
        "date_of_reassignment": "<Date the vehicle was reassigned or title transferred. Look for 'Reassignment Date' or 'Title Transfer Date'.>",
        "seller_signature": "<Signature of the seller. Look for 'Seller Signature' or similar label.>",
        "buyer_signature": "<Signature of the buyer. May appear as 'Buyer Signature' or 'Signature of Buyer'.>"
    }
}

fields_json = {
    "titlemso": {
        "deal_number": "1200090 [Id: 'unique_id_1']",
        "stock_number": "STK12345 [Id: 'unique_id_2']",
        "vin": "2T2BBMCA1RC061029 [Id: 'unique_id_3']",
        "year": "2024 [Id: 'unique_id_4']",
        "make": "LEXUS [Id: 'unique_id_5']",
        "model": "RX 350h PREMIUM [Id: 'unique_id_6']",
        "odometer_reading": "10 MI [Id: 'unique_id_7']",
        "buyer_name": "HERMAN DOUGLAS J [Id: 'unique_id_8']",
        "co_buyer_name": "JPMORGAN CHASE BANK NA LSE [Id: 'unique_id_9']",
        "buyer_address": "4425 [Id: 'unique_id_10'] SHEPHERDS [Id: 'unique_id_11'] LN [Id: 'unique_id_12'] LA [Id: 'unique_id_13'] CANADA [Id: 'unique_id_14'] CA [Id: 'unique_id_15'] 91011 [Id: 'unique_id_16']",
        "sale_price": "$45,600.00 [Id: 'unique_id_17']",
        "tavt_tax_amount": "$1,450.00 [Id: 'unique_id_18']",
        "trade_in_value": "$5,000.00 [Id: 'unique_id_19']",
        "total_amount_due": "$42,050.00 [Id: 'unique_id_20']",
        "lien_holder_name": "JPMORGAN CHASE BANK NA [Id: 'unique_id_21']",
        "dealer_fees": "$699.00 [Id: 'unique_id_22']"
    },
    "bill_of_sale": {
        "deal_number": "1200090 [Id: 'unique_id_1']",
        "stock_number": "STK12345 [Id: 'unique_id_2']",
        "vin": "2T2BBMCA1RC061029 [Id: 'unique_id_3']",
        "year": "2024 [Id: 'unique_id_4']",
        "make": "LEXUS [Id: 'unique_id_5']",
        "model": "RX 350h PREMIUM [Id: 'unique_id_6']",
        "odometer_reading": "10 MI [Id: 'unique_id_7']",
        "buyer_name": "HERMAN DOUGLAS J [Id: 'unique_id_8']",
        "co_buyer_name": "JPMORGAN CHASE BANK NA LSE [Id: 'unique_id_9']",
        "buyer_address": "4425 [Id: 'unique_id_10'] SHEPHERDS [Id: 'unique_id_11'] LN [Id: 'unique_id_12'] LA [Id: 'unique_id_13'] CANADA [Id: 'unique_id_14'] CA [Id: 'unique_id_15'] 91011 [Id: 'unique_id_16']",
        "sale_price": "$45,600.00 [Id: 'unique_id_17']",
        "tavt_tax_amount": "$1,450.00 [Id: 'unique_id_18']",
        "trade_in_value": "$5,000.00 [Id: 'unique_id_19']",
        "total_amount_due": "$42,050.00 [Id: 'unique_id_20']",
        "lien_holder_name": "JPMORGAN CHASE BANK NA [Id: 'unique_id_21']",
        "dealer_fees": "$699.00 [Id: 'unique_id_22']"
    },
     "driver_license": {
        "full_name": "JANE DOE [Id: 'unique_id_1']",
        "date_of_birth": "01/15/1985 [Id: 'unique_id_2']",
        "address": "123 MAIN ST [Id: 'unique_id_3']",
        "city": "ATLANTA [Id: 'unique_id_4']",
        "state": "GA [Id: 'unique_id_5']",
        "zip": "30303 [Id: 'unique_id_6']",
        "driver_s_license_number": "D12345678 [Id: 'unique_id_7']",
        "expiration_date": "01/15/2030 [Id: 'unique_id_8']"
    },
    "red_reassignment": {
        "vin": "2T2BBMCA1RC061029 [Id: 'unique_id_1']",
        "year": "2024 [Id: 'unique_id_2']",
        "make": "LEXUS [Id: 'unique_id_3']",
        "model": "RX 350h [Id: 'unique_id_4']",
        "odometer_reading": "10 [Id: 'unique_id_5']",
        "odometer_type": "ACTUAL [Id: 'unique_id_6']",
        "buyer_name": "JAMES SMITH [Id: 'unique_id_7']",
        "buyer_address": "123 MAIN ST, ATLANTA, GA 30303 [Id: 'unique_id_8']",
        "date_of_reassignment": "07/30/2025 [Id: 'unique_id_9']",
        "signatures": "SELLER SIGNATURE: JOHN DOE [Id: 'unique_id_10'], BUYER SIGNATURE: JAMES SMITH [Id: 'unique_id_11']"
    },
    "mv-1": {
        "buyer_full_name": "JANE DOE [Id: 'unique_id_1']",
        "co_buyer_name": "JOHN DOE [Id: 'unique_id_2']",
        "buyer_address": "123 MAIN ST [Id: 'unique_id_3']",
        "city": "ATLANTA [Id: 'unique_id_4']",
        "state": "GA [Id: 'unique_id_5']",
        "zip": "30303 [Id: 'unique_id_6']",
        "county_of_residence": "FULTON [Id: 'unique_id_7']",
        "customer_id": "GA123456789 [Id: 'unique_id_8']",
        "vin": "1HGCM82633A004352 [Id: 'unique_id_9']",
        "year": "2023 [Id: 'unique_id_10']",
        "make": "HONDA [Id: 'unique_id_11']",
        "model": "ACCORD [Id: 'unique_id_12']",
        "body_style": "SEDAN [Id: 'unique_id_13']",
        "odometer_reading": "25,000 MI [Id: 'unique_id_14']",
        "lien_holder_name": "WELLS FARGO BANK [Id: 'unique_id_15']",
        "lien_holder_address": "420 MONTGOMERY ST, SF, CA [Id: 'unique_id_16']",
        "dealer_name": "BEST CARS INC [Id: 'unique_id_17']",
        "dealer_number": "DLR78901 [Id: 'unique_id_18']",
        "sale_price": "$19,800.00 [Id: 'unique_id_19']"
    },
    "mv-7d": {
        "vin": "1FTFW1ET1EKD12345 [Id: 'unique_id_1']",
        "year": "2022 [Id: 'unique_id_2']",
        "make": "FORD [Id: 'unique_id_3']",
        "model": "F-150 [Id: 'unique_id_4']",
        "odometer_reading": "35,000 MI [Id: 'unique_id_5']",
        "odometer_disclosure_type": "ACTUAL [Id: 'unique_id_6']",
        "seller_name": "JACK SMITH [Id: 'unique_id_7']",
        "seller_address": "789 ELM ST, ORLANDO, FL 32801 [Id: 'unique_id_8']",
        "buyer_name": "EMILY JOHNSON [Id: 'unique_id_9']",
        "buyer_address": "456 OAK AVE, TAMPA, FL 33606 [Id: 'unique_id_10']",
        "date_of_reassignment": "06/15/2024 [Id: 'unique_id_11']",
        "seller_signature": "JACK SMITH [Id: 'unique_id_12']",
        "buyer_signature": "EMILY JOHNSON [Id: 'unique_id_13']"
    }
}

fields_json_v2 = {
    "titlemso": {
        "deal_number": "1200090",
        "stock_number": "STK12345",
        "vin": "2T2BBMCA1RC061029",
        "year": "2024",
        "make": "LEXUS",
        "model": "RX 350h PREMIUM",
        "odometer_reading": "10 MI",
        "buyer_name": "HERMAN DOUGLAS J",
        "co_buyer_name": "JPMORGAN CHASE BANK NA LSE",
        "buyer_address": "4425 SHEPHERDS LN LA CANADA CA 91011",
        "sale_price": "$45,600.00",
        "tavt_tax_amount": "$1,450.00",
        "trade_in_value": "$5,000.00",
        "total_amount_due": "$42,050.00",
        "lien_holder_name": "JPMORGAN CHASE BANK NA",
        "dealer_fees": "$699.00"
    },
    "bill_of_sale": {
        "deal_number": "1200090",
        "stock_number": "STK12345",
        "vin": "2T2BBMCA1RC061029",
        "year": "2024",
        "make": "LEXUS",
        "model": "RX 350h PREMIUM",
        "odometer_reading": "10 MI",
        "buyer_name": "HERMAN DOUGLAS J",
        "co_buyer_name": "JPMORGAN CHASE BANK NA LSE",
        "buyer_address": "4425 SHEPHERDS LN LA CANADA CA 91011",
        "sale_price": "$45,600.00",
        "tavt_tax_amount": "$1,450.00",
        "trade_in_value": "$5,000.00",
        "total_amount_due": "$42,050.00",
        "lien_holder_name": "JPMORGAN CHASE BANK NA",
        "dealer_fees": "$699.00"
    },
    "driver_license": {
        "full_name": "JANE DOE",
        "date_of_birth": "01/15/1985",
        "address": "123 MAIN ST",
        "city": "ATLANTA",
        "state": "GA",
        "zip": "30303",
        "driver_s_license_number": "D12345678",
        "expiration_date": "01/15/2030"
    },
    "red_reassignment": {
        "vin": "2T2BBMCA1RC061029",
        "year": "2024",
        "make": "LEXUS",
        "model": "RX 350h",
        "odometer_reading": "10",
        "odometer_type": "ACTUAL",
        "buyer_name": "JAMES SMITH",
        "buyer_address": "123 MAIN ST, ATLANTA, GA 30303",
        "date_of_reassignment": "07/30/2025",
        "signatures": "SELLER SIGNATURE: JOHN DOE, BUYER SIGNATURE: JAMES SMITH"
    },
    "mv-1": {
        "buyer_full_name": "JANE DOE",
        "co_buyer_name": "JOHN DOE",
        "buyer_address": "123 MAIN ST",
        "city": "ATLANTA",
        "state": "GA",
        "zip": "30303",
        "county_of_residence": "FULTON",
        "customer_id": "GA123456789",
        "vin": "1HGCM82633A004352",
        "year": "2023",
        "make": "HONDA",
        "model": "ACCORD",
        "body_style": "SEDAN",
        "odometer_reading": "25,000 MI",
        "lien_holder_name": "WELLS FARGO BANK",
        "lien_holder_address": "420 MONTGOMERY ST, SF, CA",
        "dealer_name": "BEST CARS INC",
        "dealer_number": "DLR78901",
        "sale_price": "$19,800.00"
    },
    "mv-7d": {
        "vin": "1FTFW1ET1EKD12345",
        "year": "2022",
        "make": "FORD",
        "model": "F-150",
        "odometer_reading": "35,000 MI",
        "odometer_disclosure_type": "ACTUAL",
        "seller_name": "JACK SMITH",
        "seller_address": "789 ELM ST, ORLANDO, FL 32801",
        "buyer_name": "EMILY JOHNSON",
        "buyer_address": "456 OAK AVE, TAMPA, FL 33606",
        "date_of_reassignment": "06/15/2024",
        "seller_signature": "JACK SMITH",
        "buyer_signature": "EMILY JOHNSON"
    }
}

fields_type = {
    "titlemso": {
        "deal_number": {
            "type": "regular"
        },
        "stock_number": {
            "type": "regular"
        },
        "vin": {
            "type": "regular"
        },
        "year": {
            "type": "regular"
        },
        "make": {
            "type": "regular"
        },
        "model": {
            "type": "regular"
        },
        "odometer_reading": {
            "type": "regular"
        },
        "buyer_name": {
            "type": "regular"
        },
        "co_buyer_name": {
            "type": "regular"
        },
        "buyer_address": {
            "type": "regular"
        },
        "sale_price": {
            "type": "regular"
        },
        "tavt_tax_amount": {
            "type": "regular"
        },
        "trade_in_value": {
            "type": "regular"
        },
        "total_amount_due": {
            "type": "regular"
        },
        "lien_holder_name": {
            "type": "regular"
        },
        "dealer_fees": {
            "type": "regular"
        }
    },
    "bill_of_sale": {
        "deal_number": {"type": "regular"},
        "stock_number": {"type": "regular"},
        "vin": {"type": "regular"},
        "year": {"type": "regular"},
        "make": {"type": "regular"},
        "model": {"type": "regular"},
        "odometer_reading": {"type": "regular"},
        "buyer_name": {"type": "regular"},
        "co_buyer_name": {"type": "regular"},
        "buyer_address": {"type": "regular"},
        "sale_price": {"type": "regular"},
        "tavt_tax_amount": {"type": "regular"},
        "trade_in_value": {"type": "regular"},
        "total_amount_due": {"type": "regular"},
        "lien_holder_name": {"type": "regular"},
        "dealer_fees": {"type": "regular"}
    },
    "driver_license": {
        "full_name": {"type": "regular"},
        "date_of_birth": {"type": "regular"},
        "address": {"type": "regular"},
        "city": {"type": "regular"},
        "state": {"type": "regular"},
        "zip": {"type": "regular"},
        "driver_s_license_number": {"type": "regular"},
        "expiration_date": {"type": "regular"}
    },
    "red_reassignment": {
        "vin": {"type": "regular"},
        "year": {"type": "regular"},
        "make": {"type": "regular"},
        "model": {"type": "regular"},
        "odometer_reading": {"type": "regular"},
        "odometer_type": {"type": "regular"},
        "buyer_name": {"type": "regular"},
        "buyer_address": {"type": "regular"},
        "date_of_reassignment": {"type": "regular"},
        "signatures": {"type": "regular"}
    },
    "mv-1": {
        "buyer_full_name": {"type": "regular"},
        "co_buyer_name": {"type": "regular"},
        "buyer_address": {"type": "regular"},
        "city": {"type": "regular"},
        "state": {"type": "regular"},
        "zip": {"type": "regular"},
        "county_of_residence": {"type": "regular"},
        "customer_id": {"type": "regular"},
        "vin": {"type": "regular"},
        "year": {"type": "regular"},
        "make": {"type": "regular"},
        "model": {"type": "regular"},
        "body_style": {"type": "regular"},
        "odometer_reading": {"type": "regular"},
        "lien_holder_name": {"type": "regular"},
        "lien_holder_address": {"type": "regular"},
        "dealer_name": {"type": "regular"},
        "dealer_number": {"type": "regular"},
        "sale_price": {"type": "regular"}
    },
    "mv-7d": {
        "vin": {"type": "regular"},
        "year": {"type": "regular"},
        "make": {"type": "regular"},
        "model": {"type": "regular"},
        "odometer_reading": {"type": "regular"},
        "odometer_disclosure_type": {"type": "regular"},
        "seller_name": {"type": "regular"},
        "seller_address": {"type": "regular"},
        "buyer_name": {"type": "regular"},
        "buyer_address": {"type": "regular"},
        "date_of_reassignment": {"type": "regular"},
        "seller_signature": {"type": "regular"},
        "buyer_signature": {"type": "regular"}
    }
}