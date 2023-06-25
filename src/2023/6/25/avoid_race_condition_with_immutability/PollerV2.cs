using System.Diagnostics;

public interface IPollerV2
{
    IWaitForMorePoller Start();
}

public interface IWaitForMorePoller
{
    Task<IWaitForMorePoller> WithMore(params string[] items);
    Task<IWaitForTimeoutPoller> WithTimeout();
}

public interface IWaitForTimeoutPoller
{
    Task WaitAndComplete();
}

public class PollerV2 : IPollerV2
{
    private string[] _items;
    public PollerV2(params string[] initialItems) => _items = initialItems.ToArray();
    public IWaitForMorePoller Start() => new WaitForMorePoller(_items);
}

public class WaitForMorePoller : IWaitForMorePoller
{
    private CancellationTokenSource _cts = new CancellationTokenSource();
    private Task _task;
    private string[] _items;

    public WaitForMorePoller(params string[] items)
    {
        _items = items.ToArray();
        _task = Task.Run(async () => 
        {
            while (!_cts.Token.IsCancellationRequested)
            {
                await Poll.Items(_items);
                await Task.Delay(TimeSpan.FromSeconds(1));
            }
        });
    }

    public async Task<IWaitForMorePoller> WithMore(params string[] items)
    {
        var newItems = _items.ToList();
        newItems.AddRange(items);

        await Cancel();

        return new WaitForMorePoller(newItems.ToArray());
    }

    public async Task<IWaitForTimeoutPoller> WithTimeout()
    {
        await Cancel();
        return new WaitForTimeoutPoller(_items);
    }

    private async Task Cancel()
    {
        _cts.Cancel();
        await _task;
    }
}

public class WaitForTimeoutPoller : IWaitForTimeoutPoller
{
    private Task _task;
    private string[] _items;
    public WaitForTimeoutPoller(params string[] items)
    {
        _items = items.ToArray();

        var timer = new Stopwatch();
        timer.Start();
        
        _task = Task.Run(async () => 
        {
            while (timer.Elapsed < TimeSpan.FromSeconds(5))
            {
                await Poll.Items(_items);
                await Task.Delay(TimeSpan.FromSeconds(1));
            }
        });
    }

    public async Task WaitAndComplete() => await _task;
}