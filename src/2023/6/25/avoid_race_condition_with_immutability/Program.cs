static class Program
{
    public static async Task Main(string[] args)
    {
        const string help = @"
Usage:
  v1 - Run Poller V1
  v2 - Run Poller v2
";
        if (args.Length < 1)
        {
            Console.Write(help);
            return;
        }
        switch (args[0].ToLowerInvariant())
        {
            case "v1":
                await RunPollerV1();
                return;
            case "v2":
                await RunPollerV2();
                return;
            default:
                Console.Write(help);
                return;
        }
    }

    private static async Task RunPollerV1()
    {
        var poller = new Poller("1", "2", "3");
        poller.Start();

        await Task.Delay(TimeSpan.FromSeconds(3));
        poller.AddMore("4");

        await Task.Delay(TimeSpan.FromSeconds(3));
        poller.AddMore("5");

        await poller.WaitAndComplete();
    }

    private static async Task RunPollerV2()
    {
        var poller = new PollerV2("1", "2", "3").Start();

        await Task.Delay(TimeSpan.FromSeconds(3));
        poller = await poller.WithMore("4");

        await Task.Delay(TimeSpan.FromSeconds(3));
        poller = await poller.WithMore("5");

        var timeoutPoller = await poller.WithTimeout();
        await timeoutPoller.WaitAndComplete();
    }
}
