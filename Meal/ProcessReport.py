import pandas as pd
import re


class ProcessReport:

    @classmethod
    def convertToCsv(cls, allList: list, strDate: str, goWhere: str) -> None:

        # handle food price
        updatedFoodPrice = cls.handlePriceFood(allList[3])

        dummyDict = {

            "location": allList[0],
            "address": allList[1],
            "link": allList[2],
            "foodPrice": updatedFoodPrice,
        }

        print("Preparing to export to csv file ...")

        # convert to dataframe from dict using pandas
        df = pd.DataFrame(dummyDict)

        # csvName
        fName = f"{goWhere}_budget meal within 2km_{strDate}.csv"

        # from dataframe to csv
        df.to_csv(fName, index=False)

        print('Data exported to csv !')

    @classmethod
    def handlePriceFood(cls, aLis: list):

        print('Processing the foodprice data ...')

        # just a simple handling of that string to remove some chars and substring
        processedLis = [cls.simpleProcess1(x) for x in aLis]

        return processedLis

    @classmethod
    def simpleProcess1(cls, s1: str) -> str:

        # example of the string scraped
        # '1. Fishball Noodle ($3.50)\n2. Economy Rice (2 Veg & 1 Meat) ($3.50)\n3. Mee Rebus ($3.00) - Halal\n4. Nasi Lemak ($3.50) - Halal\n5. Kopi O ($1.20)\n6. Teh O ($1.20)'

        # split to remove the 1. xxxx
        lis0 = s1.split(" ", 1)
        # print(lis0[1])

        # remove the n/2. n/3.  ...from strimg
        return re.sub("\\n\d\.\s+", ",", lis0[1])
