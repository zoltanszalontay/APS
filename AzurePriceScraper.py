# v10
# -*- coding: utf-8 -*-
import logging
import urllib.request
from bs4 import BeautifulSoup

class AzurePriceList:
    """Scrape the actual IaaS prices from the Azure Price list webpage"""

    BaseURL = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/"

    product_url = {
        "CentOS or Ubuntu Linux":                           "linux",
        "Red Hat Enterprise Linux":                          "red-hat",
        "SUSE Linux Enterprise":                             "sles",
        "SUSE Linux Enterprise for SAP":                     "sles-sap",
        "SQL Server Enterprise Ubuntu Linux":                "sql-server-enterprise-linux",
        "SQL Server Standard Ubuntu Linux":                  "sql-server-standard-linux",
        "SQL Server Web Ubuntu Linux":                       "sql-server-web-linux",
        "SQL Server Enterprise Red Hat Enterprise Linux":    "sql-server-enterprise-redhat",
        "SQL Server Standard Red Hat Enterprise Linux":      "sql-server-standard-redhat",
        "SQL Server Web Red Hat Enterprise Linux":           "sql-server-web-redhat",
        "SQL Server Enterprise SUSE":                        "sql-server-enterprise-sles",
        "SQL Server Standard SUSE":                          "sql-server-standard-sles",
        "SQL Server Web SUSE":                               "sql-server-web-sles",
        "Windows Operating System":                          "windows",
        "BizTalk Enterprise":                                "biztalk-enterprise",
        "BizTalk Standard":                                  "biztalk-standard",
        "Oracle Java":                                       "oracle-java",
        "SharePoint":                                        "sharepoint",
        "SQL Server Enterprise":                             "sql-server-enterprise",
        "SQL Server Standard":                               "sql-server-standard",
        "SQL Server Web":                                    "sql-server-web"
    }

    machine = []
    pricelist = [[]]
    firstpricecolumn = 0
    columns = 0

    def __init__(self, product_name, log_lvl=logging.INFO):
        # Start logging
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if len(self.log.handlers) == 0:
            self.log.addHandler(logging.StreamHandler())
        self.log.info("Product name: %s", product_name)

        # URL = AzurePriceList base URL + product specific relative path
        self.url = AzurePriceList.BaseURL + AzurePriceList.product_url[product_name] + "/"
        self.log.info("URL: %s", self.url)

    def scrape(self):
        self.log.info("Scraping starts...")
        source = urllib.request.urlopen("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/").read()
        soup = BeautifulSoup(source, 'lxml')
        
        #
        # HEADER ROW
        #  
        # Drop 1st row
        self.log.info("=====================================")
        self.log.info("Pricelist: %s", self.pricelist)
        self.log.info("Scraping header")
        row = soup.find(class_="sd-table").find_all('th')[1:]
        i = 0
        for cell in row:
            self.machine.append(cell.text)
            if(cell.text == " Pay as you go "):
                firstpricecolumn = i
            i = i + 1
        columns = i
        #self.log.info("Header: %s", self.machine)
        self.pricelist.append(self.machine)
        self.log.info("Pricelist: %s", self.pricelist)
        #
        # MACHINE PRICES
        #
        # machine_idx starts with 1 because pricelist[[]] has an empty first list element!
        machine_idx = 1
        while True:
            self.log.info("Scraping row #%d", machine_idx)
            # Drop 1st row
            row = soup.find(class_="sd-table").find_all('td')[1:]
            # self.log.info("row: %s", row) 
            i = 0
            self.machine = []
            # Scrape left columns
            for cell in row:
                if(i == firstpricecolumn):
                    break
                self.machine.append(cell.text)
                i = i + 1
            # Scraping last 4 price columns
            self.log.info("Scraping %s price columns", self.machine[0])
            prices = soup.b
            self.log.info("Type: %s", prices)
 
            # Add machine prices to pricelist 
            self.pricelist.append(self.machine)
            # self.log.info("Machine: %s", self.pricelist[machine_idx])
            machine_idx = machine_idx + 1
            # Exit after first machine price row
            if(machine_idx == 2):
                break
            
        # Log pricelist
        self.log.info("Pricelist: %s", self.pricelist)
        # for i in range(len(self.pricelist)):
        #     for j in range(len(self.pricelist[i])):
        #         self.log.info("machine[%d] = %s", i, self.pricelist[i][j])

########
#      #
# Main #
#      #
########

# Start scraping, get prices
apl = AzurePriceList("Windows Operating System", log_lvl=logging.INFO)
apl.scrape()

'''
[   <td>B1S</td>, 
    <td>1</td>, 
    <td>1.00 GiB</td>, 
    <td>2 GiB</td>, 
    <td class="payg-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.023,
                    "asia-pacific-southeast":0.018,
                    "australia-east":0.02,
                    "australia-southeast":0.02,
                    "brazil-south":0.023,
                    "canada-central":0.016,
                    "canada-east":0.018,
                    "central-india":0.018,
                    "europe-north":0.016,
                    "europe-west":0.0171,
                    "japan-east":0.021,
                    "japan-west":0.021,
                    "korea-central":0.019,
                    "korea-south":0.017,
                    "south-india":0.02,
                    "united-kingdom-south":0.019,
                    "united-kingdom-west":0.019,
                    "us-central":0.019,
                    "us-east":0.0153,
                    "us-east-2":0.019,
                    "us-north-central":0.017,
                    "us-south-central":0.019,
                    "us-west":0.018,
                    "us-west-2":0.017,
                    "us-west-central":0.019
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
    </td>,
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.01667,
                    "asia-pacific-southeast":0.01245,
                    "australia-east":0.01313,
                    "australia-southeast":0.01313,
                    "brazil-south":0.01382,
                    "canada-central":0.01142,
                    "canada-east":0.01142,
                    "central-india":0.01233,
                    "europe-north":0.01222,
                    "europe-west":0.01279,
                    "japan-east":0.01359,
                    "japan-west":0.01359,
                    "korea-central":0.01199,
                    "korea-south":0.01039,
                    "south-india":0.01405,
                    "united-kingdom-south":0.01256,
                    "united-kingdom-west":0.01256,
                    "us-central":0.01211,
                    "us-east":0.01074,
                    "us-east-2":0.01211,
                    "us-north-central":0.01074,
                    "us-south-central":0.01211,
                    "us-west":0.01336,
                    "us-west-2":0.01074,
                    "us-west-central":0.01211
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings">
        </span> 
    </td>, 
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.01207,
                    "asia-pacific-southeast":0.00937,
                    "australia-east":0.01016,
                    "australia-southeast":0.01016,
                    "brazil-south":0.01104,
                    "canada-central":0.00883,
                    "canada-east":0.00883,
                    "central-india":0.00929,
                    "europe-north":0.00952,
                    "europe-west":0.01005,
                    "japan-east":0.01054,
                    "japan-west":0.01054,
                    "korea-central":0.00952,
                    "korea-south":0.00841,
                    "south-india":0.01035,
                    "united-kingdom-south":0.00982,
                    "united-kingdom-west":0.00982,
                    "us-central":0.00925,
                    "us-east":0.00838,
                    "us-east-2":0.00925,
                    "us-north-central":0.00838,
                    "us-south-central":0.00925,
                    "us-west":0.00997,
                    "us-west-2":0.00838,
                    "us-west-central":0.00925
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings"></span> 
    </td>, 
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.00807,
                    "asia-pacific-southeast":0.00537,
                    "australia-east":0.00616,
                    "australia-southeast":0.00616,
                    "brazil-south":0.00704,
                    "canada-central":0.00483,
                    "canada-east":0.00483,
                    "central-india":0.00529,
                    "europe-north":0.00552,
                    "europe-west":0.00605,
                    "japan-east":0.00654,
                    "japan-west":0.00654,
                    "korea-central":0.00552,
                    "korea-south":0.00441,
                    "south-india":0.00635,
                    "united-kingdom-south":0.00582,
                    "united-kingdom-west":0.00582,
                    "us-central":0.00525,
                    "us-east":0.00438,
                    "us-east-2":0.00525,
                    "us-north-central":0.00438,
                    "us-south-central":0.00525,
                    "us-west":0.00597,
                    "us-west-2":0.00438,
                    "us-west-central":0.00525
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings">
        </span> 
    </td>, 
    <td> 
        <span class="wa-conditionalDisplay" 
            data-condition-region="
                asia-pacific-east 
                asia-pacific-southeast 
                australia-east 
                australia-southeast 
                brazil-south 
                canada-central 
                canada-east 
                central-india 
                europe-north 
                europe-west 
                japan-east 
                japan-west 
                korea-central 
                korea-south 
                south-india 
                united-kingdom-south 
                united-kingdom-west 
                us-central 
                us-east 
                us-east-2 
                us-north-central 
                us-south-central
                us-west us-west-2 
                us-west-central"> 
            <button class="module-builder" 
                data-event="pricingdetails-clicked-addinstance" 
                data-event-property="B2S" 
                data-module-configuration='{
                    "tier": "standard", 
                    "size": "b2s", 
                    "operatingSystem" : "windows", 
                    "type": "os-only", 
                    "license": ""
                }' 
                data-notification-title="B2S" 
                data-product="virtual-machines" 
                type="button"> 
                <span class="icon icon-size2">
                    <svg aria-hidden="true" 
                        role="presentation">
                        <use xlink:href="#svg-add-button">
                        </use>
                    </svg>
                </span> 
            </button> 
        </span> 
    </td>, 
    <td>B2S</td>, 
    <td>2</td>, 
    <td>4.00 GiB</td>, 
    <td>8 GiB</td>, 
    <td class="payg-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.088,
                    "asia-pacific-southeast":0.0702,
                    "australia-east":0.082,
                    "australia-southeast":0.082,
                    "brazil-south":0.089,
                    "canada-central":0.063,
                    "canada-east":0.07,
                    "central-india":0.069,
                    "europe-north":0.061,
                    "europe-west":0.0648,
                    "japan-east":0.082,
                    "japan-west":0.082,
                    "korea-central":0.074,
                    "korea-south":0.066,
                    "south-india":0.076,
                    "united-kingdom-south":0.07,
                    "united-kingdom-west":0.07,
                    "us-central":0.072,
                    "us-east":0.0585,
                    "us-east-2":0.072,
                    "us-north-central":0.065,
                    "us-south-central":0.072,
                    "us-west":0.071,
                    "us-west-2":0.065,
                    "us-west-central":0.072
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
    </td>, 
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.05891,
                    "asia-pacific-southeast":0.04190,
                    "australia-east":0.04464,
                    "australia-southeast":0.04464,
                    "brazil-south":0.04738,
                    "canada-central":0.03779,
                    "canada-east":0.03779,
                    "central-india":0.04145,
                    "europe-north":0.04111,
                    "europe-west":0.04362,
                    "japan-east":0.04636,
                    "japan-west":0.04636,
                    "korea-central":0.04008,
                    "korea-south":0.03368,
                    "south-india":0.04818,
                    "united-kingdom-south":0.04236,
                    "united-kingdom-west":0.04236,
                    "us-central":0.04019,
                    "us-east":0.03483,
                    "us-east-2":0.04019,
                    "us-north-central":0.03483,
                    "us-south-central":0.04019,
                    "us-west":0.04544,
                    "us-west-2":0.03483,
                    "us-west-central":0.04019
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings"></span> 
    </td>, 
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.04031,
                    "asia-pacific-southeast":0.02954,
                    "australia-east":0.03258,
                    "australia-southeast":0.03258,
                    "brazil-south":0.03616,
                    "canada-central":0.02733,
                    "canada-east":0.02733,
                    "central-india":0.02912,
                    "europe-north":0.03003,
                    "europe-west":0.03228,
                    "japan-east":0.03414,
                    "japan-west":0.03414,
                    "korea-central":0.02999,
                    "korea-south":0.02558,
                    "south-india":0.03334,
                    "united-kingdom-south":0.03133,
                    "united-kingdom-west":0.03133,
                    "us-central":0.02893,
                    "us-east":0.02543,
                    "us-east-2":0.02893,
                    "us-north-central":0.02543,
                    "us-south-central":0.02893,
                    "us-west":0.03193,
                    "us-west-2":0.02543,
                    "us-west-central":0.02893
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings"></span> 
    </td>, 
    <td class="discounted-price"> 
        <span class="price-data " 
            data-amount='{
                "regional":{
                    "asia-pacific-east":0.03231,
                    "asia-pacific-southeast":0.02154,
                    "australia-east":0.02458,
                    "australia-southeast":0.02458,
                    "brazil-south":0.02816,
                    "canada-central":0.01933,
                    "canada-east":0.01933,
                    "central-india":0.02112,
                    "europe-north":0.02203,
                    "europe-west":0.02428,
                    "japan-east":0.02614,
                    "japan-west":0.02614,
                    "korea-central":0.02199,
                    "korea-south":0.01758,
                    "south-india":0.02534,
                    "united-kingdom-south":0.02333,
                    "united-kingdom-west":0.02333,
                    "us-central":0.02093,
                    "us-east":0.01743,
                    "us-east-2":0.02093,
                    "us-north-central":0.01743,
                    "us-south-central":0.02093,
                    "us-west":0.02393,
                    "us-west-2":0.01743,
                    "us-west-central":0.02093
                }
            }' 
            data-decimals="3" 
            data-hour-format="{0}/hour" 
            data-month-format="{0}/month" 
            data-region-unavailable="N/A">$-
        </span> 
        <span class="percent-savings"></span> 
    </td>, 
    <td> 
        <span class="wa-conditionalDisplay" 
            data-condition-region="
                asia-pacific-east 
                asia-pacific-southeast 
                australia-east 
                australia-southeast 
                brazil-south 
                canada-central 
                canada-east 
                central-india 
                europe-north 
                europe-west 
                japan-east 
                japan-west 
                korea-central 
                korea-south 
                south-india 
                united-kingdom-south 
                united-kingdom-west 
                us-central us-east 
                us-east-2 
                us-north-central 
                us-south-central 
                us-west us-west-2 
                us-west-central"> 
            <button class="module-builder" 
                data-event="pricingdetails-clicked-addinstance" 
                data-event-property="B1MS" 
                data-module-configuration='{
                    "tier": "standard", 
                    "size": "b1ms", 
                    "operatingSystem" : "windows", 
                    "type": "os-only", "license": ""
                }' 
                data-notification-title="B1MS" 
                data-product="virtual-machines" 
                type="button"> 
                <span class="icon icon-size2">
                    <svg aria-hidden="true" role="presentation">
                        <use xlink:href="#svg-add-button"></use>
                    </svg>
                </span>
            </button> 
        </span> 
    </td>, 
    <td>B1MS</td>, 
    <td>1</td>, 
    <td>2.00 GiB</td>, 
    <td>4 GiB</td>, 
    <td class="payg-price"> 
        <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.044,"asia-pacific-southeast":0.0351,"australia-east":0.041,"australia-southeast":0.041,"brazil-south":0.045,"canada-central":0.032,"canada-east":0.035,"central-india":0.035,"europe-north":0.031,"europe-west":0.0324,"japan-east":0.041,"japan-west":0.041,"korea-central":0.037,"korea-south":0.033,"south-india":0.039,"united-kingdom-south":0.035,"united-kingdom-west":0.035,"us-central":0.035,"us-east":0.0288,"us-east-2":0.035,"us-north-central":0.032,"us-south-central":0.035,"us-west":0.036,"us-west-2":0.032,"us-west-central":0.035}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.02934,"asia-pacific-southeast":0.02089,"australia-east":0.02226,"australia-southeast":0.02226,"brazil-south":0.02375,"canada-central":0.01884,"canada-east":0.01884,"central-india":0.02078,"europe-north":0.02055,"europe-west":0.02181,"japan-east":0.02318,"japan-west":0.02318,"korea-central":0.02010,"korea-south":0.01690,"south-india":0.02409,"united-kingdom-south":0.02124,"united-kingdom-west":0.02124,"us-central":0.02021,"us-east":0.01747,"us-east-2":0.02021,"us-north-central":0.01747,"us-south-central":0.02021,"us-west":0.02272,"us-west-2":0.01747,"us-west-central":0.02021}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.02017,"asia-pacific-southeast":0.01477,"australia-east":0.01629,"australia-southeast":0.01629,"brazil-south":0.01808,"canada-central":0.01367,"canada-east":0.01367,"central-india":0.01458,"europe-north":0.01504,"europe-west":0.01614,"japan-east":0.01705,"japan-west":0.01705,"korea-central":0.01500,"korea-south":0.01279,"south-india":0.01671,"united-kingdom-south":0.01568,"united-kingdom-west":0.01568,"us-central":0.01446,"us-east":0.01271,"us-east-2":0.01446,"us-north-central":0.01271,"us-south-central":0.01446,"us-west":0.01599,"us-west-2":0.01271,"us-west-central":0.01446}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.01617,"asia-pacific-southeast":0.01077,"australia-east":0.01229,"australia-southeast":0.01229,"brazil-south":0.01408,"canada-central":0.00967,"canada-east":0.00967,"central-india":0.01058,"europe-north":0.01104,"europe-west":0.01214,"japan-east":0.01305,"japan-west":0.01305,"korea-central":0.011,"korea-south":0.00879,"south-india":0.01271,"united-kingdom-south":0.01168,"united-kingdom-west":0.01168,"us-central":0.01046,"us-east":0.00871,"us-east-2":0.01046,"us-north-central":0.00871,"us-south-central":0.01046,"us-west":0.01199,"us-west-2":0.00871,"us-west-central":0.01046}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td> <span class="wa-conditionalDisplay" data-condition-region="asia-pacific-east asia-pacific-southeast australia-east australia-southeast brazil-south canada-central canada-east central-india europe-north europe-west japan-east japan-west korea-central korea-south south-india united-kingdom-south united-kingdom-west us-central us-east us-east-2 us-north-central us-south-central us-west us-west-2 us-west-central"> <button class="module-builder" data-event="pricingdetails-clicked-addinstance" data-event-property="B2MS" data-module-configuration='{"tier": "standard", "size": "b2ms", "operatingSystem" : "windows", "type": "os-only", "license": ""}' data-notification-title="B2MS" data-product="virtual-machines" type="button"> <span class="icon icon-size2"><svg aria-hidden="true" role="presentation"><use xlink:href="#svg-add-button"></use></svg></span> </button> </span> </td>, <td>B2MS</td>, <td>2</td>, <td>8.00 GiB</td>, <td>16 GiB</td>, <td class="payg-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.167,"asia-pacific-southeast":0.1332,"australia-east":0.156,"australia-southeast":0.156,"brazil-south":0.171,"canada-central":0.118,"canada-east":0.131,"central-india":0.132,"europe-north":0.116,"europe-west":0.1224,"japan-east":0.156,"japan-west":0.156,"korea-central":0.14,"korea-south":0.126,"south-india":0.146,"united-kingdom-south":0.134,"united-kingdom-west":0.134,"us-central":0.134,"us-east":0.1098,"us-east-2":0.134,"us-north-central":0.122,"us-south-central":0.134,"us-west":0.135,"us-west-2":0.122,"us-west-central":0.134}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.10971,"asia-pacific-southeast":0.07581,"australia-east":0.08129,"australia-southeast":0.08129,"brazil-south":0.08688,"canada-central":0.06747,"canada-east":0.06747,"central-india":0.07501,"europe-north":0.07421,"europe-west":0.07935,"japan-east":0.08471,"japan-west":0.08471,"korea-central":0.07227,"korea-south":0.05937,"south-india":0.08837,"united-kingdom-south":0.07684,"united-kingdom-west":0.07684,"us-central":0.07238,"us-east":0.06165,"us-east-2":0.07238,"us-north-central":0.06165,"us-south-central":0.07238,"us-west":0.08289,"us-west-2":0.06165,"us-west-central":0.07238}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.07257,"asia-pacific-southeast":0.05104,"australia-east":0.05720,"australia-southeast":0.05720,"brazil-south":0.06432,"canada-central":0.04666,"canada-east":0.04666,"central-india":0.05028,"europe-north":0.05210,"europe-west":0.05652,"japan-east":0.06028,"japan-west":0.06028,"korea-central":0.05203,"korea-south":0.04324,"south-india":0.05872,"united-kingdom-south":0.05465,"united-kingdom-west":0.05465,"us-central":0.04986,"us-east":0.04289,"us-east-2":0.04986,"us-north-central":0.04289,"us-south-central":0.04986,"us-west":0.05591,"us-west-2":0.04289,"us-west-central":0.04986}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.06457,"asia-pacific-southeast":0.04304,"australia-east":0.0492,"australia-southeast":0.0492,"brazil-south":0.05632,"canada-central":0.03866,"canada-east":0.03866,"central-india":0.04228,"europe-north":0.0441,"europe-west":0.04852,"japan-east":0.05228,"japan-west":0.05228,"korea-central":0.04403,"korea-south":0.03524,"south-india":0.05072,"united-kingdom-south":0.04665,"united-kingdom-west":0.04665,"us-central":0.04186,"us-east":0.03489,"us-east-2":0.04186,"us-north-central":0.03489,"us-south-central":0.04186,"us-west":0.04791,"us-west-2":0.03489,"us-west-central":0.04186}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td> <span class="wa-conditionalDisplay" data-condition-region="asia-pacific-east asia-pacific-southeast australia-east australia-southeast brazil-south canada-central canada-east central-india europe-north europe-west japan-east japan-west korea-central korea-south south-india united-kingdom-south united-kingdom-west us-central us-east us-east-2 us-north-central us-south-central us-west us-west-2 us-west-central"> <button class="module-builder" data-event="pricingdetails-clicked-addinstance" data-event-property="B4MS" data-module-configuration='{"tier": "standard", "size": "b4ms", "operatingSystem" : "windows", "type": "os-only", "license": ""}' data-notification-title="B4MS" data-product="virtual-machines" type="button"> <span class="icon icon-size2"><svg aria-hidden="true" role="presentation"><use xlink:href="#svg-add-button"></use></svg></span> </button> </span> </td>, <td>B4MS</td>, <td>4</td>, <td>16.00 GiB</td>, <td>32 GiB</td>, <td class="payg-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.316,"asia-pacific-southeast":0.2529,"australia-east":0.297,"australia-southeast":0.297,"brazil-south":0.329,"canada-central":0.222,"canada-east":0.247,"central-india":0.251,"europe-north":0.219,"europe-west":0.2313,"japan-east":0.297,"japan-west":0.297,"korea-central":0.267,"korea-south":0.241,"south-india":0.276,"united-kingdom-south":0.253,"united-kingdom-west":0.253,"us-central":0.252,"us-east":0.2061,"us-east-2":0.252,"us-north-central":0.229,"us-south-central":0.252,"us-west":0.257,"us-west-2":0.229,"us-west-central":0.252}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.21931,"asia-pacific-southeast":0.15150,"australia-east":0.16246,"australia-southeast":0.16246,"brazil-south":0.17376,"canada-central":0.13506,"canada-east":0.13506,"central-india":0.15002,"europe-north":0.14842,"europe-west":0.15869,"japan-east":0.16931,"japan-west":0.16931,"korea-central":0.14454,"korea-south":0.11885,"south-india":0.17684,"united-kingdom-south":0.15367,"united-kingdom-west":0.15367,"us-central":0.14477,"us-east":0.12331,"us-east-2":0.14477,"us-north-central":0.12331,"us-south-central":0.14477,"us-west":0.16577,"us-west-2":0.12331,"us-west-central":0.14477}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.14511,"asia-pacific-southeast":0.10207,"australia-east":0.11436,"australia-southeast":0.11436,"brazil-south":0.12860,"canada-central":0.09332,"canada-east":0.09332,"central-india":0.10051,"europe-north":0.10420,"europe-west":0.11303,"japan-east":0.12057,"japan-west":0.12057,"korea-central":0.10405,"korea-south":0.08643,"south-india":0.11741,"united-kingdom-south":0.10930,"united-kingdom-west":0.10930,"us-central":0.09975,"us-east":0.08579,"us-east-2":0.09975,"us-north-central":0.08579,"us-south-central":0.09975,"us-west":0.11178,"us-west-2":0.08579,"us-west-central":0.09975}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data
#" data-amount='{"regional":{"asia-pacific-east":0.12911,"asia-pacific-southeast":0.08607,"australia-east":0.09836,"australia-southeast":0.09836,"brazil-south":0.1126,"canada-central":0.07732,"canada-east":0.07732,"central-india":0.08451,"europe-north":0.0882,"europe-west":0.09703,"japan-east":0.10457,"japan-west":0.10457,"korea-central":0.08805,"korea-south":0.07043,"south-india":0.10141,"united-kingdom-south":0.0933,"united-kingdom-west":0.0933,"us-central":0.08375,"us-east":0.06979,"us-east-2":0.08375,"us-north-central":0.06979,"us-south-central":0.08375,"us-west":0.09578,"us-west-2":0.06979,"us-west-central":0.08375}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td> <span class="wa-conditionalDisplay" data-condition-region="asia-pacific-east asia-pacific-southeast australia-east australia-southeast brazil-south canada-central canada-east central-india europe-north europe-west japan-east japan-west korea-central korea-south south-india united-kingdom-south united-kingdom-west us-central us-east us-east-2 us-north-central us-south-central us-west us-west-2 us-west-central"> <button class="module-builder" data-event="pricingdetails-clicked-addinstance" data-event-property="B8MS" data-module-configuration='{"tier": "standard", "size": "b8ms", "operatingSystem" : "windows", "type": "os-only", "license": ""}' data-notification-title="B8MS" data-product="virtual-machines" type="button"> <span class="icon icon-size2"><svg aria-hidden="true" role="presentation"><use xlink:href="#svg-add-button"></use></svg></span> </button> </span> </td>, <td>B8MS</td>, <td>8</td>, <td>32.00 GiB</td>, <td>64 GiB</td>, <td class="payg-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.61,"asia-pacific-southeast":0.4878,"australia-east":0.574,"australia-southeast":0.574,"brazil-south":0.639,"canada-central":0.427,"canada-east":0.474,"central-india":0.484,"europe-north":0.419,"europe-west":0.4446,"japan-east":0.574,"japan-west":0.574,"korea-central":0.517,"korea-south":0.465,"south-india":0.533,"united-kingdom-south":0.486,"united-kingdom-west":0.486,"us-central":0.482,"us-east":0.3942,"us-east-2":0.482,"us-north-central":0.438,"us-south-central":0.482,"us-west":0.495,"us-west-2":0.438,"us-west-central":0.482}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.43851,"asia-pacific-southeast":0.30300,"australia-east":0.32504,"australia-southeast":0.32504,"brazil-south":0.34753,"canada-central":0.27013,"canada-east":0.27013,"central-india":0.30004,"europe-north":0.29673,"europe-west":0.31727,"japan-east":0.33874,"japan-west":0.33874,"korea-central":0.28896,"korea-south":0.23759,"south-india":0.35369,"united-kingdom-south":0.30734,"united-kingdom-west":0.30734,"us-central":0.28953,"us-east":0.24661,"us-east-2":0.28953,"us-north-central":0.24661,"us-south-central":0.28953,"us-west":0.33166,"us-west-2":0.24661,"us-west-central":0.28953}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.29022,"asia-pacific-southeast":0.20415,"australia-east":0.22877,"australia-southeast":0.22877,"brazil-south":0.25719,"canada-central":0.18660,"canada-east":0.18660,"central-india":0.20103,"europe-north":0.20837,"europe-west":0.22606,"japan-east":0.24113,"japan-west":0.24113,"korea-central":0.20807,"korea-south":0.17287,"south-india":0.23482,"united-kingdom-south":0.21861,"united-kingdom-west":0.21861,"us-central":0.19950,"us-east":0.17157,"us-east-2":0.19950,"us-north-central":0.17157,"us-south-central":0.19950,"us-west":0.22359,"us-west-2":0.17157,"us-west-central":0.19950}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>, <td class="discounted-price"> <span class="price-data " data-amount='{"regional":{"asia-pacific-east":0.25822,"asia-pacific-southeast":0.17215,"australia-east":0.19677,"australia-southeast":0.19677,"brazil-south":0.22519,"canada-central":0.1546,"canada-east":0.1546,"central-india":0.16903,"europe-north":0.17637,"europe-west":0.19406,"japan-east":0.20913,"japan-west":0.20913,"korea-central":0.17607,"korea-south":0.14087,"south-india":0.20282,"united-kingdom-south":0.18661,"united-kingdom-west":0.18661,"us-central":0.1675,"us-east":0.13957,"us-east-2":0.1675,"us-north-central":0.13957,"us-south-central":0.1675,"us-west":0.19159,"us-west-2":0.13957,"us-west-central":0.1675}}' data-decimals="3" data-hour-format="{0}/hour" data-month-format="{0}/month" data-region-unavailable="N/A">$-</span> <span class="percent-savings"></span> </td>]
'''