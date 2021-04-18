"""
Asset Value: The AssetValue class is used for approximating user asset value and wealth. This is initially used for modeling real estate property value. 
This model currently assumes that the asset value only appreciates at a given rate (asset return rate).

Future model considerations: Integrate stochastic asset return rate... or damages to the market structure?

"""

class AssetValue():
    """
    Model for approximating asset value and wealth.
    Initially used for property value
    """
    
    def __init__(self, assetReturnRate):
        self.assetReturnRate = assetReturnRate / 12
        
    def getAssetValue(self, assetPrincipal, compoundPeriod):
        # calculates asset value on a periodic compounding per month
        assetValue = assetPrincipal * (1 + self.assetReturnRate)**compoundPeriod
        return assetValue
    
    
if __name__ == '__main__':
    pass