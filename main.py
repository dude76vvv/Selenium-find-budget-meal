from Meal.MealBot import BudgetMeal
from Meal.ProcessReport import ProcessReport as pr


goWhere = input("Enter a place to have budget meal(s):")

print("Finding budget meal(s) within 2km of ur input location")
print("Script will start now. Pls wait")

try:

    bot = BudgetMeal()
    bot.visitPage()
    bot.enterInput(goWhere)
    # bot.enterInput("taman jurong")
    # bot.enterInput("taman jurong cente")   #for testing failed

    # to apply hala filter
    # if(bot.checkResults(filterHala=True)):
    if (bot.checkResults()):

        print('Getting the results ...')

        resList, lastUpdatedDate = bot.get2kmResults()

        if resList:

            print('Processing the collected results ...')
            pr.convertToCsv(resList, lastUpdatedDate, goWhere)

    else:

        print('No results from the user input')

    print('Tearing down now ...')


except Exception as e:

    print('Oops something broke !')
    bot.closePage()
    print(e)


finally:
    print("Exiting script ...")
    bot.closePage()
