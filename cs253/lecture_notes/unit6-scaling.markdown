# Techniques for scaling

## Optimising code

If you have the option between buying a machine and figuring out how to have
multiple machines running your website OR optimising your code, you should
consider the cost of each:

Cost/Machine + maintenance **VS** Cost/Developer

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




## Upgrading machines

Replacing machines used now with those with faster & more memory, more diskspace,
faster CPUs etc

## _Add_ more machines
