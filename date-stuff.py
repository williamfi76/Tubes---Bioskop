from datetime import datetime

from Controller import adminController

currDate = datetime(2022,12,12)

adminController.addNewShowing(5, datetime(2025,6,10,12,30), datetime(2025,5,29,15,30), 1)
adminController.addNewShowing(5, datetime(2025,6,10,16,00), datetime(2025,5,29,18,00), 1)
adminController.addNewShowing(5, datetime(2025,6,10,18,30), datetime(2025,5,29,20,30), 1)