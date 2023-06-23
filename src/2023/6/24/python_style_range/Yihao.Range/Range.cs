namespace Yihao.Range;

public static class RangeExtensions
{
    public static IEnumerator<int> GetEnumerator(this (int From, int To) range)
    {
        for (int i = range.From; i < range.To; i++)
        {
            yield return i;
        }
    }

    public static IEnumerator<int> GetEnumerator(this (int From, int To, int Step) range)
    {
        if (range.Step == 0)
        {
            throw new ArgumentOutOfRangeException(nameof(range), $"'{nameof(range.Step)}' cannot be zero");
        }
        if (range.Step > 0)
        {
            if (range.From >= range.To)
            {
                yield break;
            }
            for (int i = range.From; i < range.To; i += range.Step) 
            {
                yield return i;
            }
        }
        else
        {
            if (range.From <= range.To)
            {
                yield break;
            }
            for (int i = range.From; i > range.To; i += range.Step) 
            {
                yield return i;
            }
        }
    }
}

public class Tests
{
    [Fact]
    public void TestRange()
    {
        var got = new List<int>();
        foreach (var i in (1, 10)) 
        {
            got.Add(i);
        }
        Assert.Equal(got, new List<int>{1, 2, 3, 4, 5, 6, 7, 8, 9});
    }

    [Fact]
    public void TestRangeWithZeroStep()
    {
        Assert.Throws<ArgumentOutOfRangeException>(() => 
        {
            foreach (var i in (1, 10, 0)) 
            {
            }
        });
    }

    [Fact]
    public void TestRangeWithPositiveStep_Ascending()
    {
        var got = new List<int>();
        foreach (var i in (1, 10, 2)) 
        {
            got.Add(i);
        }
        Assert.Equal(got, new List<int>{1, 3, 5, 7, 9});
    }

    [Fact]
    public void TestRangeWithPositiveStep_Descending()
    {
        var got = new List<int>();
        foreach (var i in (10, 1, 2)) 
        {
            got.Add(i);
        }
        Assert.Equal(got, new List<int>{ });
    }

    [Fact]
    public void TestRangeWithNegativeStep_Ascending()
    {
        var got = new List<int>();
        foreach (var i in (1, 10, -2)) 
        {
            got.Add(i);
        }
        Assert.Equal(got, new List<int>{});
    }

    [Fact]
    public void TestRangeWithNegativeStep_Descending()
    {
        var got = new List<int>();
        foreach (var i in (10, 1, -2)) 
        {
            got.Add(i);
        }
        Assert.Equal(got, new List<int>{10, 8, 6, 4, 2});
    }
}