# The Go Implementation of LRU Cache

Notes from reading Hashicorp's [golang-lru](https://github.com/hashicorp/golang-lru) repository.

LRU (Least Recently Used) cache is a widely used data structure. The [golang-lru](https://github.com/hashicorp/golang-lru) repository is an examplar implementation of LRU in Go. The repo exposes three implementations:

## (Standard) LRU

The standard LRU is implemented as a wrapper around the `SimpleLRU` structure. The main logic is in `SimpleLRU`, the wrapper contains a lock field and maintains thread safety.

The idea for implementing the core `SimpleLRU` structure is straightforward. The entries are put in a doubly linked list and a map at the same time. The linked list maintains the recency order. The map ensures random access.

When an entry is added, it is added in the map, and at the same time pushed to the front of the linked list. If the capacity is exceeded, the oldest entry, which is at the back of the linked list, is dropped and removed from the map.

When an entry is accessed, it is moved in the linked list to the front.

Accessing entries from the map, moving an entry to the front of linked list, and dropping the oldest entry are all O(1) operations.

Interestingly, the doubly linked list is implemented as a ring, with a `root` entry as the sentinel value. It is the "next" element of the last element, and the "prev" element of the first element. It is used to check if an element is the first or last, as well as quickly find the first and last elements.

## 2Q LRU & ARC

The 2Q (2 Queue) LRU and ARC (Adaptive Replacement Cache) are improvements over the standard LRU. The idea is, if there are a flood of new entries which are used only once added to the LRU cache, it will evict older but more frequently used entries. So these implementations balance recency and frequency. ARC is a special case for 2Q LRU.

As the name suggests, the 2Q LRU keeps two separate `SimpleLRU` instances to keep track of frequently used entries and entries that have only been accessed once. The second queue works as a buffer. Any entries are added to the second queue first. Only when they are accessed twice are they promoted to the first queue.

When entries need to be evicted, if there are many entries in the second queue (e.g. more than 25% of the total items, the percentage is configurable), the entries in the second queue are evicted first, because they are only accessed once.

---
[Home](../../../../../README.md)