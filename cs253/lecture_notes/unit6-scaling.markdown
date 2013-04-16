# Techniques for scaling

## Optimising code

If you have the option between buying a machine and figuring out how to have
multiple machines running your website OR optimising your code, you should
consider the cost of each:

Cost/Machine + maintenance **VS** Cost/Developer

Make sure you're using indexes where appropriate, tweak your queries to be simpler, rearrange your tables (ignore all that normalisation crap), make sure the queries are sane...

## _Caching_ complex operations

Storing the result of an operation so that future requests return faster.

### When do we cache?

* computation is slow
* computation will run multiple times
* when the output is the same for a particular input
* your hosting provider charges for DB access

Lets say `db.read()` takes 100ms. If every request needs to run this, and you
have a lot of requests, they take a long time to all perform.

A cache is a essentially a hashtable mapping DB requests to DB responses:

        if request in cache:
            # cache hit < 1ms
            return cache[request]
        else:
            # cache miss ~100ms
            r = db_read()
            cache[request] = r
            return r

**Jargon:** *Warm cache* -- requested data is already in there.

### Stale Cache

When you update the database but not the cache, your cache becomes out of date

Fixed by either clearing the cache when DB is updated, or updating the cache along with the DB

### Cache stampede

Someone posts (causing DB update and thus a cache clear) and lots of people visit the site at the same time, which causes a DB read for each simultaneous visit! i.e. A cache stampede is when multiple cache misses create too much load on the database.

This can be avoided by not clearing the cache, but instead overwriting it with the new data

### Cachine Techniques

Approach | DB read/pageview | DB read/submission | Bugs?
--- | --- | --- | ---
no caching | every | none | no
naive caching | cache miss | none | yes -- stale
clear cache | cache miss | none | no
refresh cache | rarely -- only when cache empty | 1 | no
update cache | 0 | 0 | no

**Simple users shouldn't touch the database**

## Upgrading machines

Replacing machines used now with those with faster & more memory, more diskspace,
faster CPUs etc

## _Add_ more machines

Replication, sharding...

# App Server Scaling

* processed request
* DB query
* collate results
* render HTML

We can add multiple machines to handle each of these requests

## Load balancer

Optimised hardware that Sits between the user and all of your app servers, and Spreads requests across multiple machines. It has a list of all the app servers and decides which to forward each request to. It decides using some scheduling algorithm (round robin, or load based decision, or ...). That's all it does. It doesn't render anything, it doesn't touch the DB, it doesn't touch the cache...

# Memcached

A server -- often you run it on it's own machine

1. User Request comes into your app servers
2. Chech memcached to see if it's in there
3. If it is, send back to the user,
4. If not, check the DB

Simple. All of your app servers can interact with memcached, it supports many sockets, and you  can have many memcached servers. It's essentially a key->value dictionary, and you can hash to decide what memcached server to cache to.

You can have a memcached server running on each of your
app servers, which interact with each standalone memcached
server, and you get this big complicated ball of
connections... Urm... but everything works out in the end

Memcached gives you these operations.

		set(key, value)
		get(key) -> value
		delete(key)
		flush() # clear entire cache

Features:

* Fast
* Not durable
* Limited by how much memory you have
* LRU cache -- Throws away data that's **L**east **R**ecently **U**sed

## Stateless

* cache survives restarts
* app using memcached is now **stateless** (crucial to scaling)
** no state between restarts
** apps are now interchangable
** adding apps is easy
** apps can be scaled independent of cache and db

So state is stored in either cookies, DB, or memcached but **NOT** the apps! :)

# Advanced cache updates

## Problem

Multiple users submit at the same time update cache at same time, overwriting eachother (known as squashing).

## Solutions

###CAS -- Check and Set

		gets(key) -> value, unique
		# unique is a hash of the value
		# compare to get(key) -> value

		cas(key, value, unique) -> True if the unique matches the unique in the cache, else: 
		                        -> False
		# compare to set(key, value)

### Example:

t | App1 | App 2
--- | --- | ---
1 | v,u = mc.gets(k) | v,u = mc.gets(k)
2 | mc.cas(k,y,u) -> True | mc.cas(k,y,u) -> False because App1 got there first and u changed