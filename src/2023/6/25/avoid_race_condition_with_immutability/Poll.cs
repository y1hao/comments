public static class Poll
{
    //.Mocks some time-consuming polling operation against each of the items
    public static async Task Items(IEnumerable<string> items)
    {
        await Task.Yield();
        Console.Write("Polling: ");
        Console.WriteLine(string.Join(", ", items));
    }
}