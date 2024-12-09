import time

import Model.YFinanceAdaptor as dm

rand = dm.DataManagerDecorator()
rand.addRandomClose()
while True:
    rand.addRandomClose()
    time.sleep(0.1)