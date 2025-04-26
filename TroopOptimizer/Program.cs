using TroopOptimizer.Models;

var test = new TroopOptimizer.TroopOptimizer.TroopOptimizer();
var aR = new ResourceAmount(5000, 5000, 5000, 5000);
var t1 = new ResourceAmount(100, 200, 400, 40);
var t2 = new ResourceAmount(400, 200, 100, 50);


test.CalculateOptimizedNumberOfTroops(aR, t1, t2);
return;
var builder = WebApplication.CreateBuilder(args);


// Add services to the container.
builder.Services.AddRazorPages();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();
