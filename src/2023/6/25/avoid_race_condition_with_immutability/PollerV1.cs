using System.Diagnostics;

public interface IPollerV1
{
    void Start();
    void AddMore(params string[] items);
    Task WaitAndComplete();
}

// This implementation is not thread safe!
public class Poller : IPollerV1
{
    private bool _hasMore = true;
    private object _hasMoreLock = new Object();

    private List<string> _items;
    private object _itemsLock = new Object();

    private Task? _task;

    public Poller(params string[] initialItems) => _items = initialItems.ToList();

    public void Start()
    {
        _task = Task.Run(async () => 
        {
            var timer = new Stopwatch();
            timer.Start();

            var hasMore = true;
            while (hasMore || timer.Elapsed < TimeSpan.FromSeconds(5))
            {
                lock (_hasMoreLock)
                {
                    hasMore = _hasMore;
                }

                if (hasMore)
                {
                    timer.Restart();
                }

                lock (_itemsLock)
                {
                    Poll.Items(_items).GetAwaiter().GetResult();
                }

                await Task.Delay(TimeSpan.FromSeconds(1));
            }
        });
    }

    public void AddMore(params string[] items)
    {
        lock (_itemsLock)
        {
            _items.AddRange(items);
        }
    }

    public async Task WaitAndComplete()
    {
        lock (_hasMoreLock)
        {
            _hasMore = false;
        }
        await _task!;
    }
}