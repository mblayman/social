# social

A different kind of social network

## Goals

Many social networks
become a popularity contest.
People want to gain a big audience
to broadcast whatever message
they want to share.

What if a social network
reflected your real life network
and acted as a rolodex
for your life?
What if you were limited
in the number of connections
you could have
on the network
to force you
to make choices that matter?

You don't need to be connected
to that guy
from high school
that you barely knew.
You probably don't really care
about the new baby
that he and his wife just had.

If a social network protected you
from spammy people
by limiting the number connections
you could have,
that would go a long way
to make your *real* social network more meaningful.

But we can go further!
Let's cap the number
of connection requests someone can make too!
If requests to connect are as limited
as the actual connections,
then those annoying recruiters will think twice
before trying to add you
to their network.

This is the vision
behind this social network.
I want to create a network full
of real connections
to people that you really care about.

## The Rules

1. The maximum number of connections is 500.

For this concept to work,
there has to be a ceiling.
The choice here is arbitrary
and based on zero scientific research,
but 500 is a nice round number
that seems reasonable.

2. Connection requests count as part of the total 500 connections.

The network should have real connection
between people
that really have some kind of relationship
with each other.

If you're that annoying person
who tries to connect to people
that you don't know
to selfishly boost your reach,
this social network will hold that against you.

A connection request can transition
between a few states:

* Pending -> Sent:
  A invitation requested by you is sent out via email to the other person.
* Sent -> Accepted:
  You've made a real connection and the other person accepted.
* Sent -> Rejected:
  You tried to connect to someone and they didn't want to connect.
  That means you burned 1 of your 500 possible connections.
* Sent -> Expired:
  You tried to connect to someone and they didn't respond.
  Guess what? That probably means they didn't want to connect,
  but they maybe didn't want to hurt your feelings.
  That still means you burned 1 of your 500 possible connections.

3. Existing connections can be burned but not severed.

Break-ups happen.
Sometimes relationships fall apart for different reasons.
The connection to that person is permanent,
but you can burn it
so they can never be part
of your network again.

A burned connection counts as part of the 500.
Why?
If connections can be severed,
the system can be easily gamed.
A connection in real life can be a sad/bad memory,
but it was still part of life.
Connection in the network should reflect that too.

These rules are all intended
to create a tension.
The rules exist
to force people to make choices
with significance.

## MVP Features

### Keeping contact information in sync

All information is private by default (in contrast to Facebook)

Access control / permissions:

* Inner circle (full visibility)
* Middle circle
* Outer circle (connections default to the outer circle)

Field example:

* Email: inner circle, middle circle, !outer circle

### Invitation flow

Two types of people that you would invite.

1. People that already have accounts.

Connection request would count against the total.

2. People that don't have an account.

Use an invitation flow that doesn't impact the total.
