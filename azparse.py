"""parses xml returned from amazon"""
import untangle

def parse_file(path):
    """Returns a xmlobject of the file at path"""
    return untangle.parse(path)

def keywords(parse_obj):
    """Returns the keywords of the xmlobject"""
    return parse_obj.ItemSearchResponse.Items.Request.ItemSearchRequest.Keywords.cdata

def num_results(parse_obj):
    """Returns the number of results from parse_object"""
    return parse_obj.ItemSearchResponse.Items.TotalResults.cdata

def price_data(parse_obj):
    """Returns the min, avg, and max prices for top listings"""
    prices = []
    try:
        for item in parse_obj.ItemSearchResponse.Items.Item:
            prices.append(int(item.OfferSummary.LowestNewPrice.Amount.cdata))
    except Exception as e:
        print(e)
        print("Failed to extract price data")
    return repr(min(prices)), repr(sum(prices)//len(prices)), repr(max(prices))

def handler(parse_obj, action, item_index=0):
    """Returns the effect of running action"""
    #check to see if index is valid
    if item_index < len(parse_obj.ItemSearchResponse.Items.Item):
        item = parse_obj.ItemSearchResponse.Items.Item[item_index]
    else:
        return None
    actions = {'IsValid':lambda:parse_obj.ItemSearchResponse.Items.Request.IsValid.cdata,
               'ItemPage':lambda:parse_obj.ItemSearchResponse.Items.Request.ItemSearchRequest.ItemPage.cdata,
               'TotalResults':lambda:parse_obj.ItemSearchResponse.Items.TotalResults.cdata,
               'ASIN':lambda:item.ASIN.cdata,
               'SalesRank':lambda:item.SalesRank.cdata,
               'Department':lambda:item.ItemAttributes.Department.cdata,
               'EAN':lambda:item.ItemAttributes.EAN.cdata,
               'Weight':lambda:item.ItemAttributes.PackageDimensions.Weight.cdata,
               'ListPrice':lambda:item.ItemAttributes.ListPrice.Amount.cdata,
               'Manufacturer':lambda:item.ItemAttributes.Manufacturer.cdata,
               'Title':lambda:item.ItemAttributes.Title.cdata,
               'UPC':lambda:item.ItemAttributes.UPC.cdata,
               'LowestNewPrice':lambda:item.OfferSummary.LowestNewPrice.Amount.cdata,
               'TotalNew':lambda:item.OfferSummary.TotalNew.cdata,
               'TotalOffers':lambda:item.Offers.TotalOffers.cdata, #buybox
               'MerchantName':lambda:item.Offers.Offer.Merchant.Name.cdata,
               'OfferPrice':lambda:item.Offers.Offer.OfferListing.Price.Amount.cdata,
               'EligibleForPrime':lambda:item.Offers.Offer.OfferListing.IsEligibleForPrime.cdata
               }
    try:
        return actions[action]()
    except:
        return None
