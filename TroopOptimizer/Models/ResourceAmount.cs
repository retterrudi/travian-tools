namespace TroopOptimizer.Models;

public class ResourceAmount
{
    private int Lumber { get; }
    private int Clay { get; }
    private int Iron { get; }
    private int Crop { get; }

    public ResourceAmount(int lumber, int clay, int iron, int crop)
    {
        Lumber = lumber;
        Clay = clay;
        Iron = iron;
        Crop = crop;
    }
    
    public int Sum() => Lumber + Clay + Iron + Crop;

    public int CountOfMaxPurchases(ResourceAmount costs) => 
        new List<int>() {
                Lumber / costs.Lumber, 
                Clay / costs.Clay, 
                Iron / costs.Iron, 
                Crop / costs.Crop
            }.Min();

    public bool ContainsNegativeValue() =>
        Lumber < 0 || Clay < 0 || Iron < 0 || Crop < 0;

    public static ResourceAmount operator +(ResourceAmount left, ResourceAmount right) =>
        new ResourceAmount(
            left.Lumber + right.Lumber, 
            left.Clay + right.Clay, 
            left.Iron + right.Iron,
            left.Crop + right.Crop);

    public static ResourceAmount operator *(int left, ResourceAmount right) =>
        new ResourceAmount(
            left * right.Lumber, 
            left * right.Clay, 
            left * right.Iron, 
            left * right.Crop);
    
    public static ResourceAmount operator * (ResourceAmount left, int right) =>
        new ResourceAmount(
            right * left.Lumber, 
            right * left.Clay, 
            right * left.Iron, 
            right * left.Crop);

    public static ResourceAmount operator -(ResourceAmount left, ResourceAmount right) =>
        new ResourceAmount(
            left.Lumber - right.Lumber, 
            left.Clay - right.Clay, 
            left.Iron - right.Iron, 
            left.Crop - right.Crop);
}