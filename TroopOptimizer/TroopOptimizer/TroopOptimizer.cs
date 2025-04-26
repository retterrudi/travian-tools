using TroopOptimizer.Models;

namespace TroopOptimizer.TroopOptimizer;

public class TroopOptimizer
{
    private ILogger _logger = default;
    private int _stepSize = 5;
    private int _redefineWindow = 5;

    public TroopOptimizer(ILogger logger)
    {
        _logger = logger;
    }

    public TroopOptimizer()
    {
        
    }
    
    public (int countTroopType1, int countTroopType2) CalculateOptimizedNumberOfTroops(
        ResourceAmount availableResourceAmount, 
        ResourceAmount troopCost1, 
        ResourceAmount troopCost2, 
        bool ignoreCropCost = false)
    {
        var bestN1Coarse = 0;
        var bestN2Coarse = 0;
        var minRemainingSumCoarse = availableResourceAmount.Sum();
        var minAbsDiffCoarse = int.MaxValue;

        var maxTroop1 = availableResourceAmount.CountOfMaxPurchases(troopCost1);

        for (var n1 = 0; n1 <= maxTroop1; n1 += _stepSize)
        {
            var costForN1 = n1 * troopCost1;
            var remainingAfterN1 = availableResourceAmount - costForN1;

            var maxTroop2GivenN1 = remainingAfterN1.CountOfMaxPurchases(troopCost2);
            if (!(maxTroop2GivenN1 > 0)) continue;

            for (var n2 = 0; n2 <= maxTroop2GivenN1; n2 += _stepSize)
            {
                var totalCost = n1 * troopCost1 + n2 * troopCost2;
                if (!(availableResourceAmount - totalCost).ContainsNegativeValue())
                {
                    var remainingResources = availableResourceAmount - totalCost;
                    var currentRemainingSum = remainingResources.Sum();
                    var currentAbsDiff = Math.Abs(n1 - n2);

                    if (currentRemainingSum < minRemainingSumCoarse)
                    {
                        minRemainingSumCoarse = currentRemainingSum;
                        bestN1Coarse = n1;
                        bestN2Coarse = n2;
                        minAbsDiffCoarse = currentAbsDiff;
                    }
                    else if (currentRemainingSum == minRemainingSumCoarse)
                    {
                        if (currentAbsDiff < minAbsDiffCoarse)
                        {
                            bestN1Coarse = n1;
                            bestN2Coarse = n2;
                            minAbsDiffCoarse = currentAbsDiff;
                        }
                    }
                }
            }
        }
        
        var bestN1Fine = bestN1Coarse;
        var bestN2Fine = bestN2Coarse;
        var minRemainingSumFine = minRemainingSumCoarse;
        var minAbsDiffFine = minAbsDiffCoarse;

        var n1Min = Math.Max(0, bestN1Coarse - _redefineWindow);
        var n1Max = bestN1Coarse + _redefineWindow;
        var n2MinBase = Math.Max(0, bestN2Coarse - _redefineWindow);
        var n2MaxBase = bestN2Coarse + _redefineWindow;

        for (var n1 = n1Min; n1 <= n1Max; ++n1)
        {
            var costForN1 = n1 * troopCost1;
            var remainingAfterN1 = availableResourceAmount - costForN1;

            var maxTroop2GivenN1 = remainingAfterN1.CountOfMaxPurchases(troopCost2);
            if (!(maxTroop2GivenN1 > 0)) continue;

            var n2Min = n2MinBase;
            var n2Max = Math.Min(maxTroop2GivenN1, n2MaxBase);

            for (var n2 = n2Min; n2 <= n2Max; ++n2)
            {
                var totalCost = n1 * troopCost1 + n2 * troopCost2;
                if (!(availableResourceAmount - totalCost).ContainsNegativeValue())
                {
                    var remainingResources = availableResourceAmount - totalCost;
                    var currentRemainingSum = remainingResources.Sum();
                    var currentAbsDiff = Math.Abs(n1 - n2);

                    if (currentRemainingSum < minRemainingSumFine)
                    {
                        minRemainingSumFine = currentRemainingSum;
                        bestN1Fine = n1;
                        bestN2Fine = n2;
                        minAbsDiffFine = currentAbsDiff;
                    }
                    else if (currentRemainingSum == minRemainingSumFine)
                    {
                        if (currentAbsDiff < minAbsDiffFine)
                        {
                            bestN1Fine = n1;
                            bestN2Fine = n2;
                            minAbsDiffFine = currentAbsDiff;
                        }
                    }
                }
            }
        }

        return (bestN1Fine, bestN2Fine);
    }
    
}